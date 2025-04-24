"""MongoDB database operations."""
import os
from typing import Optional, List, Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError
from .models.user import User
from .models.game import GameHistory, GameType

class Database:
    """Database operations class."""
    def __init__(self, uri: Optional[str] = None):
        """Initialize database connection."""
        self.client = AsyncIOMotorClient(uri or os.getenv("MONGO_URI"))
        self.db: AsyncIOMotorDatabase = self.client.fruit_casino
        self._setup_done = False

    async def setup(self):
        """Setup database indexes and constraints."""
        if self._setup_done:
            return
        
        # Create unique index on username
        await self.db[User.Config.collection].create_index(
            "username", unique=True
        )
        
        # Create indexes for game history
        await self.db[GameHistory.Config.collection].create_index([
            ("user_id", 1),
            ("game_type", 1),
            ("played_at", -1)
        ])

        self._setup_done = True

    async def create_user(self, username: str) -> User:
        """Create a new user."""
        user = User(username=username)
        try:
            result = await self.db[User.Config.collection].insert_one(user.to_dict())
            user.id = str(result.inserted_id)
            return user
        except DuplicateKeyError:
            raise ValueError(f"Username {username} already exists")

    async def get_user(self, username: str) -> Optional[User]:
        """Get user by username."""
        doc = await self.db[User.Config.collection].find_one({"username": username})
        return User(**doc) if doc else None

    async def update_user_bankroll(self, username: str, amount: float) -> User:
        """Update user's bankroll."""
        result = await self.db[User.Config.collection].find_one_and_update(
            {"username": username},
            {"$inc": {"bankroll": amount}},
            return_document=True
        )
        if not result:
            raise ValueError(f"User {username} not found")
        return User(**result)

    async def record_game(
        self, 
        username: str, 
        game_type: GameType,
        bet_amount: float,
        result_amount: float,
        game_details: dict[str, Any]
    ) -> GameHistory:
        """Record a game result."""
        user = await self.get_user(username)
        if not user:
            raise ValueError(f"User {username} not found")

        net_profit = result_amount - bet_amount
        game = GameHistory(
            user_id=str(user.id),
            game_type=game_type,
            bet_amount=bet_amount,
            result_amount=result_amount,
            net_profit=net_profit,
            game_details=game_details
        )

        # Update user statistics
        updates = {
            "$inc": {
                "bankroll": net_profit,
                "total_winnings": max(0, net_profit),
                "total_losses": abs(min(0, net_profit))
            },
            "$addToSet": {"games_played": game_type}
        }
        
        if net_profit < 0 and user.bankroll + net_profit <= 0:
            updates["$inc"]["shame_counter"] = 1

        await self.db[User.Config.collection].update_one(
            {"_id": user.id}, updates
        )
        
        # Record game history
        result = await self.db[GameHistory.Config.collection].insert_one(game.to_dict())
        game.id = str(result.inserted_id)
        return game

    async def get_leaderboard(self, limit: int = 10) -> List[User]:
        """Get top users by bankroll."""
        cursor = self.db[User.Config.collection].find().sort("bankroll", -1).limit(limit)
        return [User(**doc) async for doc in cursor]

    async def get_hall_of_shame(self, limit: int = 10) -> List[User]:
        """Get users with highest shame counter."""
        cursor = self.db[User.Config.collection].find().sort("shame_counter", -1).limit(limit)
        return [User(**doc) async for doc in cursor]

    async def get_user_stats(self, username: str) -> dict[str, Any]:
        """Get detailed user statistics."""
        pipeline = [
            {"$match": {"username": username}},
            {
                "$lookup": {
                    "from": GameHistory.Config.collection,
                    "localField": "_id",
                    "foreignField": "user_id",
                    "as": "games"
                }
            },
            {
                "$project": {
                    "username": 1,
                    "bankroll": 1,
                    "shame_counter": 1,
                    "total_winnings": 1,
                    "total_losses": 1,
                    "favorite_game": 1,
                    "total_games": {"$size": "$games"},
                    "avg_bet": {"$avg": "$games.bet_amount"},
                    "biggest_win": {"$max": "$games.net_profit"},
                    "biggest_loss": {"$min": "$games.net_profit"}
                }
            }
        ]
        
        result = await self.db[User.Config.collection].aggregate(pipeline).to_list(1)
        if not result:
            raise ValueError(f"User {username} not found")
        return result[0]
