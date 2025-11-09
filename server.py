from fastapi import FastAPI, Query
import requests
import os

app = FastAPI(title="TerraScope Dedalus Connector")

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY", "")
NASA_POWER_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

# ---------- FLOOD ----------
@app.get("/flood")
def flood(lat: float, lon: float, date: str):
    """Fetch rainfall, humidity, temperature for flood prediction"""
    weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}"
    ).json()

    return {
        "type": "flood",
        "rainfall_mm": weather.get("rain", {}).get("1h", 0),
        "humidity": weather["main"]["humidity"],
        "temperature": weather["main"]["temp"] - 273.15,
        "wind_speed": weather["wind"]["speed"],
        "pressure": weather["main"]["pressure"],
    }

# ---------- WILDFIRE ----------
@app.get("/wildfire")
def wildfire(lat: float, lon: float, date: str):
    """Fetch heat + wind + humidity for wildfire prediction"""
    weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}"
    ).json()

    return {
        "type": "wildfire",
        "temperature": weather["main"]["temp"] - 273.15,
        "humidity": weather["main"]["humidity"],
        "wind_speed": weather["wind"]["speed"],
        "pressure": weather["main"]["pressure"],
    }

# ---------- HEAT ----------
@app.get("/heat")
def heat(lat: float, lon: float, date: str):
    """Fetch temperature + humidity for heat risk"""
    weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}"
    ).json()

    return {
        "type": "heat",
        "temperature": weather["main"]["temp"] - 273.15,
        "humidity": weather["main"]["humidity"],
    }

# ---------- STORM (HURRICANE / TORNADO) ----------
@app.get("/storm")
def storm(lat: float, lon: float, date: str):
    """Fetch wind + pressure data for storm prediction"""
    weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}"
    ).json()

    return {
        "type": "storm",
        "wind_speed": weather["wind"]["speed"],
        "pressure": weather["main"]["pressure"],
        "humidity": weather["main"]["humidity"],
        "temperature": weather["main"]["temp"] - 273.15,
    }

@app.get("/")
def root():
    return {"status": "TerraScope connector running", "endpoints": ["/flood", "/wildfire", "/heat", "/storm"]}
