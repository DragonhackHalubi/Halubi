import requests
import os

url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"


def get_city_coordinates(city_name: str, token: str):
    """Calls the API for city locations and extract the coordinates fo the city."""

    headers = {
        "accept": "application/vnd.amadeus+json",
        "Authorization": f"Bearer {token}"
    }

    querystring = {
        "keyword": city_name,
        "max": "10"
    }

    response = requests.get(url, headers=headers, params=querystring)

    coordinates = response.json()["data"][0]["geoCode"]


    return coordinates