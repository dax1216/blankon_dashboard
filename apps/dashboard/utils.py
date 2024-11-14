import requests


def get_paginated_results(api_url):
    """
    Retrieves paginated results from a DRF API.

    :param api_url: The base URL of the API to retrieve data from.
    :param offset: The offset value for pagination (default is 0).
    :param limit: The limit value for pagination (default is 10).
    :return: The API response JSON data or None if there is an error.
    """
    try:
        # Construct the full URL with the offset and limit query parameters
        # Send the GET request
        response = requests.get(api_url)

        # Check if the response status code is successful
        if response.status_code == 200:
            return response.json()  # Return the JSON data from the API response
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None