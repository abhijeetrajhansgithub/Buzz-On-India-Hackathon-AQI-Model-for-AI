# Intel Optimization Module
from sklearnex import patch_sklearn

from algorithms.api.openweathermap_api import get_pollution_data, get_weather_info

patch_sklearn()

import joblib
import pandas as pd
import os
from datetime import datetime

# Paths for models and preprocessor files
model_dir = r"B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\mm_algorithms\mm_model_1\models\training"
random_forest_regression_model_path_POWAC = os.path.join(model_dir, "mm_model_1__training___model_training_for_POWAC",
                                                         "random_forest_regression_model.pkl")
encoder_path = os.path.join(model_dir, "mm_model_1__training___model_training_for_POWAC", "encoder.pkl")
scaler_path = os.path.join(model_dir, "mm_model_1__training___model_training_for_POWAC", "scaler.pkl")
feature_names_path = os.path.join(model_dir, "mm_model_1__training___model_training_for_POWAC", "feature_names.pkl")

random_forest_regression_model_path_POWAC_ND = os.path.join(model_dir,
                                                            "mm_model_1__training___model_training_for_POWAC_NO_DATE",
                                                            "random_forest_regression_model.pkl")
preprocessor_path_POWAC_ND = os.path.join(model_dir, "mm_model_1__training___model_training_for_POWAC_NO_DATE",
                                          "preprocessor.pkl")

# Load the necessary preprocessor files
encoder = joblib.load(encoder_path)
scaler = joblib.load(scaler_path)
feature_names = joblib.load(feature_names_path)

# Load the trained model
model = joblib.load(random_forest_regression_model_path_POWAC)


# Prediction function
def multimodal_model_1__random_forest__calculate_air_quality__POWAC(model_, encoder_, scaler_, feature_names_):
    # Get current pollution and weather data
    pollution_data = get_pollution_data()
    weather_data = get_weather_info()

    # Extract pollution and weather variables
    input_data = {
        'AT': [weather_data['AT']],
        'BP': [weather_data['BP']],
        'PM10': [pollution_data['pm10']],
        'PM2.5': [pollution_data['pm2_5']],
        'RH': [weather_data['RH']],
        'WD': [weather_data['WD']],
        'WS': [weather_data['WS']],
        'NH3': [pollution_data['nh3']],
        'NO': [pollution_data['no']],
        'NO2': [pollution_data['no2']],
        'Ozone': [pollution_data['o3']],
        'SO2': [pollution_data['so2']],
        'CO': [pollution_data['co']],
        'month': [datetime.now().month],
        'day': [datetime.now().day]
    }

    # Convert input data to DataFrame
    input_df = pd.DataFrame(input_data)

    # One-hot encode categorical features
    encoded_categorical_data = encoder_.transform(input_df[['month', 'day']]).toarray()
    encoded_df = pd.DataFrame(encoded_categorical_data, columns=encoder_.get_feature_names_out(['month', 'day']))

    # Combine numerical and encoded categorical data
    numerical_data = input_df[['AT', 'BP', 'PM10', 'PM2.5', 'RH', 'WD', 'WS', 'NH3', 'NO', 'NO2', 'Ozone', 'SO2', 'CO']]
    preprocessed_input = pd.concat([numerical_data, encoded_df], axis=1)

    # print(preprocessed_input.head())

    # print number of columns
    # print("Number of columns: ", len(preprocessed_input.columns))

    # Ensure the columns align with the trained model's input
    preprocessed_input = preprocessed_input.reindex(columns=feature_names_, fill_value=0)

    # Apply scaling to the input data
    input_scaled = scaler_.transform(preprocessed_input)

    # Predict AQI
    try:
        prediction = model_.predict(input_scaled)
        # print(f'Predicted Final AQI: {prediction[0]:.4f}')
        return prediction[0]
    except Exception as e:
        print(f'Error during prediction: {e}')
        return None


# Perform AQI prediction
# predicted_aqi = multimodal_model_1__random_forest__calculate_air_quality__POWAC(model, encoder, scaler, feature_names)


# #################################################################################################################
# #################################################################################################################
# #################################################################################################################

def load_preprocessor(path):
    try:
        return joblib.load(path)
    except Exception as e:
        print(f"Error loading preprocessor from {path}: {e}")
        return None


preprocessor_POWAC_ND = load_preprocessor(preprocessor_path_POWAC_ND)


def multimodal_model_1__random_forest__calculate_air_quality__POWAC_ND(model_path, preprocessor):
    from algorithms.api.openweathermap_api import get_weather_info, get_pollution_data

    # Get pollution data
    pollution_data = get_pollution_data()
    # print("Pollution data: ", pollution_data)

    # Extract pollution variables
    co = pollution_data['co']
    no = pollution_data['no']
    no2 = pollution_data['no2']
    o3 = pollution_data['o3']
    so2 = pollution_data['so2']
    pm2_5_actual = pollution_data['pm2_5']
    pm10_actual = pollution_data['pm10']
    nh3 = pollution_data['nh3']

    # Get weather data
    data = get_weather_info()
    RH = data["RH"]
    WS = data["WS"]
    WD = data["WD"]
    AT = data["AT"]
    BP = data["BP"]

    # Load the model
    try:
        pipeline = joblib.load(model_path)
    except Exception as e:
        print(f"Error loading model from {model_path}: {e}")
        return None

    # Get the current date
    current_date = datetime.now()
    day = current_date.day
    month = current_date.month

    # Prepare the input data for prediction
    input_data = {
        'AT': [AT],
        'BP': [BP],
        'PM10': [pm10_actual],
        'PM2.5': [pm2_5_actual],
        'RH': [RH],
        'WD': [WD],
        'WS': [WS],
        'NH3': [nh3],
        'NO': [no],
        'NO2': [no2],
        'Ozone': [o3],
        'SO2': [so2],
        'CO': [co]
    }

    # Convert to DataFrame
    input_df = pd.DataFrame(input_data)
    # print(input_df.head())
    # print("Number of columns: ", len(input_df.columns))

    # Handle missing values
    input_df = input_df.fillna(method='ffill')

    # Apply the preprocessor
    try:
        input_df_transformed = preprocessor.transform(input_df)
    except Exception as e:
        print(f"Error during preprocessing: {str(e)}")
        return None

    # Make predictions
    try:
        predictions = pipeline.predict(input_df_transformed)
        # print(f'Predicted Final AQI: {predictions[0]:.4f}')
        return predictions[0]  # Return the predicted value
    except Exception as e:
        print(f'Error during prediction: {str(e)}')
        return None


def get_multimodal_model_1__random_forest__calculate_air_quality__POWAC_ND():
    return multimodal_model_1__random_forest__calculate_air_quality__POWAC_ND(random_forest_regression_model_path_POWAC_ND, preprocessor_POWAC_ND)


def get_multimodal_model_1__random_forest__calculate_air_quality__POWAC():
    return multimodal_model_1__random_forest__calculate_air_quality__POWAC(model, encoder, scaler, feature_names)