import os
import logging
import time
import praw
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
import subprocess

# Load environment variables from .env file
load_dotenv()

# Create logs folder if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
log_file = "logs/reddit_data_daily.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3),  # Rotate logs at 5MB, keep 3 backups
        logging.StreamHandler()  # Also log to the console
    ]
)

# Set up Reddit API credentials using environment variables
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT"),
)

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

# Define base output directory
base_output_dir = "data/reddit_posts/daily_reddit_posts"
os.makedirs(base_output_dir, exist_ok=True)

# Get the current date in YYYY-MM-DD format
current_date = datetime.now().strftime("%Y-%m-%d")
date_folder = os.path.join(base_output_dir, current_date)
os.makedirs(date_folder, exist_ok=True)

# Helper function to clean text
def clean_text(text):
    """Cleans the input text by removing unwanted characters."""
    return text.replace("\n", " ").strip()

# Fetch posts for each cryptocurrency
for crypto in crypto_list:
    symbol = crypto["symbol"]
    keywords = crypto["keywords"]
    crypto_posts = []
    seen_post_ids = set()  # Track unique post IDs

    # Create a folder for the cryptocurrency within the date folder
    crypto_folder = os.path.join(date_folder, symbol.lower())
    os.makedirs(crypto_folder, exist_ok=True)
    output_file = os.path.join(crypto_folder, f"{symbol.lower()}.csv")

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

        # Add a delay to avoid hitting API rate limits
        time.sleep(1)

    # Save data to a CSV file for the specific cryptocurrency
    df = pd.DataFrame(crypto_posts)
    df.to_csv(output_file, index=False)
    logging.info(f"Fetched {len(crypto_posts)} posts for {symbol}. Saved to {output_file}")

# Call combine_reddit_daily_data.py at the end of the script
if __name__ == "__main__":
    # Get the directory of the current script
    current_script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to combine_reddit_daily_data.py in the reddit folder
    combine_script_path = os.path.join(current_script_dir, "..", "..", "data_processing", "reddit", "combine_reddit_daily_data.py")

    # Check if the script exists
    if os.path.exists(combine_script_path):
        try:
            logging.info(f"Triggering {combine_script_path}...")
            subprocess.run(["python3", combine_script_path], check=True)
            logging.info("combine_reddit_daily_data.py executed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to execute combine_reddit_daily_data.py: {e}")
    else:
        logging.error(f"combine_reddit_daily_data.py not found at: {combine_script_path}")
