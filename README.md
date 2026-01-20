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

### 2. PostgreSQL

PostgreSQL is required to store data on which predictions run. In order to set up the database, install PostgreSQL on the machine by running the following command:

```
apt install postgresql
```

After that, execute SQL script `tools/database_setup.sql` in order to create the database, the user, and tables. Prepending the command with `sudo -u postgres` may be required to access PostgreSQL.

```
psql -f tools/database_setup.sql
```

### 3. Task automation with `cron`

Daily data downloads and predictions are triggered by `cron`. To set it up, execute following commands:

```bash
(crontab -l 2>/dev/null; echo "AIR_POLLUTION_DIR=$(pwd)
0 14 * * * \$AIR_POLLUTION_DIR/.venv/bin/python3 \$AIR_POLLUTION_DIR/tools/python/downloads.py >> \$AIR_POLLUTION_DIR/log/download.log 2>&1
0 15 * * * \$AIR_POLLUTION_DIR/.venv/bin/python3 \$AIR_POLLUTION_DIR/tools/predictor/predictor.py >> \$AIR_POLLUTION_DIR/log/prediction.log 2>&1") | crontab -
```

If necessary, provide different time of execution of these scripts. Be aware, however, that triggering `tools/python/downloads.py` more than once a day will lead to data duplication.

## Project structure

```
.
├── archive                 # no longer used
│   ├── data
│   │   └── ...
│   └── notebooks
│       ├── FirstLook.ipynb
│       └── world_weather_online.ipynb
├── baseline_predictor      # prediction models
│   ├── smog_predictor.ipynb
│   └── smog_predictor.py
├── log                     # logs created during app runtime
│   ├── download.log
│   ├── prediction.log
│   ├── prediction2.log
│   └── runtime.log
├── tools                   # scripts for various tasks
│   ├── data_retrieval
│   │   ├── pollution_data_retrieval.sh
│   │   └── weather_data_retrieval.sh
│   ├── predictor
│   │   ├── README.md
│   │   └── predictor.py
│   ├── psql
│   │   └── database_setup.sql
│   └── python
│       ├── plots
│       │   └── ...
│       ├── downloads.py
│       ├── import_historic_data.py
│       ├── plotter.py
│       └── statistics.py
├── .gitignore
├── .python-version
├── uv.lock
├── README.md
└── pyproject.toml
```

