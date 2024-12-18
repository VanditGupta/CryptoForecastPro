import os
import pandas as pd

# Define input directory and output file path
INPUT_DIR = "data/reddit_posts/historical_reddit_posts"
OUTPUT_DIR = "data/reddit_posts/historical_reddit_posts/combined"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "merged_historical_reddit_posts.csv")

# Initialize an empty list to store DataFrames
all_data = []

# Iterate over each folder (cryptocurrency) in the input directory
for folder_name in os.listdir(INPUT_DIR):
    folder_path = os.path.join(INPUT_DIR, folder_name)
    
    # Check if it's a directory
    if os.path.isdir(folder_path):
        print(f"Processing folder: {folder_name}")
        
        # Find all CSV files in this folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                print(f"Reading file: {file_path}")
                
                # Read the CSV file into a DataFrame
                df = pd.read_csv(file_path)
                
                # Append the DataFrame to the list
                all_data.append(df)

# Concatenate all DataFrames into a single DataFrame
merged_df = pd.concat(all_data, ignore_index=True)

# Save the merged DataFrame to a CSV file
merged_df.to_csv(OUTPUT_FILE, index=False)

print(f"Merged historical Reddit posts saved to: {OUTPUT_FILE}")
