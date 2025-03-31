import httpx
import random
import logging
from typing import Dict, Any, List
from app.error.exceptions import MusicAPIError
from app.services.mood.models import Mood
from app.services.music.config import LASTFM_API_KEY, LASTFM_BASE_URL, MOOD_MUSIC_TAGS
from app.services.music.models import Song

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_song_recommendation(mood: Mood) -> Song:
    """
    Get a song recommendation based on the user's mood using the Last.fm API
    
    Args:
        mood: The user's current mood
        
    Returns:
        Song object containing the recommended song information
        
    Raises:
        MusicAPIError: If there's an error retrieving data from the Last.fm API
    """
    if not LASTFM_API_KEY:
        logger.error("Last.fm API key not found in environment variables")
        raise MusicAPIError("Last.fm API key is not configured")
    
    # Get tags associated with the mood
    mood_tags = MOOD_MUSIC_TAGS.get(mood, ["happy"])
    
    # Randomly select one of the tags for variety
    selected_tag = random.choice(mood_tags)
    
    try:
        # Get tracks for the selected tag
        tracks = await get_top_tracks_by_tag(selected_tag)
        
        if not tracks:
            # Try with a different tag if no tracks found
            alternative_tag = mood_tags[0] if len(mood_tags) > 0 else "pop"
            tracks = await get_top_tracks_by_tag(alternative_tag)
            
            if not tracks:
                # Fallback to a generic recommendation if still no tracks
                return Song(
                    title="Happy",
                    artist="Pharrell Williams",
                    url="https://www.last.fm/music/Pharrell+Williams/_/Happy",
                )
        
        # Select a random track from the top tracks
        track = random.choice(tracks[:10] if len(tracks) > 10 else tracks)
        
        return Song(
            title=track.get("name", "Unknown Title"),
            artist=track.get("artist", {}).get("name", "Unknown Artist"),
            url=track.get("url", None),
        )
        
    except Exception as e:
        logger.error(f"Error getting song recommendation: {e}")
        raise MusicAPIError(f"Error getting song recommendation: {str(e)}")

async def get_top_tracks_by_tag(tag: str) -> List[Dict[str, Any]]:
    """
    Get top tracks for a specific tag from Last.fm API
    
    Args:
        tag: The music tag to search for
        
    Returns:
        List of track data dictionaries
        
    Raises:
        MusicAPIError: If there's an error with the Last.fm API request
    """
    params = {
        "method": "tag.gettoptracks",
        "tag": tag,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": 50
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(LASTFM_BASE_URL, params=params)
            
        response.raise_for_status()
        data = response.json()
        
        # Extract tracks from the response
        return data.get("tracks", {}).get("track", [])
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error from Last.fm API: {e}")
        raise MusicAPIError(f"Music service returned status code {e.response.status_code}")
    except httpx.RequestError as e:
        logger.error(f"Error connecting to Last.fm API: {e}")
        raise MusicAPIError("Error connecting to music service")
    except Exception as e:
        logger.error(f"Unexpected error in music service: {e}")
        raise MusicAPIError(f"Unexpected error: {str(e)}")
