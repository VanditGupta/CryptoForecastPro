import os
import pandas as pd

# Define file paths
CRYPTO_DATA_PATH = "data/crypto/historical_crypto_data/combined/filtered_combined_historical_data.csv"
REDDIT_DATA_PATH = "data/reddit_posts/historical_reddit_posts/combined/merged_historical_reddit_posts.csv"
OUTPUT_PATH = "data/merged/crypto_reddit_daily_merged.csv"

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Read the cryptocurrency and Reddit data
crypto_df = pd.read_csv(CRYPTO_DATA_PATH)
reddit_df = pd.read_csv(REDDIT_DATA_PATH)

# Ensure Date columns are in datetime format
crypto_df["Date"] = pd.to_datetime(crypto_df["Date"], errors="coerce")
reddit_df["Created_At"] = pd.to_datetime(reddit_df["Created_At"], errors="coerce")

# Round Reddit timestamps to the nearest day
reddit_df["Date"] = reddit_df["Created_At"].dt.floor("D")

# Ensure Title and Content columns are strings and replace NaN with empty strings
reddit_df["Title"] = reddit_df["Title"].fillna("").astype(str)
reddit_df["Content"] = reddit_df["Content"].fillna("").astype(str)

# Aggregate Reddit data by Crypto and Date
aggregated_reddit = reddit_df.groupby(["Crypto", "Date"]).agg({
    "Subreddit": lambda x: ", ".join(x.unique()),  # Concatenate unique subreddit names
    "Score": "mean",       # Average sentiment score across posts
    "Comments": "sum",     # Total comments across posts
    "Title": lambda x: " | ".join(x),  # Concatenate all titles with a delimiter
    "Content": lambda x: " | ".join(x)  # Concatenate all content with a delimiter
}).reset_index()

# Merge with cryptocurrency data
merged_df = pd.merge(
    crypto_df,
    aggregated_reddit,
    left_on=["Symbol", "Date"],
    right_on=["Crypto", "Date"],
    how="inner"  # Inner join to ensure only matching dates are retained
)

# Drop redundant columns
merged_df = merged_df.drop(columns=["Crypto"])

# Save the combined dataset
merged_df.to_csv(OUTPUT_PATH, index=False)

print(f"Merged dataset saved to: {OUTPUT_PATH}")
