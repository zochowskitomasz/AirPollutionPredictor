import numpy as np
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "marszalkowska_log.csv")
STATS_PATH = os.path.join(BASE_DIR, "statistics.txt")

df = pd.read_csv(CSV_PATH, sep=';', header=None)
df.columns = ['pi_time', 'meter_time', 'pm25', 'temp', 'press', 'hum', 'wind']
df['pi_time'] = pd.to_datetime(df['pi_time'], errors='coerce')
metrics = ['pm25', 'temp', 'press', 'hum', 'wind']

stats = df[metrics].describe()

with open(STATS_PATH, 'w', encoding='utf-8') as f:
    print("AQICN meter stats for Marszalkowska, Warsaw, Poland", file=f)
    print(f"Total number of logs saved: {len(df)}", file=f)
    print(f"First log on {df['pi_time'].min()}", file=f)
    print(f"Last log on {df['pi_time'].max()}", file=f)
    print(file=f)
    print(stats, file=f)
    print(file=f)

    for m in metrics:
        max_val = df[m].max()
        min_val = df[m].min()

        max_day = df[df[m] == max_val]['pi_time'].dt.strftime('%Y-%m-%d').unique()
        min_day = df[df[m] == min_val]['pi_time'].dt.strftime('%Y-%m-%d').unique()
        
        print(f"{m.upper()} min: {min_val} on {min_day} max: {max_val} on {max_day}", file=f)
        print(file=f)
