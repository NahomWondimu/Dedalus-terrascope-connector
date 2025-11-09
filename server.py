from fastapi import FastAPI, Query
import requests

app = FastAPI(title="TerraScope MCP Connector")

@app.get("/flood")
def flood(lat: float, lon: float, date: str):
    weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=YOUR_KEY"
    ).json()
    return {
        "type": "flood",
        "rainfall_mm": weather.get("rain", {}).get("1h", 0),
        "humidity": weather["main"]["humidity"],
        "temperature": weather["main"]["temp"] - 273.15,
    }

@app.get("/wildfire")
def wildfire(lat: float, lon: float, date: str):
    # Example: combine FIRMS + OpenWeather
    firms = requests.get("https://firms.modaps.eosdis.nasa.gov/api/area.json?...").json()
    weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=YOUR_KEY").json()
    return {
        "type": "wildfire",
        "hotspots": len(firms.get("data", [])),
        "temperature": weather["main"]["temp"] - 273.15,
        "humidity": weather["main"]["humidity"],
        "wind_speed": weather["wind"]["speed"]
    }

@app.get("/heat")
def heat(lat: float, lon: float, date: str):
    weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=YOUR_KEY").json()
    return {
        "type": "heat",
        "temperature": weather["main"]["temp"] - 273.15,
        "humidity": weather["main"]["humidity"]
    }

@app.get("/storm")
def storm(lat: float, lon: float, date: str):
    # NOAA or OpenWeather wind data
    weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=YOUR_KEY").json()
    return {
        "type": "storm",
        "wind_speed": weather["wind"]["speed"],
        "pressure": weather["main"]["pressure"]
    }

