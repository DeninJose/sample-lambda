"""
Module: lambda_function

This module contains the implementation of an AWS Lambda function that processes
SQS events containing URLs of PDF files. The function downloads the PDF files,
uploads them to an S3 bucket, and logs the results.

Functions:
    - lambda_handler(event, context): Entry point for the Lambda function.
    - process_record(record): Processes a single SQS record by downloading and
      uploading the PDF file to S3.

Dependencies:
    - boto3: AWS SDK for Python, used for interacting with S3.
    - requests: Library for making HTTP requests to download PDF files.
    - os, urllib.parse: Standard Python libraries for file and URL handling.

Environment Variables:
    - BUCKET_NAME: The name of the S3 bucket where the PDF files will be uploaded.

Usage:
    This module is designed to be deployed as an AWS Lambda function. It expects
    SQS events as input, with each event containing a 'Records' key that holds
    a list of messages. Each message should have a 'body' key containing the URL
    of the PDF file to be processed.
"""

import os
from urllib.parse import urlparse
import json
import boto3
import requests

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('judgements-table')

INPUT_BUCKET_NAME = 'judgement-pdfs'
OUTPUT_BUCKET_NAME = 'judgement-jsons'

DS_API_URL = 'https://jsonplaceholder.typicode.com/posts'


def lambda_handler(event, _):
    """
    AWS Lambda handler function.

    Processes incoming SQS events containing URLs, downloads the corresponding
    PDF files, and uploads them to an S3 bucket.

    Args:
        event (dict): The event data passed to the Lambda function, typically
                      containing a 'Records' key with a list of SQS messages.
        _ (object): The Lambda context object (not used in this function).

    Returns:
        None
    """
    print(event)

    records = event['Records']
    for record in records:
        process_record(record)

def process_record(record):
    """
    Processes a single SQS record.

    Downloads the PDF file from the URL specified in the record, uploads it
    to the specified S3 bucket, and logs the result.

    Args:
        record (dict): A single SQS message containing a 'body' key with the URL.

    Returns:
        None
    """
    record_body = json.loads(record['body'])
    url = record_body.get('judgementPdfLink')
    if not url:
        print("Missing judgement URL.")
        return

    # Create pdf and store in S3
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        pdf_data = response.content

        filename = os.path.basename(urlparse(url).path)
        if not filename.endswith('.pdf'):
            filename += '.pdf'

        s3.put_object(Bucket=INPUT_BUCKET_NAME, Key=f'judgements/{filename}',
                      Body=pdf_data, ContentType='application/pdf')
        print(f"Uploaded {filename} to s3://{INPUT_BUCKET_NAME}/judgements/{filename}")
    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(f"Error calling {url}: {e}")
        raise e

    # Call DS API to get the job id
    try:
        # S3 path of the uploaded input file
        input_file_path = f"s3://{INPUT_BUCKET_NAME}/judgements/{filename}"
        # S3 path for the output file
        output_file_path = f"s3://{OUTPUT_BUCKET_NAME}/judgements/{filename}"
        payload = {
            "input_file_path": input_file_path,
            "output_file_path": output_file_path,
            # REMOVE THIS LINE
            "job_id": "1234"
        }
        ds_response = requests.post(DS_API_URL, json=payload, timeout=5)
        ds_response.raise_for_status()

        # REPLACE WITH ACTUAL JOB ID
        job_id = ds_response.json().get("job_id")

        print(f"Received job ID: {job_id}")
    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(f"Error calling {DS_API_URL}: {e}")
        raise e

    # Populate DynamoDB with the job ID
    try:
        # REPLACE WITH ACTUAL JUDGEMENT ID
        judgement_id = filename.rsplit('.', 1)[0]
        status = "PROCESSING"

        table.put_item(
            Item={
                'judgementId': judgement_id,
                'status': status,
                'jobId': job_id
            }
        )
        print(
            f"Inserted entry into DynamoDB: "
            f"judgementId={judgement_id}, status={status}, jobId={job_id}"
        )

    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(f"Error inserting into DynamoDB: {e}")
        raise e
