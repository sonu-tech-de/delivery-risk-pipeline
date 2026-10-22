import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

conn = get_connection()
cursor = conn.cursor()

try:
   
    query = """
        SELECT w.date, w.temp_max, w.temp_min, w.precipitation, w.windspeed_max,
               h.holiday_name
        FROM weather_daily w
        LEFT JOIN holidays h ON w.date = h.date
        ORDER BY w.date
    """
    cursor.execute(query)
    df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)

    
    df["date"] = pd.to_datetime(df["date"])
    df["is_weekend"] = df["date"].dt.dayofweek >= 5
    df["is_holiday"] = df["holiday_name"].notna()
    df["high_wind_risk"] = df["windspeed_max"] >= 40   
    df["heavy_rain_risk"] = df["precipitation"] >= 5   
    df["freezing_risk"] = df["temp_min"] <= 0          

    flag_cols = ["is_weekend", "is_holiday", "high_wind_risk",
                 "heavy_rain_risk", "freezing_risk"]
    df["risk_score"] = df[flag_cols].sum(axis=1)

    print(df)

    
    clean = df.astype(object).where(df.notna(), None)

    rows = []
    for r in clean.itertuples(index=False):
        rows.append((
            r.date.date(), r.temp_max, r.temp_min, r.precipitation,
            r.windspeed_max, r.holiday_name,
            bool(r.is_weekend), bool(r.is_holiday), bool(r.high_wind_risk),
            bool(r.heavy_rain_risk), bool(r.freezing_risk), int(r.risk_score)
        ))

    insert_query = """
        INSERT INTO risk_daily
            (date, temp_max, temp_min, precipitation, windspeed_max, holiday_name,
             is_weekend, is_holiday, high_wind_risk, heavy_rain_risk,
             freezing_risk, risk_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            temp_max = VALUES(temp_max),
            temp_min = VALUES(temp_min),
            precipitation = VALUES(precipitation),
            windspeed_max = VALUES(windspeed_max),
            holiday_name = VALUES(holiday_name),
            is_weekend = VALUES(is_weekend),
            is_holiday = VALUES(is_holiday),
            high_wind_risk = VALUES(high_wind_risk),
            heavy_rain_risk = VALUES(heavy_rain_risk),
            freezing_risk = VALUES(freezing_risk),
            risk_score = VALUES(risk_score)
    """
    cursor.executemany(insert_query, rows)
    conn.commit()
    print(f"Saved {len(rows)} rows to risk_daily")

finally:
    cursor.close()
    conn.close()