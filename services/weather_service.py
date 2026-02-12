import requests
import time
from config import LAT, LON

# =========================
# CACHE
# =========================
CACHE = {
    "data": None,
    "expires": 0
}

CACHE_TTL = 600  # 10 minutos (segundos)


def fetch_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        "&current=temperature_2m,weathercode"
    )

    res = requests.get(url, timeout=10)
    data = res.json()["current"]

    temp = data["temperature_2m"]
    code = data["weathercode"]

    return f"{temp}°C"


def get_weather():
    now = time.time()

    # 🔹 usar cache si aún es válido
    if CACHE["data"] and now < CACHE["expires"]:
        print("⚡ Weather cache hit")
        return CACHE["data"]

    # 🔹 si expiró → pedir API
    print("🌐 Fetching weather from API")

    weather = fetch_weather()

    CACHE["data"] = weather
    CACHE["expires"] = now + CACHE_TTL

    return weather
