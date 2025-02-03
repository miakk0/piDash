import requests

# Fetch data
def read_sensor_data(esp_ip):
    data = requests.get(f"http://{esp_ip}/DHT11").json()
    return data

def press_windows_power_button(esp_ip):
    data = requests.get(f"http://{esp_ip}/button").json()
    return data