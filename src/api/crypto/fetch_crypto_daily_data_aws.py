import requests
import os
import json
from datetime import datetime
from awsglue.utils import getResolvedOptions
import boto3

# Load environment variables
BASE_URL = "https://api.freecryptoapi.com/v1"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# S3 Bucket and Folder Configuration
S3_BUCKET = os.getenv("S3_BUCKET")
S3_RAW_FOLDER = "crypto-data/raw"
S3_PROCESSED_FOLDER = "crypto-data/processed"

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")
s3_client = boto3.client('s3')

def save_to_s3(filename, data):
    """Helper function to save data to S3 as a JSON file."""
    s3_key = f"{S3_RAW_FOLDER}/{current_date}/{filename}"
    s3_client.put_object(
        Bucket=S3_BUCKET, 
        Key=s3_key, 
        Body=json.dumps(data, indent=4), 
        ContentType="application/json"
    )
    print(f"Data saved to s3://{S3_BUCKET}/{s3_key}")

def get_crypto_data(symbols):
    """Fetches data for one or multiple cryptocurrencies and saves to S3."""
    symbols_str = '+'.join(symbols)
    url = f"{BASE_URL}/getData?symbol={symbols_str}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    save_to_s3("crypto_data.json", data)
    return data

def get_crypto_conversion(from_currency, to_currency, amount):
    """Fetches conversion data and saves to S3."""
    url = f"{BASE_URL}/getConversion?from={from_currency}&to={to_currency}&amount={amount}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    save_to_s3("crypto_conversion.json", data)
    return data

def transform_data_to_csv():
    """Placeholder for transformation logic if needed."""
    # Implement your transformation logic here
    print("Transformation logic can be added here.")

if __name__ == "__main__":
    # Example usage
    symbols = ["BTC", "ETH", "USDT", "SOL", "BNB", "USDC", "XRP", "DOGE", "ADA", "TRX"]
    from_currency = "BTC"
    to_currency = "ETH"
    amount = 1000
    
    print("Fetching crypto data...")
    get_crypto_data(symbols)
    
    print("Fetching crypto conversion data...")
    get_crypto_conversion(from_currency, to_currency, amount)
    
    print("Running data transformation...")
    transform_data_to_csv()
    
    print("Data ingestion and transformation completed.")
