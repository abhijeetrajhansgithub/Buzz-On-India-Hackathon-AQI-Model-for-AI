# Intel Optimization Module
import time

from sklearnex import patch_sklearn
from algorithms.api.openweathermap_api import get_pollution_data, get_weather_info
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor
import joblib
import pandas as pd
import os
from datetime import datetime, timedelta

patch_sklearn()

# Paths for models and preprocessor files
model_dir = r"B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\mm_algorithms\mm_model_1\models\training"
decision_tree_regression_model_path_POWAC = os.path.join(model_dir, "mm_model_1__training___model_training_for_POWAC",
                                                         "decision_tree_regression_model.pkl")
encoder_path = os.path.join(model_dir, "mm_model_1__training___model_training_for_POWAC", "encoder.pkl")
scaler_path = os.path.join(model_dir, "mm_model_1__training___model_training_for_POWAC", "scaler.pkl")
feature_names_path = os.path.join(model_dir, "mm_model_1__training___model_training_for_POWAC", "feature_names.pkl")

decision_tree_regression_model_path_POWAC_ND = os.path.join(model_dir,
                                                            "mm_model_1__training___model_training_for_POWAC_NO_DATE",
                                                            "decision_tree_regression_model.pkl")
preprocessor_path_POWAC_ND = os.path.join(model_dir, "mm_model_1__training___model_training_for_POWAC_NO_DATE",
                                          "preprocessor.pkl")

# Load the necessary preprocessor files
encoder = joblib.load(encoder_path)
scaler = joblib.load(scaler_path)
feature_names = joblib.load(feature_names_path)

# Load the trained model
model = joblib.load(decision_tree_regression_model_path_POWAC)

# print("Feature Names Loaded:", feature_names)
# time.sleep(30)


# Prediction function
def multimodal_model_1__decision_tree__calculate_air_quality__POWAC(model_, encoder_, scaler_, feature_names_):
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
# predicted_aqi = multimodal_model_1__decision_tree__calculate_air_quality__POWAC(model, encoder, scaler, feature_names)


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


def multimodal_model_1__decision_tree__calculate_air_quality__POWAC_ND(model_path, preprocessor):
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


# predicted_aqi_nd = multimodal_model_1__decision_tree__calculate_air_quality__POWAC_ND(
#     decision_tree_regression_model_path_POWAC_ND, preprocessor_POWAC_ND)


def get_multimodal_model_1__decision_tree__calculate_air_quality__POWAC_ND():
    return multimodal_model_1__decision_tree__calculate_air_quality__POWAC_ND(
        decision_tree_regression_model_path_POWAC_ND, preprocessor_POWAC_ND)


def get_multimodal_model_1__decision_tree__calculate_air_quality__POWAC():
    return multimodal_model_1__decision_tree__calculate_air_quality__POWAC(model, encoder, scaler, feature_names)


##################################################################################################################
####################################################################################################################
####################################################################################################################

def predict_aqi_next_seven_days():
    from algorithms.api.openweathermap_api import get_pollution_data, get_weather_info

    # Fetch historical data
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

    df = pd.DataFrame(input_data)

    # Prepare the features
    if 'month' in df.columns and 'day' in df.columns:
        # One-hot encode 'month' and 'day'
        month_day_encoded = encoder.transform(df[['month', 'day']]).toarray()

        # Create new DataFrame for the encoded features
        encoded_columns = [f'month_{i}.0' for i in range(1, 13)] + [f'day_{i}.0' for i in range(1, 32)]
        encoded_df = pd.DataFrame(month_day_encoded, columns=encoded_columns)

        # Drop original 'month' and 'day' columns and concatenate encoded columns
        X = pd.concat([df.drop(['month', 'day'], axis=1), encoded_df], axis=1)
    else:
        X = df

    # Ensure the DataFrame has the same feature names as the model expects
    X = X.reindex(columns=feature_names, fill_value=0)

    # Scale the data
    X_scaled = scaler.transform(X)

    # Predict AQI for the next 7 days
    predictions = []
    future_dates = [datetime.now() + timedelta(days=i) for i in range(1, 8)]

    for future_date in future_dates:
        # Update the input data for the future day
        future_input_data = {
            'AT': [weather_data['AT']],  # Assuming weather stays the same for simplicity
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
            'month': [future_date.month],
            'day': [future_date.day]
        }

        future_df = pd.DataFrame(future_input_data)

        # One-hot encode categorical features for the future date
        future_encoded = encoder.transform(future_df[['month', 'day']]).toarray()
        future_encoded_df = pd.DataFrame(future_encoded, columns=encoded_columns)

        # Drop 'month' and 'day' and concatenate encoded features
        X_future = pd.concat([future_df.drop(['month', 'day'], axis=1), future_encoded_df], axis=1)

        # Ensure the future DataFrame has the same feature names
        X_future = X_future.reindex(columns=feature_names, fill_value=0)

        # Scale the future input
        X_future_scaled = scaler.transform(X_future)

        # Predict AQI
        predicted_aqi = model.predict(X_future_scaled)
        predictions.append((future_date, predicted_aqi[0]))

    return predictions

#
# print("\n\n\nHERE\n\n\n")
# # Example usage
# predicted_aqi = predict_aqi_next_seven_days()
# for date, aqi in predicted_aqi:
#     print(f"Date: {date.strftime('%Y-%m-%d')}, Predicted AQI: {aqi:.2f}")
