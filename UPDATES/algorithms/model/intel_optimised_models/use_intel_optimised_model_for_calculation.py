import joblib
import numpy as np

# Load the trained models and scaler
pm2_5_model = joblib.load(r'B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\algorithms\model\intel_optimised_models\intel_optimised_models__train=1\Random_Forest_Regression_pm2_5.pkl')
pm10_model = joblib.load(r'B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\algorithms\model\intel_optimised_models\intel_optimised_models__train=1\Random_Forest_Regression_pm10.pkl')
scaler = joblib.load(r'B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\algorithms\model\intel_optimised_models\intel_optimised_models__train=1\scaler.pkl')


# Classification dictionary
CLASS_DICT = {
    1: 'Good',
    2: 'Moderate',
    3: 'Unhealthy for sensitive groups',
    4: 'Unhealthy',
    5: 'Very Unhealthy',
}


# Classification functions
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


# AQI Estimation (Simplified version for illustration purposes)
def intel__calculate_aqi(pm2_5, pm10):
    aqi_pm2_5 = (pm2_5 / 12) * 50 if pm2_5 <= 12 else (pm2_5 / 150.4) * 500
    aqi_pm10 = (pm10 / 54) * 50 if pm10 <= 54 else (pm10 / 354) * 500
    return max(aqi_pm2_5, aqi_pm10)


# Main function with additional calculations
def intel__calculate_air_quality(co, no, no2, o3, so2, nh3, pm2_5_actual, pm10_actual):
    # Prepare input values in the correct shape
    input_values = np.array([[co, no, no2, o3, so2, nh3]])

    # Scale the input values
    input_values_scaled = scaler.transform(input_values)

    # Predict PM2.5 and PM10
    predicted_pm2_5 = pm2_5_model.predict(input_values_scaled)[0]
    predicted_pm10 = pm10_model.predict(input_values_scaled)[0]

    # Classify the predicted PM2.5 and PM10 values
    pm2_5_class = classify_pm2_5(predicted_pm2_5)
    pm10_class = classify_pm10(predicted_pm10)

    # Additional calculations based on actual and predicted values
    pm2_5_absolute_error = abs(pm2_5_actual - predicted_pm2_5)
    pm10_absolute_error = abs(pm10_actual - predicted_pm10)

    pm2_5_relative_error = pm2_5_absolute_error / pm2_5_actual * 100 if pm2_5_actual != 0 else None
    pm10_relative_error = pm10_absolute_error / pm10_actual * 100 if pm10_actual != 0 else None

    # Sum and average pollutant concentration
    pollutant_sum = co + no + no2 + o3 + so2 + nh3
    avg_pollutant_concentration = pollutant_sum / 6

    # Calculate AQI based on predicted values
    predicted_aqi = intel__calculate_aqi(predicted_pm2_5, predicted_pm10)

    # Return the results in a dictionary
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


def intel__calculate_air_quality_manually(co, no, no2, o3, so2, nh3):
    print("Hello from ", intel__calculate_air_quality_manually.__name__)
    # Combine input values into a single array
    input_values = np.array([[co, no, no2, o3, so2, nh3]])

    # Scale the input values
    input_values_scaled = scaler.transform(input_values)

    # Predict PM2.5 and PM10
    predicted_pm2_5 = pm2_5_model.predict(input_values_scaled)[0]
    predicted_pm10 = pm10_model.predict(input_values_scaled)[0]

    # Classify the predicted PM2.5 and PM10 values
    pm2_5_class = classify_pm2_5(predicted_pm2_5)
    pm10_class = classify_pm10(predicted_pm10)

    # Additional calculations: Pollutant sum and average concentration
    pollutant_sum = co + no + no2 + o3 + so2 + nh3
    avg_pollutant_concentration = pollutant_sum / 6

    # Calculate AQI based on predicted values
    predicted_aqi = intel__calculate_aqi(predicted_pm2_5, predicted_pm10)

    # Additional calculations related to the Air Quality Index (AQI)
    co_concentration_ratio = co / avg_pollutant_concentration
    nox_ratio = (no + no2) / avg_pollutant_concentration  # NO and NO2 combined

    # Return the results in a dictionary
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

    print("Hello")

    return results


# # Example usage:
# result = calculate_air_quality_manually(3217.77, 23.00, 189.10, 0.44, 55.34, 41.45)
# print(result)


def intel__calculate_air_quality_manually_final_suggested_verdict(co, no, no2, o3, so2, nh3):
    print("Hello from ", intel__calculate_air_quality_manually.__name__)
    # Combine input values into a single array
    input_values = np.array([[co, no, no2, o3, so2, nh3]])

    # Scale the input values
    input_values_scaled = scaler.transform(input_values)

    # Predict PM2.5 and PM10
    predicted_pm2_5 = pm2_5_model.predict(input_values_scaled)[0]
    predicted_pm10 = pm10_model.predict(input_values_scaled)[0]

    # Classify the predicted PM2.5 and PM10 values
    pm2_5_class = classify_pm2_5(predicted_pm2_5)
    pm10_class = classify_pm10(predicted_pm10)

    # Additional calculations: Pollutant sum and average concentration
    pollutant_sum = co + no + no2 + o3 + so2 + nh3
    avg_pollutant_concentration = pollutant_sum / 6

    # Calculate AQI based on predicted values
    predicted_aqi = intel__calculate_aqi(predicted_pm2_5, predicted_pm10)

    # Additional calculations related to the Air Quality Index (AQI)
    co_concentration_ratio = co / avg_pollutant_concentration
    nox_ratio = (no + no2) / avg_pollutant_concentration  # NO and NO2 combined

    # Return the results in a dictionary
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

    print("Hello")

    return results["Overall AQI Verdict"]


# print(intel__calculate_air_quality_manually_final_suggested_verdict(4000, 30, 45, 61, 44, 22))