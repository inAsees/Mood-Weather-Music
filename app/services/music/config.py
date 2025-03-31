import os


LASTFM_API_KEY = os.getenv("LASTFM_API_KEY", "")

# API Endpoints

LASTFM_BASE_URL = "https://ws.audioscrobbler.com/2.0"


# Last.fm tags for mood-based music search
MOOD_MUSIC_TAGS = {
    "happy": ["happy", "upbeat", "cheerful", "feel good"],
    "sad": ["sad", "melancholy", "heartbreak", "emotional"],
    "calm": ["calm", "chill", "peaceful", "ambient"],
    "energetic": ["energetic", "upbeat", "party", "dance"],
    "romantic": ["romantic", "love songs", "ballad"],
    "angry": ["angry", "rage", "aggressive", "metal"],
    "anxious": ["anxious", "tense", "dark", "experimental"],
    "relaxed": ["relaxed", "chill", "lounge", "acoustic"],
}
