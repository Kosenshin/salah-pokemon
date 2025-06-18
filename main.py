import asyncio
import logging
from bot.coordinator import BotCoordinator
from utils.logger import setup_logger

async def main():
    """Main entry point for the Pokemon automation bot."""
    
    # Setup logging
    logger = setup_logger()
    logger.info("Starting Pokemon Bot v2...")
    
    try:
        # Initialize the bot coordinator
        coordinator = BotCoordinator()
        
        # Start the bot (this will handle calibration and main loop)
        await coordinator.start()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Bot crashed with error: {e}")
        raise
    finally:
        logger.info("Bot shutdown complete")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
