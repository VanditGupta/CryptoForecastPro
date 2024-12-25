import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def main():
    # Define file paths
    historical_data_path = "../data/historical_crypto_reddit_merged_historical/engineered_historical_data.csv"
    daily_data_path = f"../data/daily_crypto_reddit_merged/{datetime.now().strftime('%Y-%m-%d')}/engineered_daily_data.csv"

    # Load data
    print("Loading historical and daily data...")
    historical_data = pd.read_csv(historical_data_path, parse_dates=['Date'])
    daily_data = pd.read_csv(daily_data_path, parse_dates=['Date'])

    # Step 2: Ensure Consistent Columns
    assert list(historical_data.columns) == list(daily_data.columns), "Column mismatch between datasets!"

    # Step 3: Merge Historical and Daily Data
    print("Merging historical and daily data...")
    merged_data = pd.concat([historical_data, daily_data], ignore_index=True)
    merged_data.sort_values(by='Date', inplace=True)

    # Step 4: Drop Unnecessary Columns
    print("Dropping unnecessary columns...")
    columns_to_drop = ['Title', 'Content', 'Row_Count', 'Sentiment_Label']
    merged_data = merged_data.drop(columns=columns_to_drop, errors='ignore')

    # Step 5: Handle Missing Values
    print("Handling missing values...")
    merged_data.fillna(method='ffill', inplace=True)

    # Step 6: Feature Selection
    features = [
        'Symbol', 'Open', 'High', 'Low', 'Close', 'Sentiment_Score', 'Normalized_Sentiment_Score',
        'Sentiment_Score_Interaction', 'Sentiment_Lag_1', 'Sentiment_Lag_3', 'Sentiment_Lag_7',
        'Score', 'Score_Lag_1', 'Score_Lag_3', 'Score_Lag_7', 'Comments',
        'Comments_Lag_1', 'Comments_Lag_3', 'Comments_Lag_7'
    ]
    target = 'Price_Change'

    X = merged_data[features]
    y = merged_data[target]

    # Step 7: Label Encode the Symbol Column
    print("Encoding the Symbol column...")
    label_encoder = LabelEncoder()
    X['Symbol'] = label_encoder.fit_transform(X['Symbol'])

    # Step 8: Train-Test Split for Evaluation
    print("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Step 9: Train Random Forest with Best Parameters
    print("Training Random Forest with best parameters...")
    rf_best_model = RandomForestRegressor(
        bootstrap=True,
        max_depth=None,
        min_samples_leaf=2,
        min_samples_split=2,
        n_estimators=100,
        random_state=42
    )
    rf_best_model.fit(X_train, y_train)

    # Step 10: Predict on Test Data
    print("Predicting on test data...")
    y_pred = rf_best_model.predict(X_test)

    # Step 11: Evaluate the Model
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)

    print(f"\nEvaluation Metrics for Random Forest with Best Parameters:")
    print(f"RMSE: {rmse}")
    print(f"R²: {r2}")

    # Step 12: Predict for the Next Day
    print("Predicting the next day's price change...")
    latest_data = daily_data.tail(1)[features]
    latest_data['Symbol'] = label_encoder.transform(latest_data['Symbol'])
    next_day_prediction = rf_best_model.predict(latest_data)

    print(f"\nPredicted Price Change for the Next Day: {next_day_prediction[0]}")

    # Step 13: Plot Actual vs Predicted
    plt.figure(figsize=(12, 6))
    plt.scatter(y_test, y_pred, alpha=0.6, label="Predicted vs Actual")
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label="Perfect Prediction")
    plt.title("Random Forest: Predicted vs Actual Price Change")
    plt.xlabel("Actual Price Change")
    plt.ylabel("Predicted Price Change")
    plt.legend()
    plt.savefig("predicted_vs_actual.png")
    plt.show()

    print("\nScript completed successfully. Check 'predicted_vs_actual.png' for results.")

if __name__ == "__main__":
    main()
