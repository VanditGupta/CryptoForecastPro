import boto3
import json
import csv
import io

# Initialize AWS S3 client
s3 = boto3.client('s3')

def process_daily_data_to_historical(daily_data):
    """
    Converts daily crypto data to a format that matches historical data.
    """
    processed_data = []
    
    for entry in daily_data['symbols']:
        symbol = entry['symbol']
        date_str = entry['date']
        close_price = float(entry['last'])
        high_price = float(entry['highest'])
        low_price = float(entry['lowest'])
        
        # Approximate open price based on daily change
        open_price = close_price * (1 - (float(entry['daily_change_percentage']) / 100))
        
        processed_data.append({
            "Date": date_str,
            "Symbol": symbol,
            "Open": open_price,
            "High": high_price,
            "Low": low_price,
            "Close": close_price
        })
    
    return processed_data

def lambda_handler(event, context):
    """
    AWS Lambda handler function for processing cryptocurrency data.
    """
    # Extract bucket and object key from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    raw_key = event['Records'][0]['s3']['object']['key']
    processed_key = raw_key.replace('raw/', 'processed_csv/').replace('.json', '.csv')
    
    try:
        # Load raw JSON data from S3
        response = s3.get_object(Bucket=bucket_name, Key=raw_key)
        raw_data = json.loads(response['Body'].read().decode('utf-8'))
        
        # Process the data
        processed_data = process_daily_data_to_historical(raw_data)

        # Convert processed data to CSV format
        csv_buffer = io.StringIO()
        fieldnames = ["Date", "Symbol", "Open", "High", "Low", "Close"]
        writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_data)

        # Save processed CSV back to S3
        s3.put_object(Bucket=bucket_name, Key=processed_key, Body=csv_buffer.getvalue())
        
        print(f"Processed data saved to s3://{bucket_name}/{processed_key}")
        return {"statusCode": 200, "body": "Processing successful."}
    except Exception as e:
        print(f"Error processing file: {e}")
        return {"statusCode": 500, "body": str(e)}
