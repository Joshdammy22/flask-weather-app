import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from datetime import datetime

load_dotenv()
api_key = os.getenv('API_KEY')

@dataclass
class WeatherData:
    city: str
    state: str
    country: str
    date_time: str
    main: str
    description: str
    icon: str
    temperature: int
    latitude: float
    longitude: float

def get_lan_lon(city_name, state_code='', country_code='', api_key=''):
    query = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={api_key}'
    resp = requests.get(query).json()

    if resp and isinstance(resp, list) and len(resp) > 0:
        data = resp[0]
        lat, lon = data.get('lat'), data.get('lon')
        return lat, lon
    else:
        return None

def get_current_weather(lat, lon, API_KEY):
    # Make API request
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    resp = requests.get(url).json()

    # Extract relevant information
    weather_info = resp.get('weather', [])
    main_info = resp.get('main', {})
    
    # Additional information
    city = resp.get('name')
    state = resp.get('state', '')  # You may need to adjust this based on the API response
    country = resp.get('sys', {}).get('country', '')
    timestamp = resp.get('dt', '')
    latitude = resp.get('coord', {}).get('lat', 0)
    longitude = resp.get('coord', {}).get('lon', 0)


    # Format the date and time
    date_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %I:%M:%S %p')  # 12-hour format

    # Get the first weather entry (if available)
    if weather_info:
        weather_entry = weather_info[0]
        main_data = WeatherData(
            city=city,
            state=state,
            country=country,
            date_time=date_time,
            main=weather_entry.get('main'),
            description=weather_entry.get('description'),
            icon=weather_entry.get('icon'),
            temperature=int(main_info.get('temp')),
            latitude=latitude,
            longitude=longitude
        )
        return main_data
    else:
        return None

def main(city_name, state_name='', country_name=''):
    location_data = get_lan_lon(city_name, state_name, country_name, api_key)
    
    if location_data:
        lat, lon = location_data
        weather_data = get_current_weather(lat, lon, api_key)
        return weather_data
    else:
        return None
