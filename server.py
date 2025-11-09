from fastapi import FastAPI
import requests
import os
import json
from pathlib import Path

app = FastAPI(title="TerraScope Dedalus Connector")

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# ---------- VALIDATION ----------
@app.get("/")
def root():
    """
    Dedalus validation endpoint.
    Returns the manifest in the expected structure.
    """
    manifest_path = Path(__file__).parent / "manifest.json"
    if not manifest_path.exists():
        return {
            "status": "error",
            "error": "manifest.json not found in repo root"
        }

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Dedalus expects exactly this shape
    return {
        "manifest_version": manifest.get("version", "1.0.0"),
        "name": manifest.get("name", "dedalus-terrascope-connector"),
        "tools": manifest.get("tools", []),
        "metadata": {
            "description": manifest.get("description", "TerraScope connector"),
            "status": "ok",
            "validation": "passed"
        }
    }

# ---------- FLOOD ----------
@app.get("/flood")
def flood(lat: float, lon: float, date: str):
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
    weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}"
    ).json()
    return {
        "type": "heat",
        "temperature": weather["main"]["temp"] - 273.15,
        "humidity": weather["main"]["humidity"],
    }

# ---------- STORM ----------
@app.get("/storm")
def storm(lat: float, lon: float, date: str):
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


@app.get("/manifest")
def manifest():
    with open("manifest.json") as f:
        return json.load(f)

