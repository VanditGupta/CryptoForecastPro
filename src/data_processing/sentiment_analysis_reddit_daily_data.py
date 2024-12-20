import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

# Get the current date in YYYY-MM-DD format
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

# File paths
input_path = f"data/reddit_posts/daily_reddit_posts/{CURRENT_DATE}/combined/merged_daily_reddit_posts.csv"
output_path = f"data/reddit_posts/daily_reddit_posts/{CURRENT_DATE}/combined/sentiment_analysis/sentiment_analyzed_reddit_posts.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to calculate sentiment using VADER
def calculate_sentiment_vader(text):
    """Analyze sentiment using VADER."""
    scores = analyzer.polarity_scores(text)
    compound_score = scores['compound']
    # Determine sentiment label based on compound score
    if compound_score >= 0.05:
        sentiment = "Positive"
    elif compound_score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment, compound_score

# Load data
reddit_posts = pd.read_csv(input_path)
reddit_posts['Combined_Text'] = reddit_posts['Title'].fillna('') + " " + reddit_posts['Content'].fillna('')

# Perform sentiment analysis
results = reddit_posts['Combined_Text'].apply(calculate_sentiment_vader)
reddit_posts['Sentiment_Label'] = results.apply(lambda x: x[0])  # Positive, Negative, Neutral
reddit_posts['Sentiment_Score'] = results.apply(lambda x: x[1])  # Compound score

# Save the results
reddit_posts.to_csv(output_path, index=False)
print(f"Sentiment-analyzed Reddit data saved to '{output_path}'")
