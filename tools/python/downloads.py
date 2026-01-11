from  datetime import datetime, timedelta
import subprocess
import psycopg2

def main():
    date = (datetime.now() - timedelta(days=7)).date()
    subprocess.call(["/home/zochowski/AirPollutionPredictor/tools/data_retrieval/weather_data_retrieval.sh", str(date), str(date), "/tmp/weather.csv"])
    subprocess.call(["/home/zochowski/AirPollutionPredictor/tools/data_retrieval/pollution_data_retrieval.sh", str(date), str(date), "/tmp/pollution.csv"])
    
    connection = psycopg2.connect(database="air_pollution", user="airflow", password="airflow", host="localhost", port="5432")

    cursor = connection.cursor()
    #cursor.execute("COPY pollution(time, c6h6, co, no, no2, nox, pm10, pm25) FROM '/tmp/pollution.csv' delimiter ',' CSV HEADER;")
    #cursor.execute("COPY weather(time, temperature_2m, relative_humidity_2m, dew_point_2m, apparent_temperature, wind_speed_10m, wind_speed_100m, surface_pressure, cloud_cover, rain, snowfall) FROM '/tmp/weather.csv' delimiter ',' CSV HEADER;")
    
    #with open("/tmp/weather.csv", "r") as f:
    #    with cursor.copy("copy weather(time, temperature_2m, relative_humidity_2m, dew_point_2m, apparent_temperature, wind_speed_10m, wind_speed_100m, surface_pressure, cloud_cover, rain, snowfall) from stdin") as copy:
    #        for row in f.read().split("\n"):
    #            copy.write_row(row)

    with open("/tmp/weather.csv", "r") as f:
        cursor.copy_expert(sql="COPY weather(time, temperature_2m, relative_humidity_2m, dew_point_2m, apparent_temperature, wind_speed_10m, wind_speed_100m, surface_pressure, cloud_cover, rain, snowfall) FROM STDIN DELIMITER AS ',' CSV HEADER", file=f)
    with open("/tmp/pollution.csv", "r") as f:
        cursor.copy_expert(sql="COPY pollution(time, c6h6, co, no, no2, nox, pm10, pm25) FROM STDIN DELIMITER AS ',' CSV HEADER", file=f)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()

