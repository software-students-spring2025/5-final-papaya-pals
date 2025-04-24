# Fruit Casino Database Module

This module provides the MongoDB integration for the Fruit Casino project. It handles user data, game history, and statistics tracking.

## Features

- User management (create, retrieve, update)
- Game history tracking
- Bankroll management
- Statistics and leaderboards
- Hall of shame tracking (bankruptcy counts)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from src.db import Database
from src.models.game import GameType

# Initialize database
db = Database()
await db.setup()

# Create a user
user = await db.create_user("username")

# Record a game
game = await db.record_game(
    username="username",
    game_type=GameType.SLOTS,
    bet_amount=100,
    result_amount=200,
    game_details={"spins": 3}
)

# Get user stats
stats = await db.get_user_stats("username")
```

### Environment Variables

- `MONGO_URI`: MongoDB connection string (default: "mongodb://localhost:27017")

## Development

### Running Tests

```bash
pytest tests/
```

### Docker

Build the image:
```bash
docker build -t fruit-casino-db .
```

Run the container:
```bash
docker run -e MONGO_URI=mongodb://host.docker.internal:27017 fruit-casino-db
```

## API Reference

### Database Class

#### `create_user(username: str) -> User`
Create a new user with the given username.

#### `get_user(username: str) -> Optional[User]`
Get a user by their username.

#### `update_bankroll(username: str, amount: float) -> User`
Update a user's bankroll. Handles bankruptcy if balance goes below 0.

#### `record_game(username: str, game_type: GameType, bet_amount: float, result_amount: float, game_details: dict) -> GameHistory`
Record a game result and update user statistics.

#### `get_leaderboard(limit: int = 10) -> List[Dict[str, Any]]`
Get top users by bankroll.

#### `get_hall_of_shame(limit: int = 10) -> List[Dict[str, Any]]`
Get users with most bankruptcies.

#### `get_user_stats(username: str) -> Dict[str, Any]`
Get detailed statistics for a user.
