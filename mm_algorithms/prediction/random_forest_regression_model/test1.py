# Intel Optimization Module
from sklearnex import patch_sklearn

patch_sklearn()

import joblib
from datetime import datetime
import pandas as pd
import os

# Paths for models and preprocessor
model_dir = r"B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\mm_algorithms\mm_model_1\models\training"
random_forest_regression_model_path_POWAC = os.path.join(model_dir, "mm_model_1__training___model_training_for_POWAC", "random_forest_regression_model.pkl")
random_forest_regression_model_path_POWAC_ND = os.path.join(model_dir, "mm_model_1__training___model_training_for_POWAC_NO_DATE", "random_forest_regression_model.pkl")
preprocessor_path_POWAC = os.path.join(model_dir, "mm_model_1__training___model_training_for_POWAC", "preprocessor.pkl")
preprocessor_path_POWAC_ND = os.path.join(model_dir, "mm_model_1__training___model_training_for_POWAC_NO_DATE", "preprocessor.pkl")


# Load the preprocessor
def load_preprocessor(path):
    try:
        return joblib.load(path)
    except Exception as e:
        print(f"Error loading preprocessor from {path}: {e}")
        return None


# Load preprocessors for both models
preprocessor_POWAC = load_preprocessor(preprocessor_path_POWAC)
preprocessor_POWAC_ND = load_preprocessor(preprocessor_path_POWAC_ND)


# Ensure preprocessor is fitted
def check_preprocessor(preprocessor):
    try:
        preprocessor.transform(pd.DataFrame(columns=preprocessor.get_feature_names_out()))
        print("Preprocessor is fitted and ready.")
    except Exception as e:
        print(f"Error: {e}. Ensure your preprocessor is fitted correctly.")


check_preprocessor(preprocessor_POWAC)
check_preprocessor(preprocessor_POWAC_ND)


def predict_aqi(model_path, preprocessor):
    from algorithms.api.openweathermap_api import get_weather_info, get_pollution_data

    # Get pollution data
    pollution_data = get_pollution_data()
    print("Pollution data: ", pollution_data)

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
        'CO': [co],
        'month': [month],  # Categorical feature
        'day': [day]       # Categorical feature
    }

    # Convert to DataFrame
    input_df = pd.DataFrame(input_data)

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
        print(f'Predicted Final AQI: {predictions[0]:.4f}')
        return predictions[0]  # Return the predicted value
    except Exception as e:
        print(f'Error during prediction: {str(e)}')
        return None


# Call the function for both models
predicted_aqi = predict_aqi(random_forest_regression_model_path_POWAC, preprocessor_POWAC)
predicted_aqi_nd = predict_aqi(random_forest_regression_model_path_POWAC_ND, preprocessor_POWAC_ND)
