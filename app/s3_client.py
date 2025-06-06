"""
This module provides a client for interacting with AWS S3.

The S3Client class allows uploading and downloading files to and from S3 buckets.
It uses the default AWS credential resolution chain to securely obtain credentials
and provides error handling for common issues such as missing files or invalid credentials.
"""

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class S3Client:
    """
    A client for interacting with AWS S3 to upload and download resources.
    """

    def __init__(self):
        """
        Initialize the S3 client using the default AWS credential resolution chain.

        The credentials are automatically resolved from environment variables,
        AWS credentials file, IAM roles, or other supported methods.
        """
        self.s3 = boto3.client('s3')

    def download_file(self, bucket_name, object_name, file_name):
        """
        Download a file from an S3 bucket.

        :param bucket_name: Name of the S3 bucket
        :param object_name: S3 object name
        :param file_name: Path to save the downloaded file
        :return: True if the file was downloaded successfully, else False
        """
        try:
            self.s3.download_file(bucket_name, object_name, file_name)
            print(f"File {object_name} downloaded from {bucket_name} to {file_name}")
            return True
        except FileNotFoundError:
            print(f"The file {file_name} could not be downloaded.")
            return False
        except NoCredentialsError:
            print("Credentials not available.")
            return False
        except PartialCredentialsError:
            print("Incomplete AWS credentials provided.")
            return False

    def upload_pdf_data(self, bucket_name, object_name, pdf_data, content_type):
        """
        Upload PDF data directly to an S3 bucket.

        :param pdf_data: Binary data of the PDF file
        :param bucket_name: Name of the S3 bucket
        :param object_name: S3 object name (key) where the PDF will be stored
        :return: True if the PDF data was uploaded successfully, else False
        """
        try:
            self.s3.put_object(Bucket=bucket_name, Key=object_name,
                               Body=pdf_data, ContentType=content_type)
            print(f"PDF data uploaded to {bucket_name}/{object_name}")
            return True
        except NoCredentialsError:
            print("Credentials not available.")
            return False
        except PartialCredentialsError:
            print("Incomplete AWS credentials provided.")
            return False
        # pylint: disable=broad-exception-caught
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
