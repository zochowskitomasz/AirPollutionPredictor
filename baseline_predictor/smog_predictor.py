from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor

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

def prepare_data(weather_path, smog_path):
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
    mse = round(mean_squared_error(y_test, y_pred),2)
    rmse = round(np.sqrt(mean_squared_error(y_test, y_pred)),2)
    mae = round(mean_absolute_error(y_test, y_pred),2)
    r2 = round(r2_score(y_test, y_pred),2)
    results = {'MSE': mse, 'RMSE': rmse, 'MAE': mae, 'R2': r2}
    return results

def print_results(results, model_name):
    print(f"Results for {model_name} model:")
    print(f"MSE: {results['MSE']}, RMSE: {results['RMSE']}, MAE: {results['MAE']}, R2: {results['R2']}.")


def main():
    print("Preparing data...")
    X_train, X_test, y_train, y_test = prepare_data(
        '../downloading_data/warsaw_weather_2025_hourly.csv',
        '../downloading_data/gios-pjp-data.csv'
    )
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


if __name__ == "__main__":
    main()