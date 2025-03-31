from app.services.mood.models import Mood
from app.services.weather.config import MOOD_WEATHER_MAPPING
from app.services.weather.models import WeatherData


def match_mood_with_weather(mood: Mood, weather: WeatherData) -> bool:
    """
    Determine if the user's mood matches the current weather conditions
    
    Args:
        mood: The user's current mood
        weather: Current weather data
        
    Returns:
        Tuple containing:
          - Boolean indicating if the mood matches the weather
          - String explanation of the match or mismatch
    """
    # Get the mapping criteria for this mood
    mapping = MOOD_WEATHER_MAPPING.get(mood, {
        "conditions": [],
        "temperature": [],
        "match_all": False
    })
    
    # Check if weather condition matches the mood's associated conditions
    condition_match = weather.condition in mapping["conditions"]
    
    # Check if temperature category matches the mood's associated temperature ranges
    temperature_match = weather.temperature_category in mapping["temperature"]
    
    # Determine overall match based on matching criteria
    if mapping["match_all"]:
        # Must match both condition and temperature
        matches = condition_match and temperature_match
    else:
        # Must match either condition or temperature
        matches = condition_match or temperature_match
    
    return matches


