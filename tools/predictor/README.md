# Air Pollution Prediction using Random Forest Regression

## Introduction

This part of the project implements a Machine Learning pipeline designed to predict air pollution levels (specifically **PM2.5 particles**) based on **meteorological data** (such as temperature, wind speed, pressure, and humidity).

The system utilizes a **Random Forest Regressor**, optimized through Time Series Cross-Validation and Grid Search, to model the complex non-linear relationships between weather conditions and air quality.

The pipeline integrates directly with a PostgreSQL database for data retrieval, performs feature engineering to handle temporal cyclicity, and provides a comprehensive statistical evaluation of the model's performance.

## Project Architecture

### **Data Ingestion**
Establishes a connection to a PostgreSQL database to retrieve historical weather and pollution data.

### **Data Preprocessing**
Merges datasets based on timestamps, handles missing values, and prepares the dataset for regression analysis.

### **Feature Engineering**
Transformation of temporal variables (Hour, Month) into cyclical features using sine and cosine functions to preserve temporal continuity. This ensures that the model understands that Hour 23 is proximally close to Hour 0, and December is close to January.

### **Model Training**
Utilization of `RandomForestRegressor` due to its ability to handle non-linear relationships. Hyperparameters (`n_estimators`, `max_depth`) were tuned using `GridSearchCV`.

### **Validation Strategy**
Implementation of `TimeSeriesSplit` to respect the temporal order of observations during cross-validation (first 70% for training, last 30% for testing). This prevents significant data leakage, which occurred in the first version when a random `train_test_split` was used.

### **Evaluation**
The system outputs a detailed statistical report assessing the model's predictive capability including:

- **R² Score:** Represents the proportion of variance in the dependent variable explained by the independent variables.

- **RMSE (Root Mean Squared Error):** The average error size.

- **MAE (Mean Absolute Error):** The average absolute difference between predicted and actual values.

- **Residual Analysis:** Mean and Standard Deviation of residuals to detect bias.

### **Feature Importance**
Following evaluation, the script generates a feature importance report. This identifies which meteorological factors had the most significant impact on the model's decision-making process, providing interpretability to the model.