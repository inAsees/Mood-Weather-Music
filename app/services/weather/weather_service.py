from typing import Dict, Any
import httpx
import logging
from app.services.weather.config import (
    OPENWEATHER_API_KEY,
    OPENWEATHER_BASE_URL,
    TEMPERATURE_RANGES,
    WEATHER_MAIN_MAPPING,
)
from app.services.weather.models import WeatherData, WeatherTemperature
from app.error.exceptions import WeatherAPIError


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_weather_for_city(city: str) -> WeatherData:
    """
    Retrieve current weather data for a specified city

    Args:
        city: Name of the city

    Returns:
        WeatherData object containing the current weather information

    Raises:
        WeatherAPIError: If there's an error retrieving data from the weather API
    """
    if not OPENWEATHER_API_KEY:
        logger.error("OpenWeather API key not found in environment variables")
        raise WeatherAPIError("OpenWeather API key is not configured")

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",  # Use metric units (Celsius)
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{OPENWEATHER_BASE_URL}/weather", params=params
            )

        if response.status_code == 404:
            logger.error(f"City '{city}' not found in OpenWeather API")
            raise WeatherAPIError(f"City '{city}' not found")

        response.raise_for_status()
        data = response.json()

        # Process the weather data
        return process_weather_data(data)

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error from OpenWeather API: {e}")
        raise WeatherAPIError(
            f"Weather service returned status code {e.response.status_code}"
        )
    except httpx.RequestError as e:
        logger.error(f"Error connecting to OpenWeather API: {e}")
        raise WeatherAPIError("Error connecting to weather service")
    except Exception as e:
        logger.error(f"Unexpected error in weather service: {e}")
        raise WeatherAPIError(f"Unexpected error: {str(e)}")


def process_weather_data(data: Dict[str, Any]) -> WeatherData:
    """
    Process raw weather data from OpenWeather API into our WeatherData model

    Args:
        data: Raw JSON data from OpenWeather API

    Returns:
        WeatherData object with processed weather information
    """
    # Extract main weather condition
    weather_main = data["weather"][0]["main"]
    condition = WEATHER_MAIN_MAPPING.get(weather_main, "clear")

    # Get temperature and categorize it
    temperature = data["main"]["temp"]
    temperature_category = categorize_temperature(temperature)

    # Create WeatherData object
    return WeatherData(
        condition=condition,
        temperature=temperature,
        temperature_category=temperature_category,
        humidity=data["main"]["humidity"],
        wind_speed=data["wind"]["speed"],
        description=data["weather"][0]["description"],
    )


def categorize_temperature(temp: float) -> WeatherTemperature:
    """
    Categorize temperature into predefined ranges

    Args:
        temp: Temperature in Celsius

    Returns:
        WeatherTemperature category
    """
    for category, (min_temp, max_temp) in TEMPERATURE_RANGES.items():
        if min_temp <= temp < max_temp:
            return category

    # Default to "mild" if outside of our defined ranges
    return WeatherTemperature.MILD
