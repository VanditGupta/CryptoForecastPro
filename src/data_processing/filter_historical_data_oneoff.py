import pandas as pd
from datetime import datetime

# Path to the combined file
COMBINED_FILE_PATH = "data/crypto/historical_crypto_data/combined/combined_historical_data.csv"
OUTPUT_FILE_PATH = "data/crypto/historical_crypto_data/combined/filtered_combined_historical_data.csv"

# Cutoff date
cutoff_date = datetime.strptime("2020-09-04", "%Y-%m-%d")

# Read the combined file
df = pd.read_csv(COMBINED_FILE_PATH)

# Ensure the Date column is in datetime format
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

# Filter rows: Keep only rows with Date >= cutoff_date
filtered_df = df[df["Date"] >= cutoff_date].copy()

# Format the Date column to the desired format: YYYY-MM-DD HH:MM:SS
filtered_df["Date"] = filtered_df["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")

# Save the filtered DataFrame to a new file
filtered_df.to_csv(OUTPUT_FILE_PATH, index=False)

print(f"Filtered combined data saved to: {OUTPUT_FILE_PATH}")
