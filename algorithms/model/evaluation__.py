import joblib
import numpy as np

# Load the trained models
pm2_5_model = joblib.load('models__train=1/Random_Forest_Regression_pm2_5.pkl')
pm10_model = joblib.load('models__train=1/Random_Forest_Regression_pm10.pkl')

# Load the scaler that was used during training
scaler = joblib.load('models__train=1/scaler.pkl')

# Dummy input values (adjust according to your features)
dummy_values = np.array([[3217.77, 23.00, 189.10, 0.44, 55.34, 41.45]])  # Example shape (1, number_of_features)

# Scale the input values using the same scaler as in training
dummy_values_scaled = scaler.transform(dummy_values)

# Predict PM2.5 and PM10 using the models
predicted_pm2_5 = pm2_5_model.predict(dummy_values_scaled)
predicted_pm10 = pm10_model.predict(dummy_values_scaled)

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


# Classify the predicted values
pm2_5_health_class = classify_pm2_5(predicted_pm2_5[0])
pm10_health_class = classify_pm10(predicted_pm10[0])

# Print the predictions and classifications
print(f"Predicted PM2.5: {predicted_pm2_5[0]:.2f}, Health Class: {pm2_5_health_class} -> {CLASS_DICT[pm2_5_health_class]}")
print(f"Predicted PM10: {predicted_pm10[0]:.2f}, Health Class: {pm10_health_class} -> {CLASS_DICT[pm10_health_class]}")
