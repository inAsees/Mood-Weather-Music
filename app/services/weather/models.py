from enum import Enum
from pydantic import BaseModel


class WeatherCondition(str, Enum):
    """Enumeration of possible weather conditions"""

    CLEAR = "clear"
    CLOUDS = "clouds"
    RAIN = "rain"
    THUNDERSTORM = "thunderstorm"
    SNOW = "snow"
    MIST = "mist"
    FOG = "fog"
    DRIZZLE = "drizzle"


class WeatherTemperature(str, Enum):
    """Classification of temperature ranges"""

    FREEZING = "freezing"
    COLD = "cold"
    COOL = "cool"
    MILD = "mild"
    WARM = "warm"
    HOT = "hot"


class WeatherData(BaseModel):
    """Model for weather data retrieved from external API"""

    condition: WeatherCondition
    temperature: float
    temperature_category: WeatherTemperature
    humidity: float
    wind_speed: float
    description: str
