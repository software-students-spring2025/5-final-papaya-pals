"""User model for MongoDB."""
from typing import List, Optional
from pydantic import Field, validator
from .base import BaseDocument

class User(BaseDocument):
    """User document model."""
    username: str = Field(..., min_length=3, max_length=50)
    bankroll: float = Field(default=1000.0, ge=0)
    shame_counter: int = Field(default=0, ge=0)
    total_winnings: float = Field(default=0.0)
    total_losses: float = Field(default=0.0)
    favorite_game: Optional[str] = None
    games_played: List[str] = Field(default_factory=list)

    @validator('username')
    def username_must_be_valid(cls, v: str) -> str:
        """Validate username format."""
        if not v.strip() or not v.replace("_", "").isalnum():
            raise ValueError('Username must be alphanumeric (underscores allowed)')
        return v.strip()

    class Config:
        """Pydantic model configuration."""
        collection = "users"
