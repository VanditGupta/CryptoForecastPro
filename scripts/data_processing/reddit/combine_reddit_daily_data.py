import boto3
import pandas as pd
import os
from datetime import datetime
import json
import io

# Initialize AWS S3 client
s3 = boto3.client('s3')

# S3 bucket and folder paths
BUCKET_NAME = "crypto-sentiment-forecasting"
BASE_INPUT_PATH = "cryptoforecastpro/data/reddit_posts/daily_reddit_posts/"
BASE_OUTPUT_PATH = "cryptoforecastpro/data/reddit_posts/daily_reddit_posts/"

def read_csv_from_s3(bucket, key):
    """Read a CSV file from S3 into a Pandas DataFrame."""
    response = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(response['Body'])

def write_csv_to_s3(dataframe, bucket, key):
    """Write a Pandas DataFrame to S3 as a CSV file."""
    csv_buffer = io.StringIO()
    dataframe.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
    print(f"File saved to s3://{bucket}/{key}")

def merge_csv_files(input_prefix, output_key):
    """Merge all CSV files from an S3 prefix into a single DataFrame."""
    merged_data = []
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=input_prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith('.csv'):
                print(f"Reading file from S3: {key}")
                df = read_csv_from_s3(BUCKET_NAME, key)
                merged_data.append(df)

    if merged_data:
        merged_df = pd.concat(merged_data, ignore_index=True)
        write_csv_to_s3(merged_df, BUCKET_NAME, output_key)
        print(f"Merged file saved to S3: {output_key}")
    else:
        print(f"No CSV files found in S3 prefix: {input_prefix}")

def lambda_handler(event, context):
    """AWS Lambda handler function."""
    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    input_prefix = f"{BASE_INPUT_PATH}{current_date}/"
    output_key = f"{BASE_OUTPUT_PATH}{current_date}/combined/merged_daily_reddit_posts.csv"

    # Merge CSV files
    merge_csv_files(input_prefix, output_key)

    # Call the sentiment analysis Lambda function (if necessary)
    # You can invoke another Lambda function here if sentiment analysis needs to be done
    # response = boto3.client('lambda').invoke(
    #     FunctionName='sentiment_analysis_reddit_daily_data',
    #     InvocationType='Event',
    #     Payload=json.dumps({'bucket': BUCKET_NAME, 'key': output_key})
    # )

    return {"statusCode": 200, "body": f"Merged file saved to {output_key}"}
