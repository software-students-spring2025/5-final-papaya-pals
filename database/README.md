# Fruit Casino Database

This is the database subsystem for the Fruit Casino project. It provides a MongoDB-based storage solution with models for users, game history, and statistics.

## Features

- User management (create, retrieve, update)
- Game history tracking
- Leaderboard functionality
- User statistics and analytics
- Shame counter tracking
- Bankroll management

## Models

### User
- Username (unique)
- Bankroll
- Shame counter
- Total winnings/losses
- Favorite game
- Games played history

### Game History
- Game type (slots, roulette, blackjack)
- Bet amount
- Result amount
- Net profit
- Game-specific details
- Timestamp

## Development

### Prerequisites
- Python 3.11+
- MongoDB
- Docker (optional)

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export MONGO_URI="mongodb://localhost:27017"
```

### Running Tests

```bash
python -m pytest tests/ --cov=src
```

## Docker

Build the image:
```bash
docker build -t fruit-casino-db .
```

Run the container:
```bash
docker run -d \
  --name fruit-casino-db \
  -e MONGO_URI="mongodb://mongo:27017" \
  -p 27017:27017 \
  fruit-casino-db
```

## API Documentation

### User Operations

```python
# Create user
user = await db.create_user("username")

# Get user
user = await db.get_user("username")

# Update bankroll
user = await db.update_user_bankroll("username", amount)
```

### Game Operations

```python
# Record game result
game = await db.record_game(
    username="player1",
    game_type=GameType.SLOTS,
    bet_amount=100.0,
    result_amount=200.0,
    game_details={"symbols": ["🍎", "🍎", "🍎"]}
)
```

### Statistics

```python
# Get leaderboard
leaders = await db.get_leaderboard(limit=10)

# Get hall of shame
shame = await db.get_hall_of_shame(limit=10)

# Get user statistics
stats = await db.get_user_stats("username")
```
