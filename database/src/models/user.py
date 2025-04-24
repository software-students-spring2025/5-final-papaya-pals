"""User model for the database."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    """User model for storing user data."""
    username: str = Field(..., description="Unique username")
    bankroll: float = Field(default=1000.0, description="Current bankroll amount")
    total_winnings: float = Field(default=0.0, description="Total amount won")
    total_losses: float = Field(default=0.0, description="Total amount lost")
    bankruptcy_count: int = Field(default=0, description="Number of times gone bankrupt")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """Model configuration."""
        collection = "users"
        
    def to_dict(self) -> dict:
        """Convert model to dictionary for MongoDB storage."""
        return {
            "username": self.username,
            "bankroll": self.bankroll,
            "total_winnings": self.total_winnings,
            "total_losses": self.total_losses,
            "bankruptcy_count": self.bankruptcy_count,
            "created_at": self.created_at,
            "last_active": self.last_active
        }
