import pandas as pd
from datetime import datetime
import os

# File paths
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
reddit_posts_path = f"data/reddit_posts/daily_reddit_posts/{CURRENT_DATE}/combined/sentiment_analysis/sentiment_analyzed_reddit_posts.csv"
output_path = f"data/reddit_posts/daily_reddit_posts/{CURRENT_DATE}/combined/grouped/grouped_reddit_data.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Load Reddit posts
reddit_posts = pd.read_csv(reddit_posts_path)

# Remove time part from Created_At and convert to date
reddit_posts['Created_At'] = pd.to_datetime(reddit_posts['Created_At']).dt.date

# Fill NaN values in Title and Content with a single space and ensure string type
reddit_posts['Title'] = reddit_posts['Title'].fillna(' ').astype(str)
reddit_posts['Content'] = reddit_posts['Content'].fillna(' ').astype(str)

# Group Reddit data by Crypto and Created_At
aggregated_reddit = reddit_posts.groupby(['Crypto', 'Created_At']).agg({
    'Sentiment_Score': 'mean',         # Average sentiment
    'Score': 'sum',                   # Total score
    'Comments': 'sum',                # Total number of comments
    'Title': '|'.join,                # Combine titles with '|'
    'Content': '|'.join,              # Combine content with '|'
    'Crypto': 'count'                 # Count number of rows combined
}).rename(columns={'Crypto': 'Row_Count'}).reset_index()

# Save grouped dataset
aggregated_reddit.to_csv(output_path, index=False)
print(f"Grouped Reddit data saved to '{output_path}'")
