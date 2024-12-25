import json
import csv
import os
from datetime import datetime

# Define the base directory for daily data storage
BASE_DATA_DIR = "data/crypto/daily_crypto_data"

# Get the current date in YYYY-MM-DD format
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

def process_daily_data_to_historical(daily_data):
    """
    Converts daily crypto data to a format that matches historical data.
    """
    processed_data = []
    
    for entry in daily_data['symbols']:
        symbol = entry['symbol']
        date_str = entry['date']
        close_price = float(entry['last'])
        high_price = float(entry['highest'])
        low_price = float(entry['lowest'])
        
        # Approximate open price based on daily change
        open_price = close_price * (1 - (float(entry['daily_change_percentage']) / 100))
        
        processed_data.append({
            "Date": date_str,
            "Symbol": symbol,
            "Open": open_price,
            "High": high_price,
            "Low": low_price,
            "Close": close_price
        })
    
    return processed_data

def process_current_date_folder():
    """
    Processes only the folder corresponding to the current date.
    """
    date_folder_path = os.path.join(BASE_DATA_DIR, CURRENT_DATE)
    raw_folder_path = os.path.join(date_folder_path, "raw")
    processed_folder_path = os.path.join(date_folder_path, "processed_csv")
    
    # Ensure the date folder and subfolders exist
    if os.path.isdir(raw_folder_path):
        os.makedirs(processed_folder_path, exist_ok=True)

        # Assume the raw folder contains a single JSON file with daily data
        raw_file_path = os.path.join(raw_folder_path, "crypto_data.json")
        processed_file_path = os.path.join(processed_folder_path, "processed_crypto_data.csv")

        # Load raw JSON data
        if os.path.exists(raw_file_path):
            with open(raw_file_path, "r") as f:
                daily_data = json.load(f)

            # Process data
            processed_data = process_daily_data_to_historical(daily_data)

            # Save processed data to CSV
            with open(processed_file_path, "w", newline='') as csvfile:
                fieldnames = ["Date", "Symbol", "Open", "High", "Low", "Close"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for data in processed_data:
                    writer.writerow(data)

            print(f"Processed data saved to {processed_file_path}")
        else:
            print(f"No crypto_data.json found in {raw_folder_path}")
    else:
        print(f"No folder found for the current date: {CURRENT_DATE}")

# Run the processing function
if __name__ == "__main__":
    process_current_date_folder()
