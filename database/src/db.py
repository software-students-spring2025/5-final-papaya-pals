"""Database module for MongoDB operations."""
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from .models.user import User
from .models.game import GameType, GameHistory


class Database:
    """Database class for handling MongoDB operations."""
    
    def __init__(self, uri: Optional[str] = None):
        """Initialize database connection."""
        self.uri = uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(self.uri)
        self.db = self.client.fruit_casino
        
    async def setup(self):
        """Set up database indexes and constraints."""
        # Create unique index on username
        await self.db[User.Config.collection].create_index("username", unique=True)
        
        # Create indexes for game history
        await self.db[GameHistory.Config.collection].create_index([
            ("username", 1),
            ("played_at", -1)
        ])
        
    async def create_user(self, username: str) -> User:
        """Create a new user."""
        user = User(username=username)
        try:
            await self.db[User.Config.collection].insert_one(user.to_dict())
        except DuplicateKeyError:
            raise ValueError(f"Username {username} already exists")
        return user
    
    async def get_user(self, username: str) -> Optional[User]:
        """Get user by username."""
        doc = await self.db[User.Config.collection].find_one({"username": username})
        return User(**doc) if doc else None
    
    async def update_bankroll(self, username: str, amount: float) -> User:
        """Update user's bankroll."""
        user = await self.get_user(username)
        if not user:
            raise ValueError(f"User {username} not found")
        
        # Update bankroll and track bankruptcy if applicable
        new_bankroll = user.bankroll + amount
        bankruptcy_update = {}
        if new_bankroll <= 0:
            new_bankroll = 1000.0  # Reset bankroll
            bankruptcy_update = {"bankruptcy_count": user.bankruptcy_count + 1}
        
        # Update user document
        updates = {
            "$set": {
                "bankroll": new_bankroll,
                "last_active": datetime.utcnow(),
                **bankruptcy_update
            }
        }
        await self.db[User.Config.collection].update_one(
            {"username": username},
            updates
        )
        
        # Return updated user
        return await self.get_user(username)
    
    async def record_game(
        self,
        username: str,
        game_type: GameType,
        bet_amount: float,
        result_amount: float,
        game_details: Dict[str, Any]
    ) -> GameHistory:
        """Record a game result."""
        user = await self.get_user(username)
        if not user:
            raise ValueError(f"User {username} not found")
        
        # Calculate net profit and new bankroll
        net_profit = result_amount - bet_amount
        new_bankroll = user.bankroll + net_profit
        
        # Update user statistics
        updates = {
            "$set": {
                "bankroll": new_bankroll,
                "last_active": datetime.utcnow()
            }
        }
        
        # Update win/loss statistics
        if net_profit > 0:
            updates["$inc"] = {"total_winnings": net_profit}
        else:
            updates["$inc"] = {"total_losses": abs(net_profit)}
        
        await self.db[User.Config.collection].update_one(
            {"username": username},
            updates
        )
        
        # Record game history
        game = GameHistory(
            username=username,
            game_type=game_type,
            bet_amount=bet_amount,
            result_amount=result_amount,
            net_profit=net_profit,
            bankroll_after=new_bankroll,
            game_details=game_details
        )
        
        result = await self.db[GameHistory.Config.collection].insert_one(game.to_dict())
        return game
    
    async def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top users by bankroll."""
        cursor = self.db[User.Config.collection].find().sort("bankroll", -1).limit(limit)
        return [doc async for doc in cursor]
    
    async def get_hall_of_shame(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get users with most bankruptcies."""
        cursor = self.db[User.Config.collection].find().sort("bankruptcy_count", -1).limit(limit)
        return [doc async for doc in cursor]
    
    async def get_user_stats(self, username: str) -> Dict[str, Any]:
        """Get detailed statistics for a user."""
        user = await self.get_user(username)
        if not user:
            raise ValueError(f"User {username} not found")
        
        # Get game history
        cursor = self.db[GameHistory.Config.collection].find(
            {"username": username}
        ).sort("played_at", -1)
        
        games = [game async for game in cursor]
        
        return {
            "user": user.to_dict(),
            "total_games": len(games),
            "recent_games": games[:10],
            "biggest_win": max((game["net_profit"] for game in games), default=0),
            "biggest_loss": min((game["net_profit"] for game in games), default=0)
        }
