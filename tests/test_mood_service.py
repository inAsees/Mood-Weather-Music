from app.services.explanation.music_explanation import generate_explanation
from app.services.mood.models import Mood
from app.services.mood.mood_service import match_mood_with_weather
from app.services.weather.models import (
    WeatherCondition,
    WeatherData,
    WeatherTemperature,
)

# Create test weather data
clear_warm_weather = WeatherData(
    condition=WeatherCondition.CLEAR,
    temperature=26.0,
    temperature_category=WeatherTemperature.WARM,
    humidity=40.0,
    wind_speed=2.5,
    description="clear sky",
)

rainy_cold_weather = WeatherData(
    condition=WeatherCondition.RAIN,
    temperature=5.0,
    temperature_category=WeatherTemperature.COLD,
    humidity=85.0,
    wind_speed=6.0,
    description="light rain",
)


def test_match_mood_with_weather_matching():
    """Test mood-weather matching with matching conditions"""
    # Test happy mood with clear warm weather (should match)
    matches = match_mood_with_weather(
        Mood.HAPPY, clear_warm_weather
    )
    assert matches is True

    # Test sad mood with rainy cold weather (should match)
    matches = match_mood_with_weather(
        Mood.SAD, rainy_cold_weather
    )
    assert matches is True


def test_match_mood_with_weather_non_matching():
    """Test mood-weather matching with non-matching conditions"""
    # Test happy mood with rainy cold weather (shouldn't match)
    matches = match_mood_with_weather(
        Mood.HAPPY, rainy_cold_weather
    )
    assert matches is False

    # Test angry mood with clear warm weather (shouldn't match)
    matches = match_mood_with_weather(
        Mood.ANGRY, clear_warm_weather
    )
    assert matches is False

def test_match_mood_with_weather_match_all_requirement():
    """Test mood-weather matching with 'match_all' requirement"""
    # Test relaxed mood with clear warm weather (should match - needs both condition AND temp)
    matches = match_mood_with_weather(
        Mood.RELAXED, clear_warm_weather
    )
    assert matches is True

    # Create mix-matched weather (clear but cold)
    clear_cold_weather = WeatherData(
        condition=WeatherCondition.CLEAR,
        temperature=5.0,
        temperature_category=WeatherTemperature.COLD,
        humidity=40.0,
        wind_speed=2.5,
        description="clear sky",
    )

    # Test relaxed mood with clear but cold weather (shouldn't match - needs both)
    matches = match_mood_with_weather(
        Mood.RELAXED, clear_cold_weather
    )
    assert matches is False


def test_generate_explanation():
    """Test explanation generation"""
    # Test matching explanation
    explanation = generate_explanation(
        mood=Mood.HAPPY, weather=clear_warm_weather, city="London", matches=True
    )
    assert "happy mood aligns well" in explanation
    assert "warm and clear" in explanation
    assert "London" in explanation

    # Test non-matching explanation
    explanation = generate_explanation(
        mood=Mood.SAD, weather=clear_warm_weather, city="Paris", matches=False
    )
    assert "sad mood doesn't quite match" in explanation
    assert "warm and clear" in explanation
    assert "Paris" in explanation
