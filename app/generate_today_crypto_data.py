import pandas as pd

# Today's crypto data
today_data = {
    "Date": ["27/01/25"] * 10,  # Repeat the date to match the length of other fields
    "Symbol": ["BTC", "ETH", "USDT", "SOL", "BNB", "USDC", "XRP", "DOGE", "ADA", "TRX"],
    "Open": [104949.91, 3328.93, 1, 253.46, 682.59, 1, 3.12, 0.35, 0.98, 0.25],
    "High": [104992, 3329.02, 1, 253.32, 682.58, 1, 3.12, 0.35, 0.99, 0.25],
    "Low": [104729.99, 3310.52, 1, 250.60, 681.39, 1, 3.11, 0.34, 0.98, 0.25],
    "Close": [104851.68, 3312.26, 1, 250.67, 681.32, 1, 3.11, 0.34, 0.98, 0.25],
}

# Convert to DataFrame
today_df = pd.DataFrame(today_data)

# Save to JSON
json_path = "app/today_crypto_data.json"
today_df.to_json(json_path, orient="records", indent=4)
print(f"Today's crypto data saved to '{json_path}'")
