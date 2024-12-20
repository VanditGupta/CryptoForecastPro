import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime
import subprocess

# Load environment variables from .env file
load_dotenv()
BASE_URL = "https://api.freecryptoapi.com/v1"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# Define base directory for data storage
BASE_DATA_DIR = "data/crypto/daily_crypto_data"

# Create a unique folder for the current date with raw and processed_csv subfolders
current_date = datetime.now().strftime("%Y-%m-%d")
date_dir = os.path.join(BASE_DATA_DIR, current_date)
raw_dir = os.path.join(date_dir, "raw")
processed_csv_dir = os.path.join(date_dir, "processed_csv")
os.makedirs(raw_dir, exist_ok=True)
os.makedirs(processed_csv_dir, exist_ok=True)

def save_to_file(filename, data):
    """Helper function to save data to a JSON file in the raw directory."""
    file_path = os.path.join(raw_dir, filename)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {file_path}")

def get_crypto_data(symbols):
    """Fetches data for one or multiple cryptocurrencies and saves to a file."""
    symbols_str = '+'.join(symbols)
    url = f"{BASE_URL}/getData?symbol={symbols_str}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    save_to_file("crypto_data.json", data)
    return data

def get_crypto_conversion(from_currency, to_currency, amount):
    """Converts an amount from one cryptocurrency to another and saves to a file."""
    url = f"{BASE_URL}/getConversion?from={from_currency}&to={to_currency}&amount={amount}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    save_to_file("crypto_conversion.json", data)
    return data

####################################################################################################
def get_crypto_list():
    """Fetches the list of supported cryptocurrencies and saves to a file."""
    url = f"{BASE_URL}/getCryptoList"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    save_to_file("crypto_list.json", data)
    return data

def get_exchange_pairs(exchange):
    """Fetches all pairs listed on a supported crypto exchange and saves to a file."""
    url = f"{BASE_URL}/getExchange?exchange={exchange}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    save_to_file("exchange_pairs.json", data)
    return data

def get_data_in_currency(symbols, local_currency):
    """Fetches the latest price of cryptocurrencies in a specified local currency and saves to a file."""
    symbols_str = '+'.join(symbols)
    url = f"{BASE_URL}/getDataCurrency?symbol={symbols_str}&local={local_currency}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    save_to_file("data_in_currency.json", data)
    return data

def get_historical_data(symbol, days):
    """Fetches historical data for a cryptocurrency and saves to a file."""
    url = f"{BASE_URL}/getHistory?symbol={symbol}&days={days}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    save_to_file("historical_data.json", data)
    return data

def get_historical_timeframe(symbol, start_date, end_date):
    """Fetches historical data for a specific timeframe for a cryptocurrency and saves to a file."""
    url = f"{BASE_URL}/getTimeframe?symbol={symbol}&start={start_date}&end={end_date}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    save_to_file("historical_timeframe.json", data)
    return data

# Example usage
if __name__ == "__main__":
    symbols = ["BTC", "ETH", "USDT", "SOL", "BNB",
               "USDC", "XRP", "DOGE", "ADA", "TRX"]
    from_currency = "BTC"
    to_currency = "ETH"
    amount = 1000
    
    get_crypto_data(symbols)
    get_crypto_conversion(from_currency, to_currency, amount)
    
    # Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to transform_crypto_daily_data_to_csv.py
transform_script_path = os.path.join(current_script_dir, "..", "..", "data_processing", "crypto", "transform_crypto_daily_data_to_csv.py")

# Trigger the transform_crypto_daily_data_to_csv.py script
if os.path.exists(transform_script_path):
    try:
        print(f"Triggering {transform_script_path}...")
        subprocess.run(["python3", transform_script_path], check=True)
        print("transform_crypto_daily_data_to_csv.py executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute transform_crypto_daily_data_to_csv.py: {e}")
else:
    print(f"Script not found at: {transform_script_path}")

