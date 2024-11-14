import requests


def get_paginated_results(api_url):
    try:
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
