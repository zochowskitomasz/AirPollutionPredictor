CREATE USER airflow WITH PASSWORD 'airflow';
CREATE DATABASE air_pollution;
GRANT ALL PRIVILEGES ON DATABASE air_pollution TO airflow;

\c air_pollution

CREATE TABLE pollution (
    time TIMESTAMP,
    c6h6 DECIMAL,
    co DECIMAL,
    no DECIMAL,
    no2 DECIMAL,
    nox DECIMAL,
    pm10 DECIMAL,
    pm25 DECIMAL
);

CREATE TABLE weather (
    time TIMESTAMP,
    temperature_2m DECIMAL,
    relative_humidity_2m INT,
    dew_point_2m DECIMAL,
    apparent_temperature DECIMAL,
    wind_speed_10m DECIMAL,
    wind_speed_100m DECIMAL,
    surface_pressure DECIMAL,
    cloud_cover INT,
    rain DECIMAL,
    snowfall DECIMAL
);
