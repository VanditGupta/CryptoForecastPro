import json
import random

# Generate random predictions for tomorrow
predicted_prices = {
    "BTC": {"PredictedPrice": round(random.uniform(104800, 105200), 2)},
    "ETH": {"PredictedPrice": round(random.uniform(3300, 3350), 2)},
    "USDT": {"PredictedPrice": 1.00},
    "SOL": {"PredictedPrice": round(random.uniform(250, 255), 2)},
    "BNB": {"PredictedPrice": round(random.uniform(680, 685), 2)},
    "USDC": {"PredictedPrice": 1.00},
    "XRP": {"PredictedPrice": round(random.uniform(3.10, 3.15), 2)},
    "DOGE": {"PredictedPrice": round(random.uniform(0.34, 0.36), 4)},
    "ADA": {"PredictedPrice": round(random.uniform(0.98, 1.00), 4)},
    "TRX": {"PredictedPrice": round(random.uniform(0.25, 0.26), 4)}
}

# Save to JSON
with open("app/predicted_prices.json", "w") as f:
    json.dump(predicted_prices, f, indent=4)
print("Tomorrow's predicted prices saved to 'predicted_prices.json'")
