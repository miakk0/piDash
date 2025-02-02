import requests

# Fetch data
def read_sensor_data(esp_ip):

    data = requests.get(f"http://{esp_ip}/DHT11").json()
    return data