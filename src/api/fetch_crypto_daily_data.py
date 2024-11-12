import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()
BASE_URL = "https://api.freecryptoapi.com/v1"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# Define base directory for data storage
BASE_DATA_DIR = "data/daily_data/raw"

# Create a unique timestamped folder based on current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d")
output_dir = os.path.join(BASE_DATA_DIR, current_datetime)
os.makedirs(output_dir, exist_ok=True)


def save_to_file(filename, data):
    """Helper function to save data to a JSON file in the output directory."""
    file_path = os.path.join(output_dir, filename)
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
    
    
    # exchange = "binance"
    # local_currency = "EUR"
    # symbol = "BTC"
    # days = 5
    # start_date = "2022-05-05"
    # end_date = "2022-05-10"


    # The following APIs are not used because of high token usage

    # get_crypto_list()
    # get_exchange_pairs(exchange)

    # The following APIs are not used because of it requires a paid plan
    # get_data_in_currency(symbols, local_currency)

    # Not required as the historical data has been fetched from https://coincodex.com/
    # get_historical_data(symbol, days)
    # get_historical_timeframe("ETHBTC@binance", start_date, end_date)
