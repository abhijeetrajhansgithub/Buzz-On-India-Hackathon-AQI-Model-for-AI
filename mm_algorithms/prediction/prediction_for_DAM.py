import os

import pandas as pd
import joblib
import numpy as np
from sklearnex import patch_sklearn
from datetime import datetime, timedelta

patch_sklearn()

# Define model directory
model_dir = rf"B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\mm_algorithms\mm_model_1\models\training\mm_model_1__training___model_training_for_DAM"

# Load the encoder, scaler, and feature names
encoder_file = os.path.join(model_dir, 'encoder.pkl')
scaler_file = os.path.join(model_dir, 'scaler.pkl')
feature_names_file = os.path.join(model_dir, 'feature_names.pkl')

encoder = joblib.load(encoder_file)
scaler = joblib.load(scaler_file) if os.path.exists(scaler_file) else None
feature_names = joblib.load(feature_names_file)


# Function to create a DataFrame for input features
def create_input_dataframe(months, days):
    # Create a DataFrame with month and day
    input_data = pd.DataFrame({
        'month': months,
        'day': days
    })
    return input_data


# Function to predict AQI for the next 7 days
def predict_aqi_for_next_days_DAM(month, start_day):
    months = [month] * 7
    days = [(start_day + i) for i in range(7)]

    # Handle month overflow
    for i in range(len(days)):
        if days[i] > 31:  # Simplistic check, can be refined
            if months[i] in [1, 3, 5, 7, 8, 10, 12]:  # Months with 31 days
                days[i] = 1
                months[i] += 1
            elif months[i] == 2:  # February
                if days[i] > 29:  # Check for leap year
                    days[i] = 1
                    months[i] += 1
            else:  # Months with 30 days
                if days[i] > 30:
                    days[i] = 1
                    months[i] += 1

    # Create input DataFrame
    input_df = create_input_dataframe(months, days)

    # One-hot encode the categorical features
    encoded_input = encoder.transform(input_df).toarray()
    encoded_feature_names = encoder.get_feature_names_out(['month', 'day'])
    encoded_df = pd.DataFrame(encoded_input, columns=encoded_feature_names)

    # Combine with numerical features (if any)
    # If there are no numerical features, you can skip this step
    numerical_df = pd.DataFrame(columns=[name for name in feature_names if name not in encoded_feature_names])
    preprocessed_input = pd.concat([numerical_df, encoded_df], axis=1)

    # Scale the numerical features
    if scaler is not None:
        preprocessed_input[scaler.feature_names_in_] = scaler.transform(preprocessed_input[scaler.feature_names_in_])

    # Load the trained model
    model_file = os.path.join(model_dir,
                              'random_forest_regression_model.pkl')  # Change to your specific model file name
    model = joblib.load(model_file)

    # Make predictions
    predictions = model.predict(preprocessed_input)

    return predictions


# # Example usage: Predict AQI for the next 7 days starting from October 15
# month_input = 10  # October
# start_day_input = 15  # Starting from the 15th day
#
# predicted_aqi = predict_aqi_for_next_days_DAM(month_input, start_day_input)
# print("Predicted AQI for the next 7 days:", predicted_aqi)

def predict_tomorrow_DAM():
    # Get today's date
    today = pd.to_datetime("today")
    tomorrow = today + timedelta(days=1)
    month = tomorrow.month
    day = tomorrow.day

    # Create input DataFrame for tomorrow
    input_df = create_input_dataframe([month], [day])

    # One-hot encode the categorical features
    encoded_input = encoder.transform(input_df).toarray()
    encoded_feature_names = encoder.get_feature_names_out(['month', 'day'])
    encoded_df = pd.DataFrame(encoded_input, columns=encoded_feature_names)

    # Combine with numerical features (if any)
    numerical_df = pd.DataFrame(columns=[name for name in feature_names if name not in encoded_feature_names])
    preprocessed_input = pd.concat([numerical_df, encoded_df], axis=1)

    # Scale the numerical features
    if scaler is not None:
        preprocessed_input[scaler.feature_names_in_] = scaler.transform(preprocessed_input[scaler.feature_names_in_])

    # Load the trained model
    model_file = os.path.join(model_dir,
                              'random_forest_regression_model.pkl')  # Change to your specific model file name
    model = joblib.load(model_file)

    # Make prediction
    predicted_aqi = model.predict(preprocessed_input)

    return predicted_aqi[0]

# Example usage:
# tomorrow_aqi = predict_tomorrow_DAM()
# print("Predicted AQI for tomorrow:", tomorrow_aqi)
