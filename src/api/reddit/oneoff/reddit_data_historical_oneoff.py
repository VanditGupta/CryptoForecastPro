import os
import logging
import time
import praw
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

# Load environment variables from .env file
load_dotenv()

# Create logs folder if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
log_file = "logs/reddit_data_historical.log"
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
base_output_dir = "data/reddit_posts/historical_reddit_posts"
os.makedirs(base_output_dir, exist_ok=True)

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

    # Create a folder for the cryptocurrency
    crypto_folder = os.path.join(base_output_dir, symbol.lower())
    os.makedirs(crypto_folder, exist_ok=True)
    output_file = os.path.join(crypto_folder, f"{symbol.lower()}.csv")

    logging.info(f"Started fetching historical posts for {symbol}")
    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            for keyword in keywords:
                for post in subreddit.search(keyword, limit=200):
                    if len(crypto_posts) >= 2500:  # Stop once we reach 2500 posts per cryptocurrency
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
                if len(crypto_posts) >= 2500:
                    break
            if len(crypto_posts) >= 2500:
                break
        except Exception as e:
            logging.error(f"Error processing subreddit '{subreddit_name}' for {symbol}: {e}")

        # Add a delay to avoid hitting API rate limits
        time.sleep(1)

    # Save data to a CSV file for the specific cryptocurrency
    df = pd.DataFrame(crypto_posts)
    df.to_csv(output_file, index=False)
    logging.info(f"Fetched {len(crypto_posts)} historical posts for {symbol}. Saved to {output_file}")
