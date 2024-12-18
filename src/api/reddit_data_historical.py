import os
import praw
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
base_output_dir = "data/historical_reddit_posts"
os.makedirs(base_output_dir, exist_ok=True)

# Fetch posts for each cryptocurrency
for crypto in crypto_list:
    symbol = crypto["symbol"]
    keywords = crypto["keywords"]
    crypto_posts = []

    # Create a folder for the cryptocurrency
    crypto_folder = os.path.join(base_output_dir, symbol.lower())
    os.makedirs(crypto_folder, exist_ok=True)
    output_file = os.path.join(crypto_folder, f"{symbol.lower()}.csv")

    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        for keyword in keywords:
            for post in subreddit.search(keyword, limit=200):  # Limit increased for better data spread
                if len(crypto_posts) >= 2500:  # Stop once we reach 2500 posts per cryptocurrency
                    break
                crypto_posts.append({
                    "Crypto": symbol,
                    "Subreddit": subreddit_name,
                    "Title": post.title,
                    "Content": post.selftext,
                    "Score": post.score,
                    "Created_At": datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    "Comments": post.num_comments
                })
            if len(crypto_posts) >= 2500:
                break
        if len(crypto_posts) >= 2500:
            break

    # Save data to a CSV file for the specific cryptocurrency
    df = pd.DataFrame(crypto_posts)
    df.to_csv(output_file, index=False)
    print(f"Fetched {len(crypto_posts)} posts for {symbol}. Saved to {output_file}")
