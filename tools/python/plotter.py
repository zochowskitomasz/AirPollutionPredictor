import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import os


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
        print("Reading data from database...")
        weather = read_weather_data_from_db(connection)
        pm25 = read_smog_data_from_db(connection)

        df = pd.merge(weather, pm25, on='time', how='inner')
        df = df.sort_values(by='time')

        window_size = 168  # 7 * 24

        metrics = ['temperature_2m', 'relative_humidity_2m', 'surface_pressure', 'wind_speed_10m', 'pm25']

        for col in metrics:
            df[f'{col}_smooth'] = df[col].rolling(window=window_size, center=True).mean()

        tasks = [
            {
                'filename': 'plots/chart_1_temperature.png',
                'title': 'Temperature (2m) - 7 Day Trend',
                'primary': {'col': 'temperature_2m', 'color': "#3363FF", 'ylabel': 'Temperature (°C)'}
            },
            {
                'filename': 'plots/chart_2_humidity.png',
                'title': 'Relative Humidity - 7 Day Trend',
                'primary': {'col': 'relative_humidity_2m', 'color': "#FF3333", 'ylabel': 'Humidity (%)'}
            },
            {
                'filename': 'plots/chart_3_pressure.png',
                'title': 'Surface Pressure - 7 Day Trend',
                'primary': {'col': 'surface_pressure', 'color': '#8E44AD', 'ylabel': 'Pressure (hPa)'}
            },
            {
                'filename': 'plots/chart_4_wind.png',
                'title': 'Wind Speed - 7 Day Trend',
                'primary': {'col': 'wind_speed_10m', 'color': '#27AE60', 'ylabel': 'Wind Speed (m/s)'}
            },
            {
                'filename': 'plots/chart_5_combined_pm25_temp.png',
                'title': 'PM2.5 and Temperature - Correlation',
                'primary': {'col': 'pm25', 'color': 'tab:orange', 'ylabel': 'PM2.5'},
                'secondary': {'col': 'temperature_2m', 'color': "#3363FF", 'ylabel': 'Temperature (°C)'}
            },
            {
                'filename': 'plots/chart_6_combined_pm25_wind.png',
                'title': 'PM2.5 and Wind - Correlation',
                'primary': {'col': 'pm25', 'color': 'tab:orange', 'ylabel': 'PM2.5'},
                'secondary': {'col': 'wind_speed_10m', 'color': '#27AE60', 'ylabel': 'Wind (m/s)'}
            }
        ]

        os.makedirs('plots', exist_ok=True)

        plt.style.use('seaborn-v0_8-darkgrid')

        for task in tasks:
            fig, ax1 = plt.subplots(figsize=(12, 8))
            
            p_conf = task['primary']
            ax1.plot(df['time'], df[p_conf['col']], color=p_conf['color'], linewidth=1, alpha=0.15)
            ax1.plot(df['time'], df[f"{p_conf['col']}_smooth"], color=p_conf['color'], linewidth=3, label=p_conf['ylabel'])
            
            ax1.set_xlabel('Time', fontsize=14)
            ax1.set_ylabel(p_conf['ylabel'], color=p_conf['color'], fontsize=14, fontweight='bold')
            ax1.tick_params(axis='y', labelcolor=p_conf['color'])
            

            if 'secondary' in task:
                s_conf = task['secondary']
                ax2 = ax1.twinx()
                
                ax2.plot(df['time'], df[s_conf['col']], color=s_conf['color'], linewidth=1, alpha=0.15)
                ax2.plot(df['time'], df[f"{s_conf['col']}_smooth"], color=s_conf['color'], linewidth=3)
                
                ax2.set_ylabel(s_conf['ylabel'], color=s_conf['color'], fontsize=14, fontweight='bold')
                ax2.tick_params(axis='y', labelcolor=s_conf['color'])
                ax2.grid(False) #
            

            ax1.grid(True, alpha=0.2) 
            plt.title(task['title'], fontsize=18, fontweight='bold', pad=20)
            
            fig.autofmt_xdate()
            
            plt.savefig(task['filename'], dpi=300, bbox_inches='tight')
            #plt.show()
            plt.close() 
        print("All charts have been generated and saved.")

    finally:
        connection.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()

