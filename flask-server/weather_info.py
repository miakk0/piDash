import openmeteo_requests
from datetime import datetime
from dateutil import tz
import requests_cache
from retry_requests import retry

def generate_list_of_datetime(start: int, end: int, interval: int, timezone:str):
    datetime_list = [datetime.fromtimestamp(timestamp, tz=tz.gettz(timezone)) for timestamp in range(start, end, interval)]
    return datetime_list


def get_weather():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 45.5088,
        "longitude": -73.5878,
        "current": ["temperature_2m", "apparent_temperature", "rain", "showers", "snowfall", "weather_code", "cloud_cover"],
        "hourly": ["temperature_2m", "apparent_temperature", "weather_code", "cloud_cover"],
        "timezone": "America/Montreal",
        "forecast_days": 1,
        "models": ["gfs_hrrr"]
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    for i in range(len(params["models"])):
        response = responses[i]

        # Current values. The order of variables needs to be the same as requested.
        current = response.Current()
        current_data = {params["current"][i]: current.Variables(i).Value() for i in range(len(params["current"]))}

        hourly = response.Hourly()
        hourly_data = {"date": generate_list_of_datetime(hourly.Time(), hourly.TimeEnd(), hourly.Interval(), str(response.Timezone()))}
        for i in range(len(params["hourly"])):
            hourly_data[params["hourly"][i]] = hourly.Variables(i).ValuesAsNumpy().tolist()


    return current_data, hourly_data

