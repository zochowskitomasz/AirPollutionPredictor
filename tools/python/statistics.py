import numpy as np
import pandas as pd
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


def read_weather_data_from_db(connection):
    cursor = connection.cursor()
    query = """
    SELECT time, temperature_2m::float as temperature_2m, relative_humidity_2m, surface_pressure, wind_speed_10m::float as wind_speed_10m 
    FROM weather
    ORDER BY time
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    
    df = pd.DataFrame(rows, columns=['time', 'temperature_2m', 'relative_humidity_2m', 'surface_pressure', 'wind_speed_10m'])
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df.dropna(inplace=True)
    return df


def read_smog_data_from_db(connection):
    cursor = connection.cursor()
    query = """
    SELECT time, pm25::float as pm25 
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



def main():
    print("Connecting to PostgreSQL database...")
    connection = database_connection()

    try:
        print("Reading weather data from database...")
        weather = read_weather_data_from_db(connection)
        pm25 = read_smog_data_from_db(connection)
        df = pd.merge(weather, pm25, on='time', how='inner')
        df = df.sort_values(by='time')

        stats = df.describe()
        print("\nWeather data statistics:")

        print(f"Total number of logs saved: {len(df)}")
        print(f"First log on {df['time'].min()}")
        print(f"Last log on {df['time'].max()}")
        print()
        print(stats)
        print()

        metrics = ['temperature_2m', 'surface_pressure', 'relative_humidity_2m', 'wind_speed_10m', 'pm25']

        for m in metrics:
            max_val = df[m].max()
            min_val = df[m].min()

            max_day = df[df[m] == max_val]['time'].dt.strftime('%Y-%m-%d').unique()
            min_day = df[df[m] == min_val]['time'].dt.strftime('%Y-%m-%d').unique()
            print(f"{m.upper()} min: {min_val} on {min_day} max: {max_val} on {max_day}")
            print()

    finally:
        connection.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()

