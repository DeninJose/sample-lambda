"""
Module: pdf_downloader

This module provides functionality to download PDF files from a given URL.

Functions:
    - download_pdf(url): Downloads the content of a PDF file from the specified URL.
"""
from http_client import get


def download_pdf(url):
    """
    Downloads the content of a PDF file from the given URL.

    Args:
        url (str): The URL of the PDF file to download.

    Returns:
        bytes: The content of the downloaded PDF file as a byte string.

    Raises:
        Exception: If the HTTP request to fetch the PDF fails.
    """
    pdf_content = get(url).content
    return pdf_content
