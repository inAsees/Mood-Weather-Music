from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field



    
class ErrorResponse(BaseModel):
    """Model for error responses"""
    detail: str
