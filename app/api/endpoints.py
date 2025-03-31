from fastapi import APIRouter, HTTPException
from app.error.models import ErrorResponse
from app.services.explanation.music_explanation import generate_explanation
from app.services.mood.models import MoodRequest, MoodResponse
from app.services.weather.weather_service import get_weather_for_city
from app.services.mood.mood_service import match_mood_with_weather
from app.services.music.music_service import get_song_recommendation
from app.error.exceptions import WeatherAPIError, MusicAPIError

router = APIRouter(
    prefix="/api/v1",
    tags=["mood-weather-music"],
    responses={
        404: {"model": ErrorResponse, "description": "Not found"},
        400: {"model": ErrorResponse, "description": "Bad request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
        503: {"model": ErrorResponse, "description": "Service unavailable"}
    }
)

@router.post("/recommendations", response_model=MoodResponse, status_code=200)
async def get_mood_based_recommendation(request: MoodRequest) -> MoodResponse:
    """
    Get a song recommendation based on the user's mood and weather in their city.
    
    - Takes the user's current mood and city
    - Fetches the current weather in the city
    - Checks if the mood matches the weather
    - Provides a song recommendation to match the mood
    
    Args:
        request: The mood and city information
        
    Returns:
        A response containing weather information, mood-weather match status, and song recommendation
        
    Raises:
        HTTPException: If there's an error with the weather API, music API, or if the city is not found
    """
    try:
        # Get weather data for the city
        weather_data = await get_weather_for_city(request.city)
        
        # Check if mood matches weather
        mood_matches_weather = match_mood_with_weather(
            request.mood, 
            weather_data
        )
        
        # Get song recommendation
        song = await get_song_recommendation(request.mood)
        
        # Get explanation
        explanation = generate_explanation(
            mood=request.mood.value,
            weather=weather_data,
            song=song,
            city=request.city,
            matches=mood_matches_weather,
        )
        # Create and return the response
        return MoodResponse(
            mood=request.mood,
            city=request.city,
            weather=weather_data,
            mood_matches_weather=mood_matches_weather,
            recommendation=song,
            explanation=explanation
        )
        
    except WeatherAPIError as e:
        raise HTTPException(status_code=503, detail=f"Weather service error: {str(e)}")
    except MusicAPIError as e:
        raise HTTPException(status_code=503, detail=f"Music service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
