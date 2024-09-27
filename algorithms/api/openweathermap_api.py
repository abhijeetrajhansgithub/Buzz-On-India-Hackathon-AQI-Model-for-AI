import requests
import json


def get_pollution_data():
    api_key = '198b3a31dccbbd79f5238a2bb713fb38'
    lat = 28.6139
    lon = 77.2089
    url = fr"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract pollution stats
        pollution_info = data['list'][0]['components']  # Get the pollution components
        aqi = data['list'][0]['main']['aqi']  # Get the Air Quality Index (AQI)

        print(f"Pollution stats for New Delhi (lat: {lat}, lon: {lon}):")
        print(json.dumps(pollution_info, indent=4))  # Pretty print the pollution data
        print(f"AQI: {aqi}")

        return pollution_info
    else:
        print(f"Failed to fetch data: {response.status_code}")


# print(get_pollution_data())
