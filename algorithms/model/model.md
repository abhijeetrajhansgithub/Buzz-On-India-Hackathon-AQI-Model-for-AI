This script predicts air quality levels based on common pollutants and classifies them into health categories. It provides useful insights such as error margins, pollutant concentration, and AQI verdicts.

```
# Air Quality Prediction System

This Python script predicts air quality by estimating PM2.5 and PM10 pollutant levels using pre-trained Random Forest models. It further classifies the air quality index (AQI) into different health categories. 

## Code Structure

### Importing Required Libraries
```python
import joblib
import numpy as np
```
- `joblib`: Used for loading the pre-trained models and scaler.
- `numpy`: Utilized for array manipulations.

### Loading Models and Scaler
```python
pm2_5_model = joblib.load(r'path_to/Random_Forest_Regression_pm2_5.pkl')
pm10_model = joblib.load(r'path_to/Random_Forest_Regression_pm10.pkl')
scaler = joblib.load(r'path_to/scaler.pkl')
```
- Loads the pre-trained machine learning models for predicting PM2.5 and PM10 pollutant concentrations.
- `scaler`: Standardizes the input pollutant features.

### Health Class Dictionary
```python
CLASS_DICT = {
    1: 'Good',
    2: 'Moderate',
    3: 'Unhealthy for sensitive groups',
    4: 'Unhealthy',
    5: 'Very Unhealthy',
}
```
- Maps the predicted pollutant concentrations to health categories based on AQI thresholds.

### Classification Functions
#### PM2.5 Classification
```python
def classify_pm2_5(value):
    if value <= 12:
        return 1  # Good
    elif value <= 35.4:
        return 2  # Moderate
    elif value <= 55.4:
        return 3  # Unhealthy for sensitive groups
    elif value <= 150.4:
        return 4  # Unhealthy
    else:
        return 5  # Very Unhealthy
```
- Classifies PM2.5 pollutant concentration into AQI health categories.

#### PM10 Classification
```python
def classify_pm10(value):
    if value <= 54:
        return 1  # Good
    elif value <= 154:
        return 2  # Moderate
    elif value <= 254:
        return 3  # Unhealthy for sensitive groups
    elif value <= 354:
        return 4  # Unhealthy
    else:
        return 5  # Very Unhealthy
```
- Classifies PM10 pollutant concentration into AQI health categories.

### AQI Estimation
```python
def calculate_aqi(pm2_5, pm10):
    aqi_pm2_5 = (pm2_5 / 12) * 50 if pm2_5 <= 12 else (pm2_5 / 150.4) * 500
    aqi_pm10 = (pm10 / 54) * 50 if pm10 <= 54 else (pm10 / 354) * 500
    return max(aqi_pm2_5, aqi_pm10)
```
- Estimates the overall AQI based on predicted PM2.5 and PM10 levels.

### Main Function: Air Quality Prediction
```python
def calculate_air_quality(co, no, no2, o3, so2, nh3, pm2_5_actual, pm10_actual):
    input_values = np.array([[co, no, no2, o3, so2, nh3]])  # Preparing the input
    input_values_scaled = scaler.transform(input_values)  # Scaling the inputs
    
    predicted_pm2_5 = pm2_5_model.predict(input_values_scaled)[0]
    predicted_pm10 = pm10_model.predict(input_values_scaled)[0]

    pm2_5_class = classify_pm2_5(predicted_pm2_5)
    pm10_class = classify_pm10(predicted_pm10)

    pm2_5_absolute_error = abs(pm2_5_actual - predicted_pm2_5)
    pm10_absolute_error = abs(pm10_actual - predicted_pm10)

    pm2_5_relative_error = (pm2_5_absolute_error / pm2_5_actual * 100) if pm2_5_actual != 0 else None
    pm10_relative_error = (pm10_absolute_error / pm10_actual * 100) if pm10_actual != 0 else None

    pollutant_sum = co + no + no2 + o3 + so2 + nh3
    avg_pollutant_concentration = pollutant_sum / 6

    predicted_aqi = calculate_aqi(predicted_pm2_5, predicted_pm10)

    results = {
        'Predicted PM2.5': float(predicted_pm2_5),
        'PM2.5 Health Class': CLASS_DICT[pm2_5_class],
        'Predicted PM10': float(predicted_pm10),
        'PM10 Health Class': CLASS_DICT[pm10_class],
        'Total Pollutants (sum)': pollutant_sum,
        'Average Pollutant Concentration': avg_pollutant_concentration,
        'PM2.5 Absolute Error': float(pm2_5_absolute_error),
        'PM10 Absolute Error': float(pm10_absolute_error),
        'PM2.5 Relative Error (%)': float(pm2_5_relative_error),
        'PM10 Relative Error (%)': float(pm10_relative_error),
        'Predicted AQI': float(predicted_aqi),
        'Actual PM2.5': pm2_5_actual,
        'Actual PM10': pm10_actual,
        'Overall AQI Verdict': CLASS_DICT[pm2_5_class] if predicted_pm2_5 < predicted_pm10 else CLASS_DICT[pm10_class]
    }
    
    return results
```
- **Inputs**: Concentrations of pollutants: `CO, NO, NO2, O3, SO2, NH3`, along with actual PM2.5 and PM10 levels.
- **Processing**:
  1. Input pollutant concentrations are scaled using a pre-trained scaler.
  2. The PM2.5 and PM10 values are predicted using the Random Forest models.
  3. Predicted values are classified into AQI health categories.
  4. Errors between actual and predicted values are calculated (absolute and relative errors).
  5. Pollutant sum and average concentrations are computed.
  6. AQI is estimated based on PM2.5 and PM10 predictions.
- **Output**: A dictionary containing predicted pollutant levels, classification, errors, and AQI verdict.

### Example Usage
```python
result = calculate_air_quality(3217.77, 23.00, 189.10, 0.44, 55.34, 41.45, 12.0, 50.0)
print(result)
```
- Demonstrates how to use the `calculate_air_quality` function to get predictions for PM2.5, PM10, and AQI based on pollutant inputs.

### Function: Manual Air Quality Prediction
```python
def calculate_air_quality_manually(co, no, no2, o3, so2, nh3):
    input_values = np.array([[co, no, no2, o3, so2, nh3]])
    input_values_scaled = scaler.transform(input_values)
    predicted_pm2_5 = pm2_5_model.predict(input_values_scaled)[0]
    predicted_pm10 = pm10_model.predict(input_values_scaled)[0]
    pm2_5_class = classify_pm2_5(predicted_pm2_5)
    pm10_class = classify_pm10(predicted_pm10)
    pollutant_sum = co + no + no2 + o3 + so2 + nh3
    avg_pollutant_concentration = pollutant_sum / 6
    predicted_aqi = calculate_aqi(predicted_pm2_5, predicted_pm10)
    co_concentration_ratio = co / avg_pollutant_concentration
    nox_ratio = (no + no2) / avg_pollutant_concentration

    results = {
        'Predicted PM2.5': float(predicted_pm2_5),
        'PM2.5 Health Class': CLASS_DICT[pm2_5_class],
        'Predicted PM10': float(predicted_pm10),
        'PM10 Health Class': CLASS_DICT[pm10_class],
        'Total Pollutants (sum)': pollutant_sum,
        'Average Pollutant Concentration': avg_pollutant_concentration,
        'Predicted AQI': float(predicted_aqi),
        'CO Concentration Ratio': co_concentration_ratio,
        'NOx (NO and NO2) Ratio': nox_ratio,
        'Overall AQI Verdict': CLASS_DICT[pm2_5_class] if predicted_pm2_5 < predicted_pm10 else CLASS_DICT[pm10_class]
    }

    return results
```
- This function works similarly to the previous one, but also provides additional pollutant ratios, such as the CO concentration ratio and the combined NO and NO2 ratio.
