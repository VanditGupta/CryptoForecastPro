import pandas as pd
import os
from datetime import datetime

# Automatically get the current date in YYYY-MM-DD format
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

# Get the current working directory
current_script_dir = os.getcwd()

# Construct the daily data file path by going two folders back and locating the file
daily_data_path = os.path.join(current_script_dir, f"data/daily_crypto_reddit_merged/{CURRENT_DATE}/merged_crypto_reddit_data.csv")

# Normalize the path for consistency
daily_data_path = os.path.normpath(daily_data_path)

print(f"Daily data path: {daily_data_path}")

# Load data
daily_data = pd.read_csv(daily_data_path)

# Display basic information
print("Daily Data Overview:")
print(daily_data.info())

# Check for missing values
print("\nMissing Values in Daily Data:")
print(daily_data.isnull().sum())

# Fill missing values
daily_data['Symbol'].fillna('Unknown', inplace=True)
daily_data.fillna(0, inplace=True)

# Validate date column
daily_data['Date'] = pd.to_datetime(daily_data['Date'], errors='coerce')
print("\nInvalid Dates in Daily Data:")
print(daily_data[daily_data['Date'].isnull()])

# Ensure numeric columns are valid
numeric_columns = ['Open', 'High', 'Low', 'Close', 'Sentiment_Score', 'Score', 'Comments']
for col in numeric_columns:
    daily_data[col] = pd.to_numeric(daily_data[col], errors='coerce')

# Drop rows with invalid numeric data
daily_data.dropna(subset=numeric_columns, inplace=True)

# Ensure Sentiment_Label contains valid categories
valid_labels = ['Positive', 'Neutral', 'Negative']
daily_data['Sentiment_Label'] = daily_data['Sentiment_Label'].where(
    daily_data['Sentiment_Label'].isin(valid_labels), 'Neutral'
)

# Remove duplicates
daily_data.drop_duplicates(inplace=True)

# Define the file paths dynamically
cleaned_daily_data_path = os.path.join(current_script_dir, f"data/daily_crypto_reddit_merged/{CURRENT_DATE}/cleaned_daily_data.csv")

# Normalize the path for consistency
cleaned_daily_data_path = os.path.normpath(cleaned_daily_data_path)

# Save the cleaned daily data
daily_data.to_csv(cleaned_daily_data_path, index=False)
print(f"Cleaned daily data saved to '{cleaned_daily_data_path}'")
