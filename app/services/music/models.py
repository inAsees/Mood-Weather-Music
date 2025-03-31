from typing import Optional
from pydantic import BaseModel


class Song(BaseModel):
    """Model for song recommendation"""

    title: str
    artist: str
    url: Optional[str] = None
