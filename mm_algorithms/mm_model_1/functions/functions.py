import os

import pandas as pd


def combine_files_and_preprocess():
    # Path to the folder containing CSV files
    folder_path = r"../Multi_Modal_Dataset_1/bzhzr9b64v_1"

    # List of required columns
    required_columns = ["AT", "BP", "PM10", "PM2.5", "RH", "WD", "WS", "NH3", "NO", "NO2", "Ozone",
                        "SO2", "CO", "month", "day"]

    # List to store DataFrames
    dfs = []

    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    # Loop through all files in the folder
    file_count = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_count += 1
            print(f"Processing: {filename}")
            # Read each CSV file into a DataFrame
            df = pd.read_csv(os.path.join(folder_path, filename))

            # Ensure all required columns are present, filling missing ones with NaN
            df = df.reindex(columns=required_columns, fill_value=pd.NA)

            # Append the DataFrame to the list
            dfs.append(df)

    if file_count == 0:
        print(f"No CSV files found in folder: {folder_path}")
        return

    # Combine all DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)

    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv('combined_output_dataset_1.csv', index=False)

    print(f"Files combined successfully! {file_count} files processed.")

    # Preprocess: replace null values with the minimum value in each column
    df = combined_df.copy()

    for column in df.columns:
        if df[column].isnull().any():  # Check if there are null values in the column
            min_value = df[column].min()  # Get the minimum value of the column
            df[column].fillna(min_value, inplace=True)  # Replace nulls with the minimum value

    # Save the preprocessed DataFrame to a new CSV file
    df.to_csv('preprocessed_output_dataset_1.csv', index=False)

    print("Preprocessing complete. Null values replaced with minimum values in each column.")


# combine_files_and_preprocess()


def process_aqi_on_breakpoints():
    file = "preprocessed_output_dataset_1.csv"

    df = pd.read_csv(file)

    # Define the AQI breakpoints for each pollutant
    aqi_breakpoints = {
        'PM2.5': [(0, 12, 0, 50), (12.1, 35.4, 51, 100), (35.5, 55.4, 101, 150), (55.5, 150.4, 151, 200),
                  (150.5, 250.4, 201, 300), (250.5, 500.4, 301, 500)],
        'PM10': [(0, 54, 0, 50), (55, 154, 51, 100), (155, 254, 101, 150), (255, 354, 151, 200), (355, 424, 201, 300),
                 (425, 604, 301, 500)],
        'CO': [(0.0, 4.4, 0, 50), (4.5, 9.4, 51, 100), (9.5, 12.4, 101, 150), (12.5, 15.4, 151, 200),
               (15.5, 30.4, 201, 300), (30.5, 50.4, 301, 500)],
        'SO2': [(0, 35, 0, 50), (36, 75, 51, 100), (76, 185, 101, 150), (186, 304, 151, 200), (305, 604, 201, 300),
                (605, 1004, 301, 500)],
        'NO2': [(0, 53, 0, 50), (54, 100, 51, 100), (101, 360, 101, 150), (361, 649, 151, 200), (650, 1249, 201, 300),
                (1250, 2049, 301, 500)],
        'Ozone': [(0, 54, 0, 50), (55, 70, 51, 100), (71, 85, 101, 150), (86, 105, 151, 200), (106, 200, 201, 300),
                  (201, 500, 301, 500)],
        'NH3': [(0, 200, 0, 50), (201, 400, 51, 100), (401, 800, 101, 150), (801, 1200, 151, 200),
                (1201, 1800, 201, 300), (1801, 2400, 301, 500)]
    }

    # Convert concentration columns to numeric, forcing errors to NaN
    columns_to_convert = ['PM2.5', 'PM10', 'CO', 'SO2', 'NO2', 'Ozone', 'NH3']
    for column in columns_to_convert:
        df[column] = pd.to_numeric(df[column], errors='coerce')

    # Function to calculate AQI for a single pollutant
    def calculate_aqi(pollutant, concentration):
        breakpoints = aqi_breakpoints[pollutant]
        for bp_low, bp_high, aqi_low, aqi_high in breakpoints:
            if bp_low <= concentration <= bp_high:
                return ((aqi_high - aqi_low) / (bp_high - bp_low)) * (concentration - bp_low) + aqi_low
        return None

    # Apply AQI calculations to the respective columns
    df['AQI_PM2.5'] = df['PM2.5'].apply(lambda x: calculate_aqi('PM2.5', x))
    df['AQI_PM10'] = df['PM10'].apply(lambda x: calculate_aqi('PM10', x))
    df['AQI_CO'] = df['CO'].apply(lambda x: calculate_aqi('CO', x))
    df['AQI_SO2'] = df['SO2'].apply(lambda x: calculate_aqi('SO2', x))
    df['AQI_NO2'] = df['NO2'].apply(lambda x: calculate_aqi('NO2', x))
    df['AQI_Ozone'] = df['Ozone'].apply(lambda x: calculate_aqi('Ozone', x))
    df['AQI_NH3'] = df['NH3'].apply(lambda x: calculate_aqi('NH3', x))

    # Calculate the final AQI as the maximum of all individual AQIs
    df['Final_AQI'] = df[['AQI_PM2.5', 'AQI_PM10', 'AQI_CO', 'AQI_SO2', 'AQI_NO2', 'AQI_Ozone', 'AQI_NH3']].max(axis=1)

    # Replace null values with the minimum value for each column
    for column in df.columns:
        if df[column].isnull().any():
            min_value = df[column].min()
            df[column].fillna(min_value, inplace=True)

    # Save the results to a new CSV file
    df.to_csv('preprocessed_output_with_final_aqi_calculated_dataset_1.csv', index=False)

    print("AQI calculation completed. Results saved to 'preprocessed_output_with_final_aqi_calculated.csv'.")


process_aqi_on_breakpoints()
