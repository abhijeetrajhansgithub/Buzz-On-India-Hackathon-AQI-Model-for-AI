import joblib
import numpy as np
import time  # Import time module to measure execution time

# Load the trained models and scaler
pm2_5_model = joblib.load(
    r'B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\algorithms\model\models__train=1\Random_Forest_Regression_pm2_5.pkl')
pm10_model = joblib.load(
    r'B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\algorithms\model\models__train=1\Random_Forest_Regression_pm10.pkl')
scaler = joblib.load(
    r'B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\algorithms\model\models__train=1\scaler.pkl')

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
def calculate_aqi(pm2_5, pm10):
    aqi_pm2_5 = (pm2_5 / 12) * 50 if pm2_5 <= 12 else (pm2_5 / 150.4) * 500
    aqi_pm10 = (pm10 / 54) * 50 if pm10 <= 54 else (pm10 / 354) * 500
    return max(aqi_pm2_5, aqi_pm10)


# Main function with additional calculations
def calculate_air_quality_manually_final_suggested_verdict(co, no, no2, o3, so2, nh3):
    start_time = time.time()  # Start timing

    print("Hello from ", calculate_air_quality_manually_final_suggested_verdict.__name__)
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
    predicted_aqi = calculate_aqi(predicted_pm2_5, predicted_pm10)

    # Additional calculations related to the Air Quality Index (AQI)
    co_concentration_ratio = co / avg_pollutant_concentration
    nox_ratio = (no + no2) / avg_pollutant_concentration  # NO and NO2 combined

    # End timing
    end_time = time.time()

    # Calculate and store the time taken
    time_taken = end_time - start_time
    print(f"Time taken to execute the code: {time_taken:.4f} seconds")

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

    time_taken_dict = {
        "Without Intel Optimization Module": time_taken
    }

    return time_taken_dict


# Example usage with timing
if __name__ == "__main__":
    co = 3217.77
    no = 23.00
    no2 = 189.10
    o3 = 0.44
    so2 = 55.34
    nh3 = 41.45

    start_time = time.time()  # Start timing
    result = calculate_air_quality_manually_final_suggested_verdict(co, no, no2, o3, so2, nh3)
    end_time = time.time()  # End timing

    execution_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Time taken to execute the code: {execution_time:.4f} seconds")
