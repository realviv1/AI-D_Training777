import requests


def get_coordinates(city):

    url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}"
        "&count=1"
    )

    response = requests.get(url)

    data = response.json()

    if "results" not in data:

        return None

    result = data["results"][0]

    return (
        result["latitude"],
        result["longitude"]
    )

def get_weather(city):

    location = get_coordinates(city)

    if not location:
        return None

    latitude, longitude = location

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&daily=temperature_2m_max,"
        f"temperature_2m_min,"
        f"precipitation_sum"
        f"&forecast_days=7"
    )

    response = requests.get(url)

    return response.json()