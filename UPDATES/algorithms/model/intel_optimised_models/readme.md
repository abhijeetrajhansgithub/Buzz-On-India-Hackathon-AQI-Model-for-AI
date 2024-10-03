# Intel Optimization for Air Quality Prediction

## Overview
This project leverages Intel’s scikit-learn optimization (`sklearnex`) to accelerate machine learning model performance for predicting air quality (PM2.5 and PM10 levels). The integration of Intel's optimized modules ensures faster computations for large-scale datasets.

## Key Steps

### 1. Intel Optimization with `sklearnex`
Intel's `sklearnex` module is imported to patch and optimize the scikit-learn library for improved speed.

```python
from sklearnex import patch_sklearn
patch_sklearn()
```

### 2. Data Loading and Preprocessing
- Load preprocessed dataset: `preprocessed_data.csv`.
- Features (`X`) and target variables (`y_pm2_5`, `y_pm10`) are defined.
- Split the dataset into training and testing sets.
- Standardize features using `StandardScaler`.

### 3. Model Initialization and Training
A variety of regression models are initialized, including:
- Intel-optimized **Linear Regression**.
- Standard models: **Decision Tree**, **Random Forest**, **SVR**, **MLP**, and **Gradient Boosting**.

Each model is trained separately for predicting both `pm2_5` and `pm10` values.

### 4. Model Evaluation and Saving
For each model:
- Evaluate performance using RMSE and R² metrics.
- Save the trained model and scaler using `joblib`.

### Results are printed and models are saved in `./intel_optimised_models__train=1/`.

