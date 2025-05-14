"""
This module provides utility functions for making HTTP
GET and POST requests using the `requests` library.

Functions:
    - get(url, params=None, headers=None):
        Sends an HTTP GET request to the specified URL with optional parameters and headers.
        Returns the response object or None if the request fails.

    - post(url, data=None, json=None, headers=None):
        Sends an HTTP POST request to the specified URL
        with optional data, JSON payload, and headers.
        Returns the response object or None if the request fails.

"""
import requests

DEFAULT_TIMEOUT = 5  # Default timeout for requests in seconds

def get(url, params=None, headers=None, timeout=DEFAULT_TIMEOUT):

    """
    Sends a GET request to the specified URL.

    :param url: The URL to send the GET request to.
    :param params: Dictionary of URL parameters to append to the URL.
    :param headers: Dictionary of HTTP headers to send with the request.
    :param timeout: The timeout value for the request in seconds.
    :return: Response object from the GET request.
    """
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"GET request failed: {e}")
        return None


def post(url, data=None, json=None, headers=None, timeout=DEFAULT_TIMEOUT):
    """
    Sends a POST request to the specified URL.

    :param url: The URL to send the POST request to.
    :param data: Dictionary, list of tuples, bytes, or file-like object to send in the body.
    :param json: JSON data to send in the body.
    :param headers: Dictionary of HTTP headers to send with the request.
    :param timeout: The timeout value for the request in seconds.
    :return: Response object from the POST request.
    """
    try:
        response = requests.post(url, data=data, json=json, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"POST request failed: {e}")
        return None
