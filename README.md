# Cryptocurrency Sentiment and Price Prediction Tool

## Description

The Cryptocurrency Price Prediction Tool is an advanced tool designed to analyze and forecast cryptocurrency price trends by integrating real-time social sentiment data with historical and daily price data. This project leverages modern data engineering and machine learning techniques to provide actionable insights for 10 popular cryptocurrencies, including Bitcoin (BTC) and Ethereum (ETH), through an interactive QuickSight dashboard.

## Features

- **Real-Time Data Integration:**
  - Daily ingestion of cryptocurrency price data from CoinGecko & Free Crypto APIs.
  - Social sentiment analysis from Reddit posts using Reddit API.
- **Advanced Prediction Models:**
  - Automated model training and inference using AWS SageMaker.
  - Sentiment analysis using BERT to gauge market sentiment for the previous day.
- **Workflow Automation:**
  - Apache Airflow for scheduling and orchestrating data ingestion workflows.
  - AWS Step Functions for automating end-to-end model retraining workflows.
- **Interactive Dashboard:**
  - Insights delivered via a visually rich QuickSight dashboard, displaying trends in sentiment, historical prices, and price predictions.
- **System Monitoring:**
  - AWS CloudWatch for tracking workflow performance and setting alerts.

## Technical Stack

- **Data Ingestion:**
  - **APIs:** Reddit API, CoinGecko API
  - **Orchestration:** Apache Airflow
- **Storage:**
  - **AWS S3:** For storing raw and processed data
- **Modeling and Predictions:**
  - **AWS SageMaker:** For model training and batch inference
  - **BERT:** For sentiment analysis
- **Workflow Automation:**
  - **AWS Step Functions:** For orchestrating workflows
  - **AWS CloudWatch:** For monitoring and alerting
- **Visualization:**
  - **QuickSight:** For creating an interactive dashboard

## Dataset Description

- **Social Sentiment Data:** Daily Reddit posts containing data 10 cryptocurrencies (Bitcoin (BTC), Ethereum (ETH), Tether (USDT), Solana (SOL), BNB, USD Coin (USDC), XRP (XRP), Dogecoin (DOGE), Cardano (ADA), and TRON (TRX)).
- **Price Data:** Historical and real-time cryptocurrency prices sourced from CoinGecko, and Free Crypto APIs.

## Running the Application

1. **Data Pipeline Setup:**
   - Configure Apache Airflow to automate daily data ingestion from Reddit and CoinGecko, and Free Crypto APIs.
   - Store raw data in AWS S3 for processing.
2. **Data Processing:**
   - Preprocess the raw data to clean and transform it for model training using Lambda functions.
   - Perform sentiment analysis using BERT to gauge market sentiment.
   - Store processed data in AWS S3.
3. **Model Training and Prediction:**
   - Use AWS SageMaker to train sentiment and price prediction models.
   - Automate daily retraining workflows with Step Functions.
4. **Dashboard Integration:**
   - Connect the processed data in AWS S3 to QuickSight for visualizing results.

<!-- ## Visualization Screenshot

*(Add a screenshot of your QuickSight dashboard here.)* -->

## Contributing

Contributions are welcome. Please refer to our [CONTRIBUTING.md](https://github.com/VanditGupta/CryptoForecastPro/blob/main/CONTRIBUTING.md) for guidelines on how to contribute.

## License

This project is licensed under the [MIT LICENSE](https://opensource.org/licenses/MIT).

## Acknowledgements

- Special thanks to the contributors and supporters who helped make this project successful.

## Contact

For inquiries or contributions, feel free to contact me at [gupta.vandi@northeastern.edu](mailto:gupta.vandi@northeastern.edu).
