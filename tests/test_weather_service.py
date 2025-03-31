import pytest
import httpx
from unittest.mock import patch, MagicMock
from app.error.exceptions import WeatherAPIError
from app.services.weather.weather_service import (
    categorize_temperature,
    get_weather_for_city,
    process_weather_data,
)

# Mock OpenWeather API response
mock_weather_response = {
    "weather": [
        {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
    ],
    "main": {
        "temp": 22.5,
        "feels_like": 21.8,
        "temp_min": 20.9,
        "temp_max": 23.9,
        "pressure": 1015,
        "humidity": 45,
    },
    "wind": {"speed": 3.2, "deg": 280},
    "clouds": {"all": 0},
    "dt": 1625050800,
    "sys": {"country": "GB", "sunrise": 1625019168, "sunset": 1625078532},
    "timezone": 3600,
    "id": 2643743,
    "name": "London",
    "cod": 200,
}


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_get_weather_for_city_success(mock_get):
    """Test successful weather retrieval"""
    # Configure mock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_weather_response
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    # Test function
    result = await get_weather_for_city("London")

    # Verify result
    assert result.condition == "clear"
    assert result.temperature == 22.5
    assert result.temperature_category == "mild"
    assert result.humidity == 45
    assert result.wind_speed == 3.2
    assert result.description == "clear sky"


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_get_weather_for_city_not_found(mock_get):
    """Test city not found error"""
    # Configure mock
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    # Test function and expect error
    with pytest.raises(WeatherAPIError) as excinfo:
        await get_weather_for_city("NonExistentCity")

    # Verify error message
    assert "not found" in str(excinfo.value)


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_get_weather_for_city_api_error(mock_get):
    """Test general API error"""
    # Configure mock to raise an exception
    mock_get.side_effect = httpx.RequestError("Connection error")

    # Test function and expect error
    with pytest.raises(WeatherAPIError) as excinfo:
        await get_weather_for_city("London")

    # Verify error message
    assert "Error connecting" in str(excinfo.value)


def test_process_weather_data():
    """Test weather data processing"""
    result = process_weather_data(mock_weather_response)

    assert result.condition == "clear"
    assert result.temperature == 22.5
    assert result.temperature_category == "mild"
    assert result.humidity == 45
    assert result.wind_speed == 3.2
    assert result.description == "clear sky"


def test_categorize_temperature():
    """Test temperature categorization"""
    assert categorize_temperature(-10) == "freezing"
    assert categorize_temperature(5) == "cold"
    assert categorize_temperature(15) == "cool"
    assert categorize_temperature(20) == "mild"
    assert categorize_temperature(27) == "warm"
    assert categorize_temperature(35) == "hot"
