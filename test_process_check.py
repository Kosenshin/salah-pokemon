#!/usr/bin/env python3
"""
Simple test script to verify PokéMMO process checking functionality.
"""

import asyncio
from bot.calibrator import ScreenCalibrator

async def test_process_check():
    """Test the PokéMMO process checking."""
    print("Testing PokéMMO process check...")
    
    calibrator = ScreenCalibrator()
    
    try:
        # This will raise an error if PokéMMO is not running
        result = await calibrator.calibrate()
        print(f"✅ Calibration successful: {result}")
        
        if calibrator.window_region:
            print(f"📊 Window region: {calibrator.window_region}")
        if calibrator.screen_size:
            print(f"🖥️  Screen size: {calibrator.screen_size}")
            
    except RuntimeError as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure PokéMMO is running before starting the bot!")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(test_process_check())
