import os
from urllib.parse import urlparse
import boto3
import requests

s3 = boto3.client('s3')
BUCKET_NAME = 'judgement-pdfs'

def lambda_handler(event, context):
    print(event)

    records = event['Records']
    for record in records:
        process_record(record)

def process_record(record):
    url = record['body']
    if not url:
        print("No URL found.")
        return

    # Create pdf and store in S3
    try:
        response = requests.get(url)
        response.raise_for_status()
        pdf_data = response.content

        filename = os.path.basename(urlparse(url).path)
        if not filename.endswith('.pdf'):
            filename += '.pdf'

        s3.put_object(Bucket=BUCKET_NAME, Key=filename, Body=pdf_data, ContentType='application/pdf')
        print(f"Uploaded {filename} to s3://{BUCKET_NAME}/{filename}")
    except Exception as e:
        print(f"Error processing {url}: {e}")

    # Call DS API to get the job id
    # Populate dynamodb with the job id