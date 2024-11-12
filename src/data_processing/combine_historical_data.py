import os
import pandas as pd

# Define directories for historical data and output
HISTORICAL_DATA_DIR = "data/historical_data"
COMBINED_DATA_DIR = os.path.join(HISTORICAL_DATA_DIR, "combined")
os.makedirs(COMBINED_DATA_DIR, exist_ok=True)

# Mapping of folder names to symbols
symbol_map = {
    "btc": "BTC",
    "eth": "ETH",
    "usdt": "USDT",
    "sol": "SOL",
    "bnb": "BNB",
    "usdc": "USDC",
    "xrp": "XRP",
    "doge": "DOGE",
    "ada": "ADA",
    "trx": "TRX"
}

# Initialize an empty list to store each file's data
all_data = []

def process_file(filepath, symbol):
    """Processes an individual CSV file by dropping unnecessary columns, adding the Symbol column, and renaming columns."""
    df = pd.read_csv(filepath)
    
    # Drop Volume and Market Cap columns if they exist
    df = df.drop(columns=["Volume", "Market Cap"], errors='ignore')
    
    # Rename columns to match the desired format
    df = df.rename(columns={"Start": "Date", "Open": "Open", "High": "High", "Low": "Low", "Close": "Close"})
    
    # Convert Date column to the standard format if needed
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # Add the Symbol column
    df["Symbol"] = symbol
    
    # Select only the columns needed in the desired order
    df = df[["Date", "Symbol", "Open", "High", "Low", "Close"]]
    
    return df

# Iterate over each folder in the historical data directory
for folder_name in os.listdir(HISTORICAL_DATA_DIR):
    folder_path = os.path.join(HISTORICAL_DATA_DIR, folder_name)
    
    # Check if it's a directory and has a corresponding symbol
    if os.path.isdir(folder_path) and folder_name in symbol_map:
        symbol = symbol_map[folder_name]
        
        # Find all CSV files in this folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                # Process the file and append its data to the list
                df = process_file(file_path, symbol)
                all_data.append(df)

# Concatenate all dataframes in the list into a single dataframe
combined_df = pd.concat(all_data, ignore_index=True)

# Save the combined data to a CSV file
combined_output_path = os.path.join(COMBINED_DATA_DIR, "combined_historical_data.csv")
combined_df.to_csv(combined_output_path, index=False)
print(f"Combined historical data saved to {combined_output_path}")
