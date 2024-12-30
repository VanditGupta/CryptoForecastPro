import boto3
import logging
import time
import praw
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import io
import os
import json

# Load environment variables from .env file
load_dotenv()

# Initialize AWS S3 client
s3 = boto3.client('s3')

# Initialize AWS Lambda client
lambda_client = boto3.client('lambda')

# Set up Reddit API credentials using environment variables
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT"),
)

# S3 bucket and folder paths
BUCKET_NAME = "crypto-sentiment-forecasting"
BASE_S3_PATH = "cryptoforecastpro/data/reddit_posts/daily_reddit_posts/"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Helper function to clean text
def clean_text(text):
    """Cleans the input text by removing unwanted characters."""
    return text.replace("\n", " ").strip()

# Save data to S3
def save_to_s3(dataframe, symbol, current_date):
    """Saves the DataFrame to S3 as a CSV."""
    csv_buffer = io.StringIO()
    dataframe.to_csv(csv_buffer, index=False)
    s3_key = f"{BASE_S3_PATH}{current_date}/{symbol.lower()}.csv"
    s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=csv_buffer.getvalue())
    logging.info(f"Saved data to s3://{BUCKET_NAME}/{s3_key}")

# Function to fetch posts for a single cryptocurrency
def fetch_reddit_posts(symbol, keywords, subreddits, current_date):
    """Fetches Reddit posts for a specific cryptocurrency."""
    crypto_posts = []
    seen_post_ids = set()  # Track unique post IDs

    logging.info(f"Started fetching posts for {symbol}")
    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            for keyword in keywords:
                for post in subreddit.search(keyword, limit=200):
                    if len(crypto_posts) >= 100:  # Stop once we reach 100 posts per cryptocurrency
                        break
                    if post.id in seen_post_ids:
                        continue
                    seen_post_ids.add(post.id)
                    crypto_posts.append({
                        "Crypto": symbol,
                        "Subreddit": subreddit_name,
                        "Title": clean_text(post.title),
                        "Content": clean_text(post.selftext),
                        "Score": post.score,
                        "Created_At": datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        "Comments": post.num_comments
                    })
                if len(crypto_posts) >= 100:
                    break
            if len(crypto_posts) >= 100:
                break
        except Exception as e:
            logging.error(f"Error processing subreddit '{subreddit_name}' for {symbol}: {e}")
            time.sleep(2)  # Add a delay for rate limits

    # Save data to S3 if posts were fetched
    if crypto_posts:
        df = pd.DataFrame(crypto_posts)
        save_to_s3(df, symbol, current_date)
    else:
        logging.info(f"No posts fetched for {symbol}")

# Lambda handler
def lambda_handler(event, context):
    """AWS Lambda handler function."""
    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # List of cryptocurrencies and their related keywords
    crypto_list = [
        {"symbol": "BTC", "keywords": ["Bitcoin", "BTC"]},
        {"symbol": "ETH", "keywords": ["Ethereum", "ETH"]},
        {"symbol": "USDT", "keywords": ["Tether", "USDT"]},
        {"symbol": "SOL", "keywords": ["Solana", "SOL"]},
        {"symbol": "BNB", "keywords": ["Binance Coin", "BNB"]},
        {"symbol": "USDC", "keywords": ["USD Coin", "USDC"]},
        {"symbol": "XRP", "keywords": ["Ripple", "XRP"]},
        {"symbol": "DOGE", "keywords": ["Dogecoin", "DOGE"]},
        {"symbol": "ADA", "keywords": ["Cardano", "ADA"]},
        {"symbol": "TRX", "keywords": ["Tron", "TRX"]},
    ]

    # Expanded list of relevant subreddits
    subreddits = [
        "cryptocurrency", "CryptoMarkets", "Bitcoin", "CryptoMoonShots",
        "Altcoin", "CryptoCurrencyTrading", "Binance", "BitcoinBeginners",
        "CryptoMoon", "AltStreetBets", "cryptotrading", "blockchain", "DeFi"
    ]

    # Fetch posts for each cryptocurrency
    for crypto in crypto_list:
        fetch_reddit_posts(crypto["symbol"], crypto["keywords"], subreddits, current_date)

    logging.info("Reddit data fetching completed.")

    # Invoke the combine_reddit_daily_data Lambda function synchronously
    try:
        response = lambda_client.invoke(
            FunctionName="combine_reddit_daily_data",  # Replace with the actual function name
            InvocationType="RequestResponse",  # Synchronous invocation
            Payload=json.dumps({
                "bucket": BUCKET_NAME,
                "current_date": current_date
            })
        )
        combine_response = json.loads(response['Payload'].read())
        logging.info("combine_reddit_daily_data Lambda function completed successfully.")
        logging.info(f"Response: {combine_response}")
    except Exception as e:
        logging.error(f"Error invoking combine_reddit_daily_data Lambda function: {e}")
        return {"statusCode": 500, "body": "Error in invoking combine_reddit_daily_data Lambda"}

    return {"statusCode": 200, "body": "Reddit data fetching and combining completed successfully."}
