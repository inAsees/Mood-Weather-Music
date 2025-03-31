class BaseAPIError(Exception):
    """Base class for API-related exceptions"""
    pass

class WeatherAPIError(BaseAPIError):
    """Exception raised for errors in the weather service"""
    pass

class MusicAPIError(BaseAPIError):
    """Exception raised for errors in the music service"""
    pass

class MoodServiceError(BaseAPIError):
    """Exception raised for errors in the mood matching service"""
    pass
