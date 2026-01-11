from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error, median_absolute_error
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import psycopg2


def database_connection():
    connection = psycopg2.connect(
        database="air_pollution",
        user = "airflow",
        password = "airflow",
        host = "localhost",
        port = "5432"
    )
    return connection

def read_weather_data(path):
    df = pd.read_csv(path, sep=',')
    df.columns=['time', 'temp', 'hum', 'press', 'wind']
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df['month'] = df['time'].dt.month
    df.dropna(inplace=True)
    return df

def read_smog_data(path):
    df = pd.read_csv(path, sep=',', header=None)
    df.drop(columns=[2], inplace=True)
    df.columns = ['time', 'pm25']
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df.dropna(inplace=True)
    return df

def read_weather_data_from_db(connection):
    cursor = connection.cursor()
    query = """
    SELECT time, temp, hum, press, wind 
    FROM weather
    ORDER BY time
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    
    df = pd.DataFrame(rows, columns=['time', 'temp', 'hum', 'press', 'wind'])
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df['month'] = df['time'].dt.month
    df.dropna(inplace=True)
    return df

def read_smog_data_from_db(connection):
    cursor = connection.cursor()
    query = """
    SELECT time, pm25 
    FROM pollution
    ORDER BY time
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    
    df = pd.DataFrame(rows, columns=['time', 'pm25'])
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df.dropna(inplace=True)
    return df

def prepare_data(connection):
    weather = read_weather_data_from_db(connection)
    pm25 = read_smog_data_from_db(connection)
    df = pd.merge(weather, pm25, on='time', how='inner')
    X = df[['temp', 'press', 'hum', 'wind', 'month']]
    y = df['pm25']
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test

def prepare_data_from_csv(weather_path, smog_path):
    weather = read_weather_data(weather_path)
    pm25 = read_smog_data(smog_path)
    df = pd.merge(weather, pm25, on='time', how='inner')
    X = df[['temp', 'press', 'hum', 'wind', 'month']]
    y = df['pm25']
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(model, param_grid, X_train, y_train):
    grid = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring='neg_mean_absolute_error',
        cv=5,
        n_jobs=-1,
        verbose=1
    )
    grid.fit(X_train, y_train)
    fitted_model = grid.best_estimator_
    return fitted_model

def evaluate_model(fitted_model, X_test, y_test):
    y_pred = fitted_model.predict(X_test)
    
    mse = round(mean_squared_error(y_test, y_pred), 2)
    rmse = round(np.sqrt(mean_squared_error(y_test, y_pred)), 2)
    mae = round(mean_absolute_error(y_test, y_pred), 2)
    r2 = round(r2_score(y_test, y_pred), 2)
    
    mape = round(mean_absolute_percentage_error(y_test, y_pred), 2)
    median_ae = round(median_absolute_error(y_test, y_pred), 2)
    
    residuals = y_test - y_pred
    residuals_std = round(np.std(residuals), 2)
    residuals_mean = round(np.mean(residuals), 2)
    
    pred_min = round(np.min(y_pred), 2)
    pred_max = round(np.max(y_pred), 2)
    actual_min = round(np.min(y_test), 2)
    actual_max = round(np.max(y_test), 2)
    
    results = {
        'MSE': mse,
        'RMSE': rmse,
        'MAE': mae,
        'R2': r2,
        'MAPE': mape,
        'Median_AE': median_ae,
        'Residuals_Mean': residuals_mean,
        'Residuals_Std': residuals_std,
        'Pred_Min': pred_min,
        'Pred_Max': pred_max,
        'Actual_Min': actual_min,
        'Actual_Max': actual_max
    }
    
    return results

def print_results(results, model_name):
    print(f"\n{'='*60}")
    print(f"Results for {model_name} model:")
    print(f"{'='*60}")
    
    print(f"  R² Score:                 {results['R2']}")
    print(f"  RMSE (Root Mean Sq. Error): {results['RMSE']}")
    print(f"  MAE (Mean Absolute Error):  {results['MAE']}")
    print(f"  MSE (Mean Squared Error):   {results['MSE']}")
    print(f"  MAPE (Mean Abs. % Error):   {results['MAPE']}%")
    print(f"  Median Absolute Error:    {results['Median_AE']}")
    
    print("\nResiduals Analysis:")
    print(f"  Residuals Mean:           {results['Residuals_Mean']}")
    print(f"  Residuals Std Dev:        {results['Residuals_Std']}")
    
    print("\nValue Ranges:")
    print(f"  Predicted Range:  [{results['Pred_Min']}, {results['Pred_Max']}]")
    print(f"  Actual Range:     [{results['Actual_Min']}, {results['Actual_Max']}]")
    print(f"{'='*60}\n")


def main():
    print("Connecting to PostgreSQL database...")
    connection = database_connection()
    
    try:
        print("Preparing data from database...")
        X_train, X_test, y_train, y_test = prepare_data(connection)
        print("Data prepared, length of training set:", len(X_train), "length of test set:", len(X_test))

        print("Training model...")
        RF = RandomForestRegressor()

        RF_param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20, 30]
        }

        RF_model = train_model(RF, RF_param_grid, X_train, y_train)

        print("Evaluating model...")
        RF_results = evaluate_model(RF_model, X_test, y_test)
        print_results(RF_results, "Random Forest Regressor")
    
    finally:
        connection.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()