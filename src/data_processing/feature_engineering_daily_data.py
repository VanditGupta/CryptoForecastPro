import pandas as pd
import os
from datetime import datetime
import subprocess  # Import subprocess module

# File paths
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
current_script_dir = os.path.dirname(os.path.abspath(__file__))

print("Current Directory" + current_script_dir)

daily_data_path = os.path.normpath(
    os.path.join(current_script_dir, "..", f"data/daily_crypto_reddit_merged/{CURRENT_DATE}/cleaned_daily_data.csv")
)
output_path = os.path.normpath(
    os.path.join(current_script_dir, "..", f"data/daily_crypto_reddit_merged/{CURRENT_DATE}/engineered_daily_data.csv")
)
merge_script_path = os.path.normpath(
    os.path.join(current_script_dir, "merge_crypto_reddit_daily_data.py")
)

# Load data
daily_data = pd.read_csv(daily_data_path)

# Feature Engineering

# Add price change feature
daily_data['Price_Change'] = daily_data['Close'] - daily_data['Open']

# Add normalized sentiment score
daily_data['Normalized_Sentiment_Score'] = daily_data['Sentiment_Score'] / daily_data['Row_Count']

# Add interaction term (Sentiment_Score * Score)
daily_data['Sentiment_Score_Interaction'] = daily_data['Sentiment_Score'] * daily_data['Score']

# Save the engineered data
os.makedirs(os.path.dirname(output_path), exist_ok=True)
daily_data.to_csv(output_path, index=False)
print(f"Engineered daily data saved to '{output_path}'")

# Call the merge_crypto_reddit_daily_data.py script using subprocess
try:
    result = subprocess.run(
        ["python", merge_script_path],
        check=True,
        capture_output=True,
        text=True
    )
    print(f"Successfully executed merge script:\n{result.stdout}")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while executing merge script:\n{e.stderr}")
