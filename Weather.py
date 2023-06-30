

import requests
import json

def get_weather(api_key, city):
    base_url = "https://api.openweathermap.org/data/2.5/forecast?id=524901&appid=59b0ea11226ead5d91dbd1bdd56283c2"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        weather_data = response.json()

        if weather_data["cod"] != "404":
            main_info = weather_data["weather"][0]["main"]
            description = weather_data["weather"][0]["description"]
            temperature = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]
            wind_speed = weather_data["wind"]["speed"]

            print(f"Weather in {city}:")
            print(f"Main: {main_info}")
            print(f"Description: {description}")
            print(f"Temperature: {temperature}°C")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind_speed} m/s")
        else:
            print(f"Error: {weather_data['message']}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def main():
    api_key = "59b0ea11226ead5d91dbd1bdd56283c2"  # Replace with your OpenWeatherMap API key
    city = input("Enter the city name: ")
    get_weather(api_key, city)


if __name__ == "__main__":
    main()
