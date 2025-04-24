"""Unit tests for database operations."""
import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorClient
from ..src.db import Database
from ..src.models.game import GameType

@pytest_asyncio.fixture
async def db() -> AsyncGenerator[Database, None]:
    """Database fixture for testing."""
    # Use test database
    test_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(test_uri)
    db_name = "test_fruit_casino"
    
    # Create test database instance
    test_db = Database(test_uri)
    test_db.db = client[db_name]
    
    await test_db.setup()
    yield test_db
    
    # Cleanup after tests
    await client.drop_database(db_name)
    await client.close()

@pytest.mark.asyncio
async def test_create_user(db: Database):
    """Test user creation."""
    username = "test_user"
    user = await db.create_user(username)
    assert user.username == username
    assert user.bankroll == 1000.0
    assert user.shame_counter == 0

    # Test duplicate username
    with pytest.raises(ValueError):
        await db.create_user(username)

@pytest.mark.asyncio
async def test_get_user(db: Database):
    """Test user retrieval."""
    username = "test_user"
    created_user = await db.create_user(username)
    
    fetched_user = await db.get_user(username)
    assert fetched_user is not None
    assert fetched_user.username == created_user.username
    assert fetched_user.bankroll == created_user.bankroll

    # Test non-existent user
    assert await db.get_user("nonexistent") is None

@pytest.mark.asyncio
async def test_update_user_bankroll(db: Database):
    """Test bankroll updates."""
    username = "test_user"
    user = await db.create_user(username)
    initial_bankroll = user.bankroll
    
    # Test adding money
    amount = 500.0
    updated_user = await db.update_user_bankroll(username, amount)
    assert updated_user.bankroll == initial_bankroll + amount

    # Test removing money
    amount = -200.0
    updated_user = await db.update_user_bankroll(username, amount)
    assert updated_user.bankroll == initial_bankroll + 500.0 + amount

@pytest.mark.asyncio
async def test_record_game(db: Database):
    """Test game recording."""
    username = "test_user"
    user = await db.create_user(username)
    
    # Test winning game
    game = await db.record_game(
        username=username,
        game_type=GameType.SLOTS,
        bet_amount=100.0,
        result_amount=200.0,
        game_details={"symbols": ["🍎", "🍎", "🍎"]}
    )
    assert game.net_profit == 100.0
    
    updated_user = await db.get_user(username)
    assert updated_user.bankroll == user.bankroll + game.net_profit
    assert updated_user.total_winnings == 100.0
    assert updated_user.total_losses == 0.0
    assert GameType.SLOTS in updated_user.games_played

    # Test losing game that causes bankruptcy
    game = await db.record_game(
        username=username,
        game_type=GameType.ROULETTE,
        bet_amount=updated_user.bankroll,
        result_amount=0.0,
        game_details={"bet": "red", "result": "black"}
    )
    
    updated_user = await db.get_user(username)
    assert updated_user.bankroll == 0.0
    assert updated_user.shame_counter == 1

@pytest.mark.asyncio
async def test_leaderboard(db: Database):
    """Test leaderboard functionality."""
    # Create test users with different bankrolls
    users = [
        ("user1", 2000.0),
        ("user2", 3000.0),
        ("user3", 1000.0)
    ]
    
    for username, amount in users:
        user = await db.create_user(username)
        await db.update_user_bankroll(username, amount - user.bankroll)
    
    leaderboard = await db.get_leaderboard(limit=3)
    assert len(leaderboard) == 3
    assert leaderboard[0].username == "user2"
    assert leaderboard[1].username == "user1"
    assert leaderboard[2].username == "user3"

@pytest.mark.asyncio
async def test_user_stats(db: Database):
    """Test user statistics."""
    username = "test_user"
    await db.create_user(username)
    
    # Record some games
    games = [
        (GameType.SLOTS, 100.0, 200.0, {"symbols": ["🍎", "🍎", "🍎"]}),
        (GameType.ROULETTE, 50.0, 0.0, {"bet": "red", "result": "black"}),
        (GameType.BLACKJACK, 200.0, 400.0, {"cards": ["A♠", "K♥"]})
    ]
    
    for game_type, bet, result, details in games:
        await db.record_game(username, game_type, bet, result, details)
    
    stats = await db.get_user_stats(username)
    assert stats["total_games"] == 3
    assert stats["biggest_win"] == 200.0  # From blackjack
    assert stats["biggest_loss"] == -50.0  # From roulette
    assert stats["avg_bet"] == pytest.approx(116.67, rel=1e-2)
