import pandas as pd
from datetime import datetime, timedelta
import os

# File paths
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
crypto_data_path = f"data/crypto/daily_crypto_data/{CURRENT_DATE}/processed_csv/processed_crypto_data.csv"
grouped_reddit_path = f"data/reddit_posts/daily_reddit_posts/{CURRENT_DATE}/combined/grouped/grouped_daily_reddit_data.csv"
output_path = f"data/daily_crypto_reddit_merged/{CURRENT_DATE}/merged_crypto_reddit_data.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Function to find the closest date with tolerance
def find_closest_date_with_tolerance(crypto_date, reddit_dates, tolerance_days=2):
    reddit_dates = pd.Series(reddit_dates)
    date_range = reddit_dates[(reddit_dates >= (crypto_date - timedelta(days=tolerance_days))) & 
                              (reddit_dates <= (crypto_date + timedelta(days=tolerance_days)))]
    if not date_range.empty:
        return date_range.iloc[(date_range - crypto_date).abs().argsort().iloc[0]]
    else:
        return None

# Load and preprocess crypto data
crypto_data = pd.read_csv(crypto_data_path)
crypto_data['Date'] = pd.to_datetime(crypto_data['Date']).dt.date

# Load and preprocess grouped Reddit data
grouped_reddit = pd.read_csv(grouped_reddit_path)
grouped_reddit['Created_At'] = pd.to_datetime(grouped_reddit['Created_At']).dt.date

# Sort datasets by Symbol and Crypto in ascending order
crypto_data = crypto_data.sort_values(by='Symbol')
grouped_reddit = grouped_reddit.sort_values(by='Crypto')

# Merge on closest dates
reddit_dates = grouped_reddit['Created_At'].unique()
crypto_data['Closest_Reddit_Date'] = crypto_data['Date'].apply(
    lambda x: find_closest_date_with_tolerance(x, reddit_dates)
)

merged_data = pd.merge(
    crypto_data,
    grouped_reddit,
    left_on=['Symbol', 'Closest_Reddit_Date'],
    right_on=['Crypto', 'Created_At'],
    how='inner'
)

# Add lagged features
for lag in [1, 3, 7]:  # Lag windows in days
    merged_data[f'Sentiment_Lag_{lag}'] = merged_data.groupby('Symbol')['Sentiment_Score'].shift(lag)
    merged_data[f'Score_Lag_{lag}'] = merged_data.groupby('Symbol')['Score'].shift(lag)
    merged_data[f'Comments_Lag_{lag}'] = merged_data.groupby('Symbol')['Comments'].shift(lag)

# Drop unnecessary columns and save
merged_data = merged_data.drop(columns=['Closest_Reddit_Date', 'Crypto', 'Created_At'])
merged_data.to_csv(output_path, index=False)

print(f"Final merged data saved to '{output_path}' with {len(merged_data)} rows")
