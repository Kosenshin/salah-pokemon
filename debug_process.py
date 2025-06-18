#!/usr/bin/env python3
"""
Debug script to test PokéMMO process detection and window management.
"""

import asyncio
import sys
import platform
from bot.process_manager import ProcessManager
from utils.logger import setup_logger


async def main():
    """Debug the process manager functionality."""
    
    logger = setup_logger()
    logger.info("🐛 Starting PokéMMO Process Debug Session...")
    
    # Check if running on Windows
    if platform.system() != "Windows":
        logger.error("❌ This bot only works on Windows!")
        logger.info("💡 Current OS detected: " + platform.system())
        return
    
    try:
        # Initialize process manager
        logger.info("Initializing Process Manager...")
        process_manager = ProcessManager()
        
        # Test process detection and window management
        logger.info("Testing PokéMMO detection...")
        
        # This will raise an error if PokéMMO is not running
        success = process_manager.check_pokemmo_running()
        
        if success:
            logger.info("🎉 All checks passed!")
            
            # Get and display window region for actions
            region = process_manager.get_window_region()
            if region:
                logger.info(f"🎯 Window region for actions: {region}")
                logger.info("   This region will be used for targeting bot actions")
            
            logger.info("✅ Debug session completed successfully!")
        
    except RuntimeError as e:
        logger.error(f"❌ Runtime Error: {e}")
        logger.info("💡 Make sure PokéMMO is running and try again")
        return 1
        
    except Exception as e:
        logger.error(f"❌ Unexpected error during debug: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
