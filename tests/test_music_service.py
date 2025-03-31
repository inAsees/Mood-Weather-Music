import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.error.exceptions import MusicAPIError
from app.services.mood.models import Mood
from app.services.music.music_service import (
    get_song_recommendation,
    get_top_tracks_by_tag,
)

# Mock Last.fm API response
mock_lastfm_response = {
    "tracks": {
        "track": [
            {
                "name": "Happy",
                "artist": {
                    "name": "Pharrell Williams",
                    "mbid": "5c3e1746-1b81-4045-a38b-4d3d6b9f10ce",
                    "url": "https://www.last.fm/music/Pharrell+Williams",
                },
                "url": "https://www.last.fm/music/Pharrell+Williams/_/Happy",
                "streamable": "0",
                "image": [
                    {
                        "#text": "https://lastfm.freetls.fastly.net/i/u/34s/2a96cbd8b46e442fc41c2b86b821562f.png",
                        "size": "small",
                    },
                    {
                        "#text": "https://lastfm.freetls.fastly.net/i/u/64s/2a96cbd8b46e442fc41c2b86b821562f.png",
                        "size": "medium",
                    },
                    {
                        "#text": "https://lastfm.freetls.fastly.net/i/u/174s/2a96cbd8b46e442fc41c2b86b821562f.png",
                        "size": "large",
                    },
                    {
                        "#text": "https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
                        "size": "extralarge",
                    },
                ],
                "@attr": {"rank": "1"},
            }
        ]
    }
}


@pytest.mark.asyncio
@patch("app.services.music_service.get_top_tracks_by_tag", new_callable=AsyncMock)
async def test_get_song_recommendation_success(mock_get_tracks):
    """Test successful song recommendation"""
    # Configure mock
    mock_get_tracks.return_value = mock_lastfm_response["tracks"]["track"]

    # Test function
    result = await get_song_recommendation(Mood.HAPPY)

    # Verify result
    assert result.title == "Happy"
    assert result.artist == "Pharrell Williams"
    assert result.url == "https://www.last.fm/music/Pharrell+Williams/_/Happy"


@pytest.mark.asyncio
@patch("app.services.music_service.get_top_tracks_by_tag", new_callable=AsyncMock)
async def test_get_song_recommendation_no_tracks(mock_get_tracks):
    """Test recommendation when no tracks are found"""
    # Configure mock to return empty list
    mock_get_tracks.return_value = []

    # Test function
    result = await get_song_recommendation(Mood.HAPPY)

    # Verify result (should use fallback)
    assert result.title == "Happy"
    assert result.artist == "Pharrell Williams"


@pytest.mark.asyncio
@patch("app.services.music_service.get_top_tracks_by_tag", new_callable=AsyncMock)
async def test_get_song_recommendation_error(mock_get_tracks):
    """Test error handling in song recommendation"""
    # Configure mock to raise an exception
    mock_get_tracks.side_effect = Exception("API error")

    # Test function and expect error
    with pytest.raises(MusicAPIError) as excinfo:
        await get_song_recommendation(Mood.HAPPY)

    # Verify error message
    assert "Error getting song recommendation" in str(excinfo.value)


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_get_top_tracks_by_tag_success(mock_get):
    """Test successful track retrieval by tag"""
    # Configure mock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_lastfm_response
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    # Test function
    result = await get_top_tracks_by_tag("happy")

    # Verify result
    assert len(result) == 1
    assert result[0]["name"] == "Happy"
    assert result[0]["artist"]["name"] == "Pharrell Williams"
