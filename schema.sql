CREATE DATABASE IF NOT EXISTS delivery_risk;
USE delivery_risk;

CREATE TABLE weather_daily (
    date DATE PRIMARY KEY,
    temp_max FLOAT,
    temp_min FLOAT,
    precipitation FLOAT,
    windspeed_max FLOAT,
);

CREATE TABLE holidays (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    holiday_name VARCHAR(100),
    weekday VARCHAR(20)
);

CREATE TABLE risk_daily (
    date DATE PRIMARY KEY,
    temp_max FLOAT,
    temp_min FLOAT,
    precipitation FLOAT,
    windspeed_max FLOAT,
    holiday_name VARCHAR(100),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    high_wind_risk BOOLEAN,
    heavy_rain_risk BOOLEAN,
    freezing_risk BOOLEAN,
    risk_score INT
);