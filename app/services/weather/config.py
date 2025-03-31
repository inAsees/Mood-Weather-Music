import os

# API Key
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# Base url
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"

# Temperature ranges in Celsius
TEMPERATURE_RANGES = {
    "freezing": (-50, 0),
    "cold": (0, 10),
    "cool": (10, 18),
    "mild": (18, 24),
    "warm": (24, 30),
    "hot": (30, 50),
}

# Mapping of OpenWeather main conditions to our conditions
WEATHER_MAIN_MAPPING = {
    "Clear": "clear",
    "Clouds": "clouds",
    "Rain": "rain",
    "Drizzle": "drizzle",
    "Thunderstorm": "thunderstorm",
    "Snow": "snow",
    "Mist": "mist",
    "Smoke": "mist",
    "Haze": "mist",
    "Dust": "mist",
    "Fog": "fog",
    "Sand": "mist",
    "Ash": "mist",
    "Squall": "thunderstorm",
    "Tornado": "thunderstorm",
}

# Mood-Weather Matching
# Define weather conditions that match each mood
MOOD_WEATHER_MAPPING = {
    "happy": {
        "conditions": ["clear", "clouds"],
        "temperature": ["mild", "warm"],
        "match_all": False,  # Match either condition OR temperature
    },
    "sad": {
        "conditions": ["rain", "drizzle", "mist", "fog"],
        "temperature": ["cold", "cool"],
        "match_all": False,
    },
    "calm": {
        "conditions": ["clear", "clouds"],
        "temperature": ["mild"],
        "match_all": True,  # Match both condition AND temperature
    },
    "energetic": {
        "conditions": ["clear"],
        "temperature": ["mild", "warm"],
        "match_all": False,
    },
    "romantic": {
        "conditions": ["clear", "drizzle"],
        "temperature": ["mild", "cool"],
        "match_all": False,
    },
    "angry": {
        "conditions": ["thunderstorm"],
        "temperature": ["hot"],
        "match_all": False,
    },
    "anxious": {
        "conditions": ["thunderstorm", "fog", "mist"],
        "temperature": ["freezing", "hot"],
        "match_all": False,
    },
    "relaxed": {
        "conditions": ["clear", "clouds"],
        "temperature": ["mild", "warm"],
        "match_all": True,
    },
}