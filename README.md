# Delivery Risk Pipeline

A data pipeline that combines weather forecasts and public holidays for Freiburg and gives every day a delivery risk score from 0 to 5.

## Why I built this
I deliver orders by e-bike in Freiburg and work in warehouse operations. Weather and holidays change how hard a delivery day is, but nobody tracks it in one place. I built this project to practice a complete data engineering workflow: extract, transform and load. For example, during a sudden storm in November 2025, riders were overwhelmed and deliveries were delayed. If we had a system to predict this risk based on weather and holidays, we could have planned better and added extra shifts.

## What it does
1. **Extract:** loads a 7-day weather forecast for Freiburg from the Open-Meteo API
2. **Extract:** scrapes Baden-Württemberg public holidays with BeautifulSoup
3. **Load:** stores both in MySQL (`weather_daily` and `holidays`)
4. **Transform:** joins them in pandas and adds risk flags
5. **Load:** saves the daily result to `risk_daily`
6. **Orchestrate:** `run_pipeline.py` runs all steps in order and stops if one fails

## Risk flags
| Flag | Rule |
|---|---|
| high_wind_risk | max wind ≥ 40 km/h |
| heavy_rain_risk | precipitation ≥ 5 mm |
| freezing_risk | min temperature ≤ 0 °C |
| is_weekend | Saturday or Sunday |
| is_holiday | public holiday in Baden-Württemberg |

`risk_score` is the number of flags that are true (0 to 5).
These thresholds are my own estimates, not official limits, and they are easy to change.

## Tech stack
Python (pandas, requests, BeautifulSoup), MySQL, python-dotenv, Git

## Project structure
| File | Purpose |
|---|---|
| `load_weather.py` | pulls weather data from the API into MySQL |
| `scrape_holidays.py` | scrapes holidays and loads them into MySQL |
| `build_risk_table.py` | joins the data, adds flags, saves `risk_daily` |
| `run_pipeline.py` | runs the three steps in order |
| `schema.sql` | creates the database tables |

## How to run

1. Clone the repository:
```bash
git clone [https://github.com/sonu-tech-de/delivery-risk-pipeline]
cd delivery-risk-pipeline
```

2. Set up the virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create a `.env` file in the project folder with your MySQL details:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=delivery_risk
```

4. Create the tables by running `schema.sql` in your MySQL database.

5. Run the pipeline:
```bash
python run_pipeline.py
```

## What I learned
- Storing credentials in a `.env` file and keeping them out of Git
- Writing re-runnable loads with `ON DUPLICATE KEY UPDATE`
- Scraping a table with BeautifulSoup and cleaning German dates
- Splitting a pipeline into steps that stop when one fails

## What I would improve next
- Run the pipeline on a daily schedule
- Replace my guessed thresholds with real delivery data
- Add data quality checks and alerts
- Add a dashboard