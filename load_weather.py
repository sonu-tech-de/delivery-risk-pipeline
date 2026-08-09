import requests
import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv


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

load_dotenv()
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()
insert_query = """
    INSERT INTO weather_daily (date, temp_max, temp_min, precipitation, windspeed_max)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        temp_max = VALUES(temp_max),
        temp_min = VALUES(temp_min),
        precipitation = VALUES(precipitation),
        windspeed_max = VALUES(windspeed_max)
"""

for index, row in df.iterrows():
    cursor.execute(insert_query, (
        row["time"], 
        row["temperature_2m_max"], 
        row["temperature_2m_min"],
        row["precipitation_sum"], 
        row["wind_speed_10m_max"]
    ))

conn.commit()
cursor.close()
conn.close()