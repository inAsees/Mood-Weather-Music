from app.services.music.models import Song
from app.services.weather.models import WeatherData

# Explanation templates for mood-weather matching
EXPLANATION_TEMPLATES = {
    "match": """Your {mood} mood aligns well with the current {weather_desc} weather in {city}.We've recommended '{song_title}' by '{artist}' to complement your mood.""",
    "no_match": """Your {mood} mood doesn't quite match the current {weather_desc} weather in {city}.We've recommended '{song_title}' by '{artist}' to enhance your mood regardless of the weather.""",
}

def generate_explanation(
    mood: str, weather: WeatherData, song: Song, city: str, matches: bool
) -> str:
    """
    Generate a human-readable explanation of the mood-weather match

    Args:
        mood: The user's current mood
        weather: Current weather data
        city: The city name
        matches: Whether the mood matches the weather

    Returns:
        String explanation of the match or mismatch
    """
    song_title = song.title
    song_artist = song.artist

    weather_temp_category = weather.temperature_category.value
    weather_condition = weather.condition.value
    # Create a weather description string
    weather_desc = f"{weather_temp_category} and {weather_condition}"

    # Select the appropriate template based on whether there's a match
    template_key = "match" if matches else "no_match"
    template = EXPLANATION_TEMPLATES[template_key]

    # Format the explanation
    return template.format(
        mood=mood,
        weather_desc=weather_desc,
        city=city,
        song_title=song_title,
        artist=song_artist
    )
