"""Unit tests for database operations."""
import os
import uuid
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorClient
from src.db import Database
from src.models.game import GameType


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[Database, None]:
    """Database fixture for testing."""
    # Use test database with unique name to avoid conflicts
    test_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(test_uri)
    db_name = f"test_fruit_casino_{uuid.uuid4().hex}"
    
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
    username = "testuser"
    user = await db.create_user(username)
    assert user.username == username
    assert user.bankroll == 1000.0
    assert user.bankruptcy_count == 0
    
    # Test duplicate username
    with pytest.raises(ValueError):
        await db.create_user(username)


@pytest.mark.asyncio
async def test_get_user(db: Database):
    """Test user retrieval."""
    username = "testuser"
    await db.create_user(username)
    
    user = await db.get_user(username)
    assert user is not None
    assert user.username == username
    
    # Test non-existent user
    assert await db.get_user("nonexistent") is None


@pytest.mark.asyncio
async def test_update_bankroll(db: Database):
    """Test bankroll updates."""
    username = "testuser"
    user = await db.create_user(username)
    
    # Test adding money
    updated = await db.update_bankroll(username, 500)
    assert updated.bankroll == 1500.0
    
    # Test removing money
    updated = await db.update_bankroll(username, -200)
    assert updated.bankroll == 1300.0
    
    # Test bankruptcy
    updated = await db.update_bankroll(username, -2000)
    assert updated.bankroll == 1000.0  # Reset to initial amount
    assert updated.bankruptcy_count == 1


@pytest.mark.asyncio
async def test_record_game(db: Database):
    """Test game recording."""
    username = "testuser"
    await db.create_user(username)
    
    # Test winning game
    game = await db.record_game(
        username=username,
        game_type=GameType.SLOTS,
        bet_amount=100,
        result_amount=200,
        game_details={"spins": 3}
    )
    assert game.net_profit == 100
    assert game.bankroll_after == 1100.0
    
    # Verify user stats
    user = await db.get_user(username)
    assert user.bankroll == 1100.0
    assert user.total_winnings == 100
    assert user.total_losses == 0
    
    # Test losing game
    game = await db.record_game(
        username=username,
        game_type=GameType.BLACKJACK,
        bet_amount=50,
        result_amount=0,
        game_details={"cards": ["A♠", "K♥"]}
    )
    assert game.net_profit == -50
    assert game.bankroll_after == 1050.0
    
    # Verify updated stats
    user = await db.get_user(username)
    assert user.bankroll == 1050.0
    assert user.total_winnings == 100
    assert user.total_losses == 50


@pytest.mark.asyncio
async def test_leaderboard(db: Database):
    """Test leaderboard functionality."""
    # Create test users with different bankrolls
    users = [
        ("user1", 2000),
        ("user2", 1500),
        ("user3", 3000)
    ]
    
    for username, amount in users:
        user = await db.create_user(username)
        await db.update_bankroll(username, amount - user.bankroll)
    
    # Get leaderboard
    leaderboard = await db.get_leaderboard(limit=3)
    assert len(leaderboard) == 3
    assert leaderboard[0]["username"] == "user3"  # Highest bankroll
    assert leaderboard[0]["bankroll"] == 3000


@pytest.mark.asyncio
async def test_hall_of_shame(db: Database):
    """Test hall of shame functionality."""
    # Create test users with different bankruptcy counts
    users = ["user1", "user2", "user3"]
    for username in users:
        await db.create_user(username)
    
    # Cause bankruptcies
    await db.update_bankroll("user1", -2000)  # 1 bankruptcy
    await db.update_bankroll("user2", -2000)  # 1 bankruptcy
    await db.update_bankroll("user2", -2000)  # 2 bankruptcies
    
    # Get hall of shame
    shame = await db.get_hall_of_shame(limit=3)
    assert len(shame) == 3
    assert shame[0]["username"] == "user2"  # Most bankruptcies
    assert shame[0]["bankruptcy_count"] == 2


@pytest.mark.asyncio
async def test_user_stats(db: Database):
    """Test user statistics."""
    username = "testuser"
    await db.create_user(username)
    
    # Record some games
    games = [
        (GameType.SLOTS, 100, 200),    # Win 100
        (GameType.BLACKJACK, 50, 0),   # Lose 50
        (GameType.ROULETTE, 200, 400)  # Win 200
    ]
    
    for game_type, bet, result in games:
        await db.record_game(
            username=username,
            game_type=game_type,
            bet_amount=bet,
            result_amount=result,
            game_details={}
        )
    
    # Get user stats
    stats = await db.get_user_stats(username)
    assert stats["total_games"] == 3
    assert len(stats["recent_games"]) == 3
    assert stats["biggest_win"] == 200   # Roulette game
    assert stats["biggest_loss"] == -50  # Blackjack game
    assert stats["user"]["total_winnings"] == 300
    assert stats["user"]["total_losses"] == 50
