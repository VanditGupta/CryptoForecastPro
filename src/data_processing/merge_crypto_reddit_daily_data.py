import pandas as pd
from datetime import datetime, timedelta
import os

# File paths
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
crypto_data_path = f"data/crypto/daily_crypto_data/{CURRENT_DATE}/processed_csv/processed_crypto_data.csv"
grouped_reddit_path = f"data/reddit_posts/daily_reddit_posts/{CURRENT_DATE}/combined/grouped/grouped_reddit_data.csv"
output_path = f"data/crypto_reddit_merged/{CURRENT_DATE}/merged_crypto_reddit_data.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Function to find the closest date with tolerance
def find_closest_date_with_tolerance(crypto_date, reddit_dates, tolerance_days=7):
    reddit_dates = pd.Series(reddit_dates)  # Convert to pandas Series for consistency
    date_range = reddit_dates[(reddit_dates >= (crypto_date - timedelta(days=tolerance_days))) & 
                              (reddit_dates <= (crypto_date + timedelta(days=tolerance_days)))]
    if not date_range.empty:
        return date_range.iloc[(date_range - crypto_date).abs().argsort().iloc[0]]
    else:
        return None

# Load and preprocess crypto data
crypto_data = pd.read_csv(crypto_data_path)
crypto_data['Date'] = pd.to_datetime(crypto_data['Date']).dt.date  # Remove time component

# Debug: Print unique symbols and dates in crypto_data
print("Crypto data preview after date conversion:")
print(crypto_data.head())
print("Unique symbols in crypto_data:", crypto_data['Symbol'].unique())
print("Unique dates in crypto_data:", crypto_data['Date'].unique())

# Load and preprocess grouped Reddit data
grouped_reddit = pd.read_csv(grouped_reddit_path)
grouped_reddit['Created_At'] = pd.to_datetime(grouped_reddit['Created_At']).dt.date

# Debug: Print unique symbols and dates in grouped_reddit
print("Grouped Reddit data preview after date conversion:")
print(grouped_reddit.head())
print("Unique symbols in grouped_reddit:", grouped_reddit['Crypto'].unique())
print("Unique dates in grouped_reddit:", grouped_reddit['Created_At'].unique())

# Sort datasets by Symbol and Crypto in ascending order
crypto_data = crypto_data.sort_values(by='Symbol')
grouped_reddit = grouped_reddit.sort_values(by='Crypto')

# Debug: Confirm sorting
print("Crypto data sorted by Symbol:")
print(crypto_data.head())
print("Grouped Reddit data sorted by Crypto:")
print(grouped_reddit.head())

# Merge on closest dates
reddit_dates = grouped_reddit['Created_At'].unique()
print("Unique Reddit dates:", reddit_dates)

crypto_data['Closest_Reddit_Date'] = crypto_data['Date'].apply(
    lambda x: find_closest_date_with_tolerance(x, reddit_dates)
)

# Debug: Check the closest dates assigned
print("Closest Reddit dates in crypto_data:")
print(crypto_data[['Date', 'Closest_Reddit_Date']].head())

merged_data = pd.merge(
    crypto_data,
    grouped_reddit,
    left_on=['Symbol', 'Closest_Reddit_Date'],
    right_on=['Crypto', 'Created_At'],
    how='inner'
)

# Debug: Check intermediate merged data
print("Merged data preview:")
print(merged_data.head())
print("Number of rows in merged data:", len(merged_data))

# Add lagged features
for lag in [1, 3, 7]:  # Lag windows in days
    merged_data[f'Sentiment_Lag_{lag}'] = merged_data.groupby('Symbol')['Sentiment_Score'].shift(lag)
    merged_data[f'Score_Lag_{lag}'] = merged_data.groupby('Symbol')['Score'].shift(lag)
    merged_data[f'Comments_Lag_{lag}'] = merged_data.groupby('Symbol')['Comments'].shift(lag)

# Drop unnecessary columns and save
merged_data = merged_data.drop(columns=['Closest_Reddit_Date', 'Crypto', 'Created_At'])
merged_data.to_csv(output_path, index=False)

# Debug: Print final data
print("Final merged data:")
print(merged_data.head())
print(f"Final data saved to '{output_path}' with {len(merged_data)} rows")
