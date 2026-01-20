import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import os

TEST_SIZE = 75
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
METRICS_PATH = os.path.join(BASE_DIR, "metrics.txt")
CSV_PATH = os.path.join(BASE_DIR, "marszalkowska_log.csv")

df = pd.read_csv(CSV_PATH, sep=';', header=None)
df.columns = ['pi_time', 'meter_time', 'pm25', 'temp', 'press', 'hum', 'wind']

df = df.sort_values(by='pi_time')

train_df = df.iloc[:-TEST_SIZE]
test_df = df.iloc[-TEST_SIZE:]

X_train = train_df[['temp', 'press', 'hum', 'wind']]
y_train = train_df['pm25']

X_test = test_df[['temp', 'press', 'hum', 'wind']]
y_test = test_df['pm25']

rf = RandomForestRegressor(n_estimators=150, max_depth=10, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

with open(METRICS_PATH, "a") as f:
    f.write(f"{pd.Timestamp.now()} Train size: {len(train_df)}, test size: {len(test_df)}, metrics: MSE={mse:.2f}, RMSE={rmse:.4f}, MAE={mae:.2f}, R2={r2:.4f}\n")
