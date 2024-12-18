import os
import pandas as pd
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Configure logging with log rotation
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("logs/combine_historical_data.log", maxBytes=5_000_000, backupCount=3),
        logging.StreamHandler()
    ]
)

# Define directories for historical data and output
HISTORICAL_DATA_DIR = "data/crypto/historical_crypto_data"
COMBINED_DATA_DIR = os.path.join(HISTORICAL_DATA_DIR, "combined")
os.makedirs(COMBINED_DATA_DIR, exist_ok=True)

# Mapping of folder names to symbols
# Dynamically generate symbol map from folder names
symbol_map = {folder.lower(): folder.upper() for folder in os.listdir(HISTORICAL_DATA_DIR) if os.path.isdir(os.path.join(HISTORICAL_DATA_DIR, folder))}

# Initialize an empty list to store each file's data
all_data = []

def process_file(filepath, symbol):
    """Processes an individual CSV file by dropping unnecessary columns, adding the Symbol column, and renaming columns."""
    try:
        df = pd.read_csv(filepath)
        
        # Drop Volume and Market Cap columns if they exist
        df = df.drop(columns=["Volume", "Market Cap"], errors='ignore')
        
        # Rename columns to match the desired format
        df = df.rename(columns={"Start": "Date", "Open": "Open", "High": "High", "Low": "Low", "Close": "Close"})
        
        # Convert Date column to the standard format if needed
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce').dt.strftime("%Y-%m-%d %H:%M:%S")
        
        # Add the Symbol column
        df["Symbol"] = symbol
        
        # Select only the columns needed in the desired order
        df = df[["Date", "Symbol", "Open", "High", "Low", "Close"]]
        
        return df
    except Exception as e:
        logging.error(f"Error processing file {filepath}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if an error occurs

# Iterate over each folder in the historical data directory
for folder_name in os.listdir(HISTORICAL_DATA_DIR):
    folder_path = os.path.join(HISTORICAL_DATA_DIR, folder_name)
    
    # Check if it's a directory and has a corresponding symbol
    if os.path.isdir(folder_path) and folder_name.lower() in symbol_map:
        symbol = symbol_map[folder_name.lower()]
        logging.info(f"Processing folder {folder_name} for symbol {symbol}")
        
        # Find all CSV files in this folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                logging.info(f"Processing file {file_path}")
                # Process the file and append its data to the list
                df = process_file(file_path, symbol)
                if not df.empty:
                    all_data.append(df)

# Concatenate all dataframes in the list into a single dataframe
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Remove duplicates
    combined_df = combined_df.drop_duplicates()
    
    # Log final data summary
    logging.info(f"Total rows in combined data: {len(combined_df)}")
    logging.info(f"Sample rows:\n{combined_df.head()}")

    # Save the combined data to a CSV file
    combined_output_path = os.path.join(COMBINED_DATA_DIR, "combined_historical_data.csv")
    combined_df.to_csv(combined_output_path, index=False)
    logging.info(f"Combined historical data saved to {combined_output_path}")
else:
    logging.warning("No data to combine. Please check the input folders.")
