import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app import create_app
from app.error.exceptions import WeatherAPIError
from app.services.music.models import Song
from app.services.weather.models import (
    WeatherCondition,
    WeatherData,
    WeatherTemperature,
)

client = TestClient(create_app())

# Mock data for tests
mock_weather_data = WeatherData(
    condition=WeatherCondition.CLEAR,
    temperature=22.5,
    temperature_category=WeatherTemperature.MILD,
    humidity=45.0,
    wind_speed=3.2,
    description="clear sky",
)

mock_song = Song(
    title="Happy",
    artist="Pharrell Williams",
    url="https://www.last.fm/music/Pharrell+Williams/_/Happy",
)


@pytest.mark.asyncio
@patch("app.api.endpoints.get_weather_for_city", new_callable=AsyncMock)
@patch("app.api.endpoints.get_song_recommendation", new_callable=AsyncMock)
@patch("app.api.endpoints.match_mood_with_weather")
async def test_recommendations_endpoint_success(
    mock_match_mood, mock_get_song, mock_get_weather
):
    """Test successful recommendation endpoint call"""
    # Configure mocks
    mock_get_weather.return_value = mock_weather_data
    mock_get_song.return_value = mock_song
    mock_match_mood.return_value = (True, "Your happy mood matches the weather")

    # Test API call
    response = client.post(
        "/api/v1/recommendations", json={"mood": "happy", "city": "London"}
    )

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["mood"] == "happy"
    assert data["city"] == "London"
    assert data["mood_matches_weather"] is True
    assert data["recommendation"]["title"] == "Happy"
    assert data["recommendation"]["artist"] == "Pharrell Williams"


@pytest.mark.asyncio
@patch("app.api.endpoints.get_weather_for_city", new_callable=AsyncMock)
async def test_recommendations_endpoint_city_not_found(mock_get_weather):
    """Test recommendation endpoint with invalid city"""

    # Configure mock to raise exception
    mock_get_weather.side_effect = WeatherAPIError("City 'NonExistentCity' not found")

    # Test API call
    response = client.post(
        "/api/v1/recommendations", json={"mood": "happy", "city": "NonExistentCity"}
    )

    # Verify response
    assert response.status_code == 503
    assert "Weather service error" in response.json()["detail"]


@pytest.mark.asyncio
async def test_recommendations_endpoint_invalid_mood():
    """Test recommendation endpoint with invalid mood"""
    # Test API call with invalid mood
    response = client.post(
        "/api/v1/recommendations", json={"mood": "invalid_mood", "city": "London"}
    )

    # Verify response
    assert response.status_code == 422  # Validation error
