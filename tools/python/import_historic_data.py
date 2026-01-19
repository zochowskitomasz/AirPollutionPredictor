from  datetime import datetime, timedelta
import subprocess
import psycopg2

def main():
    years = [2026]
    daysbase = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
    months = daysbase + [i for i in range(10,13)] 

    trzyje = ["01", "03", "05", "07", "08", 10, 12]
    
    fir = "01"
    
    for year in years:
        for month in months:
            if month != "02":
                if month in trzyje:
                    las = "31"
                else:
                    las = "30"
            elif year != 2024:
                las = "28"
            else:
                las = "29"

            print("downloading")
            start = f"{year}-{month}-{fir}"
            end = f"{year}-{month}-{las}"

            subprocess.call(["/home/zochowski/AirPollutionPredictor/tools/data_retrieval/weather_data_retrieval.sh", str(start), str(end), "/tmp/weathert.csv"])
            subprocess.call(["/home/zochowski/AirPollutionPredictor/tools/data_retrieval/pollution_data_retrieval.sh", str(start), str(end), "/tmp/pollutiont.csv"])
            
            connection = psycopg2.connect(database="air_pollution", user="airflow", password="airflow", host="localhost", port="5432")

            cursor = connection.cursor()


            print("attempting...")
            with open("/tmp/weathert.csv", "r") as f:
                cursor.copy_expert(sql="COPY wTEST(time, temperature_2m, relative_humidity_2m, dew_point_2m, apparent_temperature, wind_speed_10m, wind_speed_100m, surface_pressure, cloud_cover, rain, snowfall) FROM STDIN DELIMITER AS ',' CSV HEADER", file=f)
            with open("/tmp/pollutiont.csv", "r") as f:
                cursor.copy_expert(sql="COPY pTEST(time, c6h6, co, no, no2, nox, pm10, pm25) FROM STDIN DELIMITER AS ',' CSV HEADER", file=f)

            connection.commit()
            connection.close()
            print("done!")

    print("all done!!!!")

if __name__ == "__main__":
    main()

