# AirPollutionPredictor

This project has been developed by Piotr Jurczyk, Tomasz Żochowski and Jan Wyrzykowski during class Infrastructure for Data Science: From UNIX to Containers. Our goal was to create an infrastructure that allows to conduct a Data Science project using various tools, such as Unix tools, PostgreSQL and more.

## Setup

There are a few actions needed to set up the project after cloning this repository. The detailed instructions are listed below.

### 1. Virtual environment with `uv`

The virtual environment is essential for executing Python scripts. To set it up, install `uv` first. There are a few installation options, two of which are listed below. The first one requires `pip` and the other one uses `curl`. 

```bash
pip install uv 
# or
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then, install the virtual environment using `uv`:

```
uv sync
```

### PostgreSQL

PostgreSQL is required to store data on which predictions run. In order to set up the database, install PostgreSQL on the machine by running the following command:

```
apt install postgresql
```

After that, execute SQL script `tools/database_setup.sql` in order to create the database, the user, and tables. Prepending the command with `sudo -u postgres` may be required to access PostgreSQL.

```
psql -f tools/database_setup.sql
```

## Cron

WIP

## Project structure

```
.
├── archive                 # no longer used
│   ├── data
│   ├── notebooks
│   │   ├── FirstLook.ipynb
│   │   ├── world_weather_online.ipynb
├── baseline_predictor      # prediction models
│   ├── smog_predictor.ipynb
│   ├── smog_predictor.py
│   ├── smog_predictor2.py
├── log                     # logs created during app runtime
│   ├── download.log
│   ├── prediction.log
|   ├── prediction2.log
│   ├── runtime.log
├── tools                   # scripts for various tasks
│   ├── data_retrieval
│   │   ├── pollution_data_retrieval.sh
│   │   ├── weather_data_retrieval.sh
│   ├── psql
│   │   ├── database_setup.sql
│   ├── python
│   │   ├── downloads.py
│   │   ├── import_historic_data.py
├── .gitignore
├── .python-version
├── uv.lock
├── README.md
├── pyproject.toml
```

