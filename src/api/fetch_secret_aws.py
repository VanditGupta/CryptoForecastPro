import boto3
import json
from botocore.exceptions import ClientError

def get_secret(secret_name="cryptoforecastpro-secrets", region_name="us-east-1"):
    """
    Retrieve secrets from AWS Secrets Manager.

    Parameters:
        secret_name (str): Name of the secret in AWS Secrets Manager.
        region_name (str): AWS region where the secret is stored.

    Returns:
        dict: A dictionary of secrets.
    """
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # Retrieve the secret
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        
        # Parse and return the secret
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)  # Convert JSON string to dictionary
        else:
            print("Binary secrets are not supported in this example.")
            return None

    except ClientError as e:
        print(f"Failed to retrieve secret: {e}")
        return None


# Example usage
if __name__ == "__main__":
    secrets = get_secret()

    if secrets:
        ACCESS_TOKEN = secrets.get("ACCESS_TOKEN")
        S3_BUCKET = secrets.get("S3_BUCKET")
        CLIENT_ID = secrets.get("CLIENT_ID")
        CLIENT_SECRET = secrets.get("CLIENT_SECRET")
        USER_AGENT = secrets.get("USER_AGENT")

        print(f"Access Token: {ACCESS_TOKEN}")
        print(f"S3 Bucket: {S3_BUCKET}")
    else:
        print("Secrets retrieval failed.")
