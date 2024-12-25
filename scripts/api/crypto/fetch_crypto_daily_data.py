import requests
import boto3
import os
import json
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()
BASE_URL = "https://api.freecryptoapi.com/v1"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# Initialize AWS S3 client
s3 = boto3.client('s3')

# Bucket and folder structure
BUCKET_NAME = "crypto-sentiment-forecasting"
BASE_S3_PATH = "cryptoforecastpro/data/crypto/daily_crypto_data/"

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

def save_to_s3(filename, data):
    """Uploads JSON data to the raw folder in S3."""
    s3_key = f"{BASE_S3_PATH}{current_date}/raw/{filename}"  # Add raw folder inside the date folder
    s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=json.dumps(data))
    print(f"Data saved to s3://{BUCKET_NAME}/{s3_key}")

def get_crypto_data(symbols):
    """Fetches data for one or multiple cryptocurrencies and saves to S3."""
    symbols_str = '+'.join(symbols)
    url = f"{BASE_URL}/getData?symbol={symbols_str}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    save_to_s3("crypto_data.json", data)
    return data

def get_crypto_conversion(from_currency, to_currency, amount):
    """Converts an amount from one cryptocurrency to another and saves to S3."""
    url = f"{BASE_URL}/getConversion?from={from_currency}&to={to_currency}&amount={amount}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    save_to_s3("crypto_conversion.json", data)
    return data

if __name__ == "__main__":
    # Example usage
    symbols = ["BTC", "ETH", "USDT", "SOL", "BNB", "USDC", "XRP", "DOGE", "ADA", "TRX"]
    from_currency = "BTC"
    to_currency = "ETH"
    amount = 1000

    # Fetch data and save to S3
    get_crypto_data(symbols)
    get_crypto_conversion(from_currency, to_currency, amount)
