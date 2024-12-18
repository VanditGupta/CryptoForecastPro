import os
import pandas as pd
from datetime import timedelta

# Define file paths
CRYPTO_DATA_PATH = "data/crypto/historical_crypto_data/combined/filtered_combined_historical_data.csv"
REDDIT_DATA_PATH = "data/reddit_posts/historical_reddit_posts/combined/merged_historical_reddit_posts.csv"
OUTPUT_PATH = "data/merged/historical/crypto_reddit_combined_3day.csv"

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Read the cryptocurrency and Reddit data
crypto_df = pd.read_csv(CRYPTO_DATA_PATH)
reddit_df = pd.read_csv(REDDIT_DATA_PATH)

# Ensure Date columns are in datetime format
crypto_df["Date"] = pd.to_datetime(crypto_df["Date"], errors="coerce")
reddit_df["Created_At"] = pd.to_datetime(reddit_df["Created_At"], errors="coerce")

# Add Price_Difference column
crypto_df["Price_Difference"] = crypto_df["Close"] - crypto_df["Open"]

# Ensure Title and Content columns are strings
reddit_df["Title"] = reddit_df["Title"].astype(str)
reddit_df["Content"] = reddit_df["Content"].astype(str)

# Aggregate Reddit data over a 3-day window
reddit_df["Date"] = reddit_df["Created_At"].dt.floor("D")
reddit_df["Window_End"] = reddit_df["Date"] + timedelta(days=2)  # Create 3-day window

aggregated_reddit = reddit_df.groupby(["Crypto", "Window_End"]).agg({
    "Subreddit": lambda x: ", ".join(x.unique()),  # Unique subreddits
    "Score": "mean",       # Average sentiment score
    "Comments": "sum",     # Total comments
    "Title": lambda x: " | ".join(x),  # Concatenate titles
    "Content": lambda x: " | ".join(x)  # Concatenate content
}).reset_index()

# Merge with cryptocurrency data
crypto_df["Window_End"] = crypto_df["Date"]  # Align price data to the window
merged_df = pd.merge(
    crypto_df,
    aggregated_reddit,
    left_on=["Symbol", "Window_End"],
    right_on=["Crypto", "Window_End"],
    how="left"
)

# Drop redundant columns
merged_df = merged_df.drop(columns=["Crypto", "Window_End", "Open", "Close"])  # Drop Open/Close for simplicity

# Save the combined dataset
merged_df.to_csv(OUTPUT_PATH, index=False)

print(f"Merged dataset saved to: {OUTPUT_PATH}")
