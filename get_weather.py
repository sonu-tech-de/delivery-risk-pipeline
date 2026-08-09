import requests
import pandas as pd

url = "https://api.open-meteo.com/v1/forecast" 
params = {
    "latitude" : "47.9959",
    "longitude" : "7.8522",
    "daily" : "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
    "timezone" : "Europe/Berlin"
}

response = requests.get(url, params=params)
data = response.json()["daily"]
df = pd.DataFrame(data)
print(df)