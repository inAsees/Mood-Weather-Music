from enum import Enum
from pydantic import BaseModel, Field

from app.services.music.models import Song
from app.services.weather.models import WeatherData


class Mood(str, Enum):
    """Enumeration of possible user moods"""

    HAPPY = "happy"
    SAD = "sad"
    CALM = "calm"
    ENERGETIC = "energetic"
    ROMANTIC = "romantic"
    ANGRY = "angry"
    ANXIOUS = "anxious"
    RELAXED = "relaxed"


class MoodRequest(BaseModel):
    """Model for user mood and city request"""

    mood: Mood = Field(..., description="User's current mood", examples="happy")
    city: str = Field(
        ..., description="City name for weather information", examples="new york"
    )


class MoodResponse(BaseModel):
    """Response model for the mood-based recommendation"""

    mood: Mood
    city: str
    weather: WeatherData
    mood_matches_weather: bool
    recommendation: Song
    explanation: str = Field(..., description="Explanation of the recommendation")
