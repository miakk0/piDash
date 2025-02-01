import openmeteo_requests
import os
import datetime
import requests_cache
import pandas as pd
from retry_requests import retry

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
def get_weather():
    #if os.path.exists("weather.txt"): 
    #    os.remove("weather.txt")
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
        "timezone": "America/New_York",
        "forecast_days": 1,
        "models": ["gfs_hrrr"]
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    for i in range(len(params["models"])):
        response = responses[i]
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")


        # Current values. The order of variables needs to be the same as requested.
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()
        current_apparent_temperature = current.Variables(1).Value()
        current_rain = current.Variables(2).Value()
        current_showers = current.Variables(3).Value()
        current_snowfall = current.Variables(4).Value()
        current_weather_code = current.Variables(5).Value()
        current_cloud_cover = current.Variables(6).Value()

        variables = {
            "current_temperature_2m": round(current_temperature_2m,2),
            "current_apparent_temperature": current_apparent_temperature,
            "current_rain": current_rain,
            "current_showers": current_showers,
            "current_snowfall": current_snowfall,
            "current_weather_code": current_weather_code,
            "current_cloud_cover": current_cloud_cover,
        }

        print(f"Current time {current.Time()}")

        print(f"Current temperature_2m {current_temperature_2m}")
        print(f"Current apparent_temperature {current_apparent_temperature}")
        print(f"Current rain {current_rain}")
        print(f"Current showers {current_showers}")
        print(f"Current snowfall {current_snowfall}")
        print(f"Current weather_code {current_weather_code}")
        print(f"Current cloud_cover {current_cloud_cover}")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
        hourly_weather_code = hourly.Variables(2).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(3).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}

        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["apparent_temperature"] = hourly_apparent_temperature
        hourly_data["weather_code"] = hourly_weather_code
        hourly_data["cloud_cover"] = hourly_cloud_cover

        #hourly_dataframe = pd.DataFrame(data = hourly_data)
        #with open("weather.txt", 'a') as f:
        #    now = datetime.datetime.now()
        #    f.write(f"Recorded at: {now} using {params['models'][i]}\n")
        #    for name, value in variables:
        #        f.write(f"{name}: {value}\n")
        #    df_string = hourly_dataframe.to_string(header=True, index=True)
        #    f.write(df_string + "\n\n\n")
    return variables

