import pandas as pd
import random
from datetime import datetime, timedelta

# Cryptocurrencies and their subreddits
cryptos = [
    {"symbol": "BTC", "subreddit": "cryptocurrency"},
    {"symbol": "ETH", "subreddit": "CryptoMarkets"},
    {"symbol": "USDT", "subreddit": "Tether"},
    {"symbol": "SOL", "subreddit": "cryptotrading"},
    {"symbol": "BNB", "subreddit": "Binance"},
    {"symbol": "USDC", "subreddit": "USDC"},
    {"symbol": "XRP", "subreddit": "Ripple"},
    {"symbol": "DOGE", "subreddit": "Dogecoin"},
    {"symbol": "ADA", "subreddit": "Altcoin"},
    {"symbol": "TRX", "subreddit": "Tronix"},
]

# Example titles, content, and sentiment labels
example_reviews = [
    {
        "title": "Massive growth potential for {crypto}!",
        "content": "{crypto} has been performing exceptionally well recently. Many investors are bullish on its future.",
        "sentiment": "Positive",
        "score": random.uniform(0.5, 1),
    },
    {
        "title": "{crypto} adoption is slow but steady",
        "content": "{crypto} has shown resilience but needs more utility to gain mass adoption.",
        "sentiment": "Neutral",
        "score": 0,
    },
    {
        "title": "{crypto} crashes hard, but is it just temporary?",
        "content": "{crypto} has seen a major dip recently. People are debating whether it's a temporary setback or the start of a bigger problem.",
        "sentiment": "Negative",
        "score": random.uniform(-1, -0.5),
    },
]

# Generate random Reddit data
reddit_data = []
current_date = datetime.now()

for crypto in cryptos:
    for _ in range(random.randint(5, 10)):  # 5 to 10 reviews per cryptocurrency
        review = random.choice(example_reviews)
        reddit_data.append({
            "Crypto": crypto["symbol"],
            "Subreddit": crypto["subreddit"],
            "Title": review["title"].format(crypto=crypto["symbol"]),
            "Content": review["content"].format(crypto=crypto["symbol"]),
            "Score": random.randint(50, 1000),  # Random score
            "Created_At": (current_date - timedelta(minutes=random.randint(1, 1440))).strftime("%d/%m/%y %H:%M"),  # Random time in the past day
            "Comments": random.randint(10, 150),  # Random comment count
            "Combined_Text": review["title"].format(crypto=crypto["symbol"]) + " " + review["content"].format(crypto=crypto["symbol"]),
            "Sentiment_Label": review["sentiment"],
            "Sentiment_Score": review["score"],
        })

# Convert to DataFrame
reddit_df = pd.DataFrame(reddit_data)

# Save the Reddit data to the app folder
reddit_csv_path = "app/reddit_daily_data_all_cryptos.csv"
reddit_df.to_csv(reddit_csv_path, index=False)
print(f"Reddit daily data saved to '{reddit_csv_path}'")
