"""
This module provides a client for interacting with AWS DynamoDB.

The DynamoDBClient class allows performing operations such as inserting items
into DynamoDB tables. It uses the default AWS credential resolution chain to
securely obtain credentials and provides error handling for common issues.
"""

import boto3
from botocore.exceptions import BotoCoreError, ClientError

class DynamoDBClient:
    """
    A client for interacting with AWS DynamoDB to perform operations such as
    inserting items into tables.
    """

    def __init__(self):
        """
        Initialize the DynamoDB client using the default AWS credential resolution chain.

        The credentials are automatically resolved from environment variables,
        AWS credentials file, IAM roles, or other supported methods.
        """
        self.dynamodb = boto3.resource('dynamodb')

    def put_item(self, table_name, item):
        """
        Insert an item into a DynamoDB table.

        :param table_name: Name of the DynamoDB table
        :param item: A dictionary representing the item to insert
        :return: Response from DynamoDB if the operation is successful, else None
        """
        try:
            table = self.dynamodb.Table(table_name)
            response = table.put_item(Item=item)
            return response
        except (BotoCoreError, ClientError) as error:
            print(f"Error putting item into DynamoDB table: {error}")
            return None
