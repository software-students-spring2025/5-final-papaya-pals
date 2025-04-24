"""Game history model for MongoDB."""
from datetime import datetime
from enum import Enum
from typing import Optional, Any
from pydantic import Field
from .base import BaseDocument

class GameType(str, Enum):
    """Supported game types."""
    SLOTS = "slots"
    ROULETTE = "roulette"
    BLACKJACK = "blackjack"

class GameHistory(BaseDocument):
    """Game history document model."""
    user_id: str
    game_type: GameType
    bet_amount: float = Field(..., gt=0)
    result_amount: float
    net_profit: float = Field(default=0.0)
    game_details: dict[str, Any] = Field(default_factory=dict)
    played_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic model configuration."""
        collection = "game_history"
