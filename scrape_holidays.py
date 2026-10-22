import requests
import pandas as pd
from bs4 import BeautifulSoup
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import date
YEAR = date.today().year

GERMAN_MONTHS = {
    "Januar": 1, "Februar": 2, "März": 3, "April": 4,
    "Mai": 5, "Juni": 6, "Juli": 7, "August": 8,
    "September": 9, "Oktober": 10, "November": 11, "Dezember": 12
}


def parse_german_date(date_raw):
    day_str, month_str = date_raw.replace(".", "").split()
    return f"{YEAR}-{GERMAN_MONTHS[month_str]:02d}-{int(day_str):02d}"

url = "https://www.schulferien.org/deutschland/feiertage/baden-wuerttemberg/"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find_all("table")[0]

rows = []
for tr in table.find_all("tr"):
    cells = [td.get_text(strip=True) for td in tr.find_all("td")]
    if len(cells) >= 3 and cells[0][:2].isdigit():
        rows.append(cells[:3])

holidays_df = pd.DataFrame(rows, columns=["date_raw", "weekday", "holiday_name"])
holidays_df["date"] = holidays_df["date_raw"].apply(parse_german_date)

load_dotenv()
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

insert_query = """
    INSERT INTO holidays (date, holiday_name, weekday)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
        holiday_name = VALUES(holiday_name),
        weekday = VALUES(weekday)
"""

for _, row in holidays_df.iterrows():
    cursor.execute(insert_query, (row["date"], row["holiday_name"], row["weekday"]))

conn.commit()
print(f"Inserted/updated {cursor.rowcount} rows")
cursor.close()
conn.close()

