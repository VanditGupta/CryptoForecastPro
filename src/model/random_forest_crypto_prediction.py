import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys
import os
import joblib

def main():
    CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
    next_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    # Define file paths
    historical_data_path = "data/historical_crypto_reddit_merged_historical/engineered_historical_data.csv"
    daily_data_path = f"data/daily_crypto_reddit_merged/{CURRENT_DATE}/engineered_daily_data.csv"
    output_path = f"results/{CURRENT_DATE}/price_change/crypto_prediction_results_{next_date}.csv"
    plot_path = f"results/{CURRENT_DATE}/plots/predicted_vs_actual.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Load data
    print("Loading historical and daily data...")
    historical_data = pd.read_csv(historical_data_path, parse_dates=['Date'])
    daily_data = pd.read_csv(daily_data_path, parse_dates=['Date'])

    # Ensure Consistent Columns
    assert list(historical_data.columns) == list(daily_data.columns), "Column mismatch between datasets!"

    # Merge Historical and Daily Data
    print("Merging historical and daily data...")
    merged_data = pd.concat([historical_data, daily_data], ignore_index=True)
    merged_data.sort_values(by='Date', inplace=True)

    # Drop Unnecessary Columns
    print("Dropping unnecessary columns...")
    columns_to_drop = ['Title', 'Content', 'Row_Count', 'Sentiment_Label']
    merged_data = merged_data.drop(columns=columns_to_drop, errors='ignore')

    # Handle Missing Values
    print("Handling missing values...")
    merged_data = merged_data.ffill()

    # Feature Selection
    features = [
        'Symbol', 'Open', 'High', 'Low', 'Close', 'Sentiment_Score', 'Normalized_Sentiment_Score',
        'Sentiment_Score_Interaction', 'Sentiment_Lag_1', 'Sentiment_Lag_3', 'Sentiment_Lag_7',
        'Score', 'Score_Lag_1', 'Score_Lag_3', 'Score_Lag_7', 'Comments',
        'Comments_Lag_1', 'Comments_Lag_3', 'Comments_Lag_7'
    ]
    target = 'Price_Change'

    X = merged_data[features]
    y = merged_data[target]

    # Encode the Symbol Column
    print("Encoding the Symbol column...")
    label_encoder = LabelEncoder()
    X.loc[:, 'Symbol'] = label_encoder.fit_transform(X['Symbol'])

    # Train-Test Split for Evaluation
    print("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest with Best Parameters
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

    # Predict on Test Data
    print("Predicting on test data...")
    y_pred = rf_best_model.predict(X_test)

    # Evaluate the Model
    rmse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    accuracy = rf_best_model.score(X_test, y_test)

    print(f"\nEvaluation Metrics for Random Forest with Best Parameters:")
    print(f"RMSE: {rmse}")
    print(f"R²: {r2}")
    print(f"Accuracy: {accuracy}")

    # Predict for the Next Day
    print("Predicting the next day's price change...")
    latest_data = daily_data.tail(1)[features]
    latest_data.loc[:, 'Symbol'] = label_encoder.transform(latest_data['Symbol'])
    next_day_prediction = rf_best_model.predict(latest_data)

    print(f"\nPredicted Price Change for the Next Day: {next_day_prediction[0]}")
    
    # Saving next day prediction
    print(f"Saving next day prediction to '{output_path}'")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    next_day_prediction_df = pd.DataFrame({"Predicted_Price_Change": [next_day_prediction[0]]})
    next_day_prediction_df.to_csv(output_path, index=False)
    
    # Save the Model
    model_path = f"models/{CURRENT_DATE}/random_forest_crypto_prediction_model.pkl"
    print(f"Saving the model to '{model_path}'")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(rf_best_model, model_path)
    

    # Plot Actual vs Predicted
    plt.figure(figsize=(12, 6))
    plt.scatter(y_test, y_pred, alpha=0.6, label="Predicted vs Actual")
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label="Perfect Prediction")
    plt.title("Random Forest: Predicted vs Actual Price Change")
    plt.xlabel("Actual Price Change")
    plt.ylabel("Predicted Price Change")
    plt.legend()
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)

    print("\nScript completed successfully. Check 'predicted_vs_actual.png' for results.")
    print("Exiting now.")
    sys.exit(0)

if __name__ == "__main__":
    main()
