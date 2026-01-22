# Project structure

This document describes in detail the structure of the project &ndash; hardware, infrastructure, scripts, database and job scheduling.

## Hardware and infrastructure

{hardware}

The design of our project is presented in the picture below.

![Project infrastructure presented in a diagram with five blocks. Smog data API and Weather data API blocks have arrows pointing to Logs and Postgres Database blocks. Postgres Database block points to Python prediction model block, which in turn points to Logs block. APIs and Python blocks are in a group captioned as Cron.](img/infrastructure.png)

Details regarding each component of this diagram are described below, in next sections.

## Data retrieval

One of the core elements of any data science project is collecting data. To showcase the possibilities of our system, we made sure to find data sources which allow to collect historical as well as recent data.

### Data sources

It turned out that fulfilling our goals required two sources of data &ndash; one for [weather](https://open-meteo.com/en/docs/historical-weather-api) and one for [pollution](https://api.gios.gov.pl/pjp-api/swagger-ui/index.html). These two APIs return very different data structures, which forced us to create a different script for each one.

### Data collection scripts

Data retrieval is handled by two shell scripts: `tools/data_retrieval/weather_data_retrieval.sh` and `tools/data_retrieval/pollution_data_retrieval.sh`. They both work in a similar way &ndash; they take three arguments: start date, end date (inclusive) and output file path. Below is a list of steps they perform:

1. Verify access to the log file and the number of arguments.
2. Query the API.
3. Extract data columns from the response.
   - In case of pollution data, this step is more complicated. Each columns requires a different API query.
4. Join the columns and write the result into the target `.csv` file, adding the header line at the start.

> [!NOTE]
> In case of the weather data script, geographic location is written directly in the API query, whereas in case of the pollution data script, the list of sensors from a chosen location is listed. If you want to use this project for a different region, make sure to change accordingly.

Both scripts write their logs to `log/runtime.log`.

### Master scripts

There is a Python script called `tools/python/downloads.py` which is used for periodical data download. It takes the date 7 days back from the date of execution (to ensure that the data from that date is available in the API) and runs data retrieval scripts listed above for that day, saving the results to directory `/tmp`. Then it connects to the PostgreSQL database and uploads collected data.

A similar task is achieved by the `tools/python/import_historic_data.py` script, although its focus is to &ndash; *nomen omen* &ndash; import historic data. More specifically, it pulls the data from years 2023-2025 in monthly intervals; this makes for a reasonable execution time of weather and pollution data retrieval scripts.

## Database

The `README.md` file specifies how to set up the PostgreSQL database required for storing the data. Below are the details of the database's usage.

### Database content

For this project, database with a name `air_pollution` is set up. It is then populated with two tables: `weather` and `pollution`. Although the names of these tables are self-explanatory, it may be worth listing their columns.

Table `weather` has following columns:
- time,
- temperature_2m,
- relative_humidity_2m,
- dew_point_2m,
- apparent_temperature,
- wind_speed_10m,
- wind_speed_100m,
- surface_pressure,
- cloud_cover,
- rain,
- snowfall.

Table `pollution` has following columns:
- time,
- c6h6,
- co,
- no,
- no2,
- nox,
- pm10,
- pm25.

### User and access

Since connecting to the database is required to write as well as read data, a special user `airflow` with password `airflow` was created (the choice of the username has historical reasons). This user is granted all privileges to the database `air_pollution`.

> [!CAUTION]
> This poses a serious security risk if used in an exposed system. Make sure to change the username and/or password in the database (in `tools/psql/database_setup.sql` script or directly) as well as in scripts located in `tools/predictor` and `tools/python` directories.

## Analysis

The goal of this project was to analyze acquired data &ndash; namely, model the level of PM2.5 pollution based on weather conditions. We go through tools used for that goal below.

### Exploratory Data Analysis

There are two main scripts which are used for EDA in out project. The first one, `tools/python/statistics.py`, calculates various statistics on data to get more insight into it. The second one, `tools/python/plotter.py`, draws time series of some features and saves plots to `tools/python/plots` directory. 

These scripts use data from the database by connecting to it. Additionally, Python libraries are used to perform the analyses.

### Model

The main model we used in the project is located in the `tools/predictor` directory. The detailed description is located in the [model doc file](model.md) as well as a [README file](../tools/predictor/README.md) located in the `tools/predictor` directory. This script also connects to the database to query relevant data.

## Job scheduling

To automate the implemented workflow, `cron` is being used. It performs two tasks daily: data retrieval and prediction.

### Data retrieval

Every day (default time specified in setup instructions in [README](../README.md) is 14:00), data retrieval is performed using the `tools/python/downloads.py` script. Any output from the execution of this script is saved to `log/download.log` to allow for troubleshooting if needed.

### Prediction

Like data retrieval, prediction is ran every day (the only difference is time &ndash; it's executed at 15:00 so that new data has definitely been downloaded). The script `tools/predictor/predictor.py` is executed, and the output containing prediction metrics is saved to `log/prediction.log`. 