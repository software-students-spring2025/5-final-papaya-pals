"""Game models for the database."""
from datetime import datetime
from enum import Enum
from typing import Any, Dict
from pydantic import BaseModel, Field


class GameType(str, Enum):
    """Enum for different types of games."""
    SLOTS = "slots"
    BLACKJACK = "blackjack"
    ROULETTE = "roulette"


class GameHistory(BaseModel):
    """Model for storing game history."""
    username: str = Field(..., description="Username of the player")
    game_type: GameType = Field(..., description="Type of game played")
    bet_amount: float = Field(..., description="Amount bet")
    result_amount: float = Field(..., description="Amount won or lost")
    net_profit: float = Field(..., description="Net profit (positive) or loss (negative)")
    bankroll_after: float = Field(..., description="Bankroll after the game")
    game_details: Dict[str, Any] = Field(default_factory=dict, description="Game-specific details")
    played_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """Model configuration."""
        collection = "game_history"
        
    def to_dict(self) -> dict:
        """Convert model to dictionary for MongoDB storage."""
        return {
            "username": self.username,
            "game_type": self.game_type,
            "bet_amount": self.bet_amount,
            "result_amount": self.result_amount,
            "net_profit": self.net_profit,
            "bankroll_after": self.bankroll_after,
            "game_details": self.game_details,
            "played_at": self.played_at
        }
