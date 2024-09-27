import pandas as pd
import numpy as np


# Function to preprocess the dataset
def preprocess_data(filepath):
    # Load the dataset (replace 'your_dataset.csv' with the path to your actual dataset)
    data = pd.read_csv(filepath)

    # Replace zero values with the minimum value of the respective column (excluding zeros)
    for column in data.columns:
        if data[column].dtype != object:  # Ensure it's a numerical column
            min_nonzero = data[data[column] > 0][column].min()  # Find minimum non-zero value
            data[column] = data[column].replace(0, min_nonzero)  # Replace 0 with the min non-zero value

    # Remove columns
    remove_cols = ['date']
    data.drop(remove_cols, axis=1, inplace=True)

    # Save the preprocessed data to a new CSV file (or overwrite the original if you prefer)
    data.to_csv('preprocessed_data.csv', index=False)

    return data


# Example usage
if __name__ == "__main__":
    # Provide the path to your dataset
    path = r"../../data/delhi_aqi.csv"
    processed_data = preprocess_data(path)
    print("Preprocessing complete. Processed data saved as 'preprocessed_data.csv'.")
