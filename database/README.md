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

Build and run:
```bash
docker build -t fruit-casino-db .
docker run -d \
  --name fruit-casino-db \
  -e MONGO_URI="mongodb://mongo:27017" \
  -p 27017:27017 \
  fruit-casino-db
```

## API Examples

```python
# Create and get user
user = await db.create_user("username")
user = await db.get_user("username")

# Record game result
game = await db.record_game(
    username="player1",
    game_type=GameType.SLOTS,
    bet_amount=100.0,
    result_amount=200.0,
    game_details={"symbols": ["🍎", "🍎", "🍎"]}
)

# Get statistics
leaders = await db.get_leaderboard(limit=10)
shame = await db.get_hall_of_shame(limit=10)
stats = await db.get_user_stats("username")
