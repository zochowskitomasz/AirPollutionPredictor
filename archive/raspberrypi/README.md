# Real-Time Data Ingestion and On-Device Training

## Introduction

This part of the project serves as a **Proof of Concept** for using a low-power single-board computer to run the entire project pipeline with lightweight tools.

It demonstrates the ability to perform machine learning tasks independently, including:

1. **Data Ingestion:** Fetching real-time sensor data from external APIs via a shell script.
2. **Local Storage:** Managing datasets on-device in CSV format.
3. **Model Training:** Periodically retraining a Random Forest Regressor on the device to adapt to the latest environmental trends without cloud dependency.

## Project Architecture

The workflow consists of two main scripts:

1. **`smog_log.sh` (Bash):** A data acquisition script that queries the WAQI (World Air Quality Index) API for the Marszałkowska station in Warsaw. It parses the JSON response and appends raw meteorological and pollution data to a local CSV log.
2. **`edge_predictor.py` (Python):** A modeling script that reads the updated log, performs a temporal train/test split, retrains a Random Forest model, and logs performance metrics.

Additionally, a **`meter_stats.py`** script was developed to view basic statistics of acquired data. This script was later adapted for the main server deployment.

## Hardware

**Raspberry Pi Model B Rev 2** running Raspberry Pi OS, a Linux distribution based on Debian. Although it is a 10+ year old device, it successfully handles these basic tasks.

## Automated Execution

For periodical data collection and model retraining (once every hour), we used `cron`.

Due to low power consumption, the device was able to run 24/7 for the last 3 months, saving almost 2000 weather and air pollution data records.

Based on this data, a simple **Random Forest Regressor** with fixed parameters was trained (using `GridSearchCV` proved to be too resource-hungry for this hardware). Due to the limited dataset (only ~3 months of data split into train and test sets), the current model performance is limited, primarily lacking seasonal patterns.
