import pandas as pd
from datetime import datetime
import os
import subprocess

# File paths
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
reddit_posts_path = f"data/reddit_posts/daily_reddit_posts/{CURRENT_DATE}/combined/sentiment_analysis/sentiment_analyzed_reddit_posts.csv"
output_path = f"data/reddit_posts/daily_reddit_posts/{CURRENT_DATE}/combined/grouped/grouped_daily_reddit_data.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Load Reddit posts
reddit_posts = pd.read_csv(reddit_posts_path)

# Remove time part from Created_At and convert to date
reddit_posts['Created_At'] = pd.to_datetime(reddit_posts['Created_At']).dt.date

# Fill NaN values in Title and Content with a single space and ensure string type
reddit_posts['Title'] = reddit_posts['Title'].fillna(' ').astype(str)
reddit_posts['Content'] = reddit_posts['Content'].fillna(' ').astype(str)

# Define a function to calculate sentiment label based on average sentiment score
def calculate_average_label(score):
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Group Reddit data by Crypto and Created_At
aggregated_reddit = reddit_posts.groupby(['Crypto', 'Created_At']).agg({
    'Sentiment_Score': 'mean',         # Average sentiment
    'Score': 'sum',                   # Total score
    'Comments': 'sum',                # Total number of comments
    'Title': '|'.join,                # Combine titles with '|'
    'Content': '|'.join,              # Combine content with '|'
    'Crypto': 'count'                 # Count number of rows combined
}).rename(columns={'Crypto': 'Row_Count'}).reset_index()

# Calculate the average sentiment label
aggregated_reddit['Sentiment_Label'] = aggregated_reddit['Sentiment_Score'].apply(calculate_average_label)

# Save grouped dataset
aggregated_reddit.to_csv(output_path, index=False)
print(f"Grouped Reddit data saved to '{output_path}'")

# Call the merge_crypto_reddit_daily_data.py script
merge_script_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../merge_crypto_reddit_daily_data.py")
)

try:
    print("Calling merge_crypto_reddit_daily_data.py...")
    subprocess.run(["python3", merge_script_path], check=True, cwd=os.path.dirname(merge_script_path))
    print("Merging of crypto and Reddit data completed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error while running merge_crypto_reddit_daily_data.py: {e}")