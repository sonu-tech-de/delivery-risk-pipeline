import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()


query = """
    SELECT w.date, w.temp_max, w.temp_min, w.precipitation, w.windspeed_max,
        h.holiday_name
    FROM weather_daily w
    LEFT JOIN holidays h ON w.date = h.date
    ORDER BY w.date
"""
cursor.execute(query)
df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
cursor.close()
conn.close()


df["date"] = pd.to_datetime(df["date"])
df["is_weekend"] = df["date"].dt.dayofweek >= 5
df["is_holiday"] = df["holiday_name"].notna()
df["high_wind_risk"] = df["windspeed_max"] >= 40      
df["heavy_rain_risk"] = df["precipitation"] >= 5      
df["freezing_risk"] = df["temp_min"] <= 0             

flag_cols = ["is_weekend", "is_holiday", "high_wind_risk", "heavy_rain_risk", "freezing_risk"]
df["risk_score"] = df[flag_cols].sum(axis=1)

print(df)