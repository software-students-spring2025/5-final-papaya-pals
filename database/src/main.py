"""
Main entry point for the database service.
This module initializes the database connection and keeps the service running.
"""
import asyncio
import logging
import signal
import sys
from contextlib import asynccontextmanager

from .db import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Global database instance
db = None


async def initialize_database():
    """Initialize the database connection and setup indexes."""
    global db
    try:
        logger.info("Initializing database connection...")
        db = Database()
        await db.setup()
        logger.info("Database initialized successfully")
        return db
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def shutdown_database():
    """Properly close the database connection."""
    global db
    if db and hasattr(db, "client"):
        logger.info("Closing database connection...")
        db.client.close()
        logger.info("Database connection closed")


async def keep_alive():
    """Keep the service running until interrupted."""
    try:
        while True:
            await asyncio.sleep(60)
            logger.debug("Database service is running...")
    except asyncio.CancelledError:
        logger.info("Service shutdown initiated")


async def main():
    """Main entry point for the database service."""
    # Set up signal handlers
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown_database()))

    try:
        # Initialize database
        await initialize_database()
        
        # Keep the service running
        logger.info("Database service started")
        await keep_alive()
    except Exception as e:
        logger.error(f"Error in database service: {e}")
        sys.exit(1)
    finally:
        await shutdown_database()


if __name__ == "__main__":
    asyncio.run(main())
