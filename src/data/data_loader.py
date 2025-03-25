import os
import pandas as pd

def load_data(file_path):
    """
    Load data from a CSV file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded from {file_path}.")
        return data
    except Exception as e:
        raise Exception(f"Error reading {file_path}: {e}")

def preprocess_data(data):
    """
    Preprocess the data by removing duplicates, handling missing values, and standardizing column names.
    """
    if data is None or data.empty:
        raise ValueError("Data is empty or None.")
    
    # Remove duplicate rows
    data = data.drop_duplicates()
    
    # Fill missing values with empty strings (adjust as necessary)
    data = data.fillna("")
    
    # Convert column names to lowercase for consistency
    data.columns = [col.lower() for col in data.columns]
    
    return data

def save_data(data, output_path):
    """
    Save the processed data to a CSV file.
    """
    try:
        data.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}.")
    except Exception as e:
        raise Exception(f"Error saving data to {output_path}: {e}")

if __name__ == "__main__":
    # Example usage:
    input_file = "data/raw_data.csv"      # Adjust path as needed
    output_file = "data/processed_data.csv" # Adjust path as needed
    
    try:
        raw_data = load_data(input_file)
        processed_data = preprocess_data(raw_data)
        save_data(processed_data, output_file)
    except Exception as err:
        print(err)