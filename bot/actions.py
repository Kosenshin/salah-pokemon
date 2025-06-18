import asyncio
import pyautogui
from typing import Tuple, Optional
from utils.logger import setup_logger
from config.settings import BOT_SETTINGS, ACTION_SETTINGS


class ActionHandler:
    """Handles all bot actions like teleport, movement, etc."""
    
    def __init__(self):
        self.logger = setup_logger()
        self.window_region = None
        
        # Disable pyautogui failsafe for automation
        pyautogui.FAILSAFE = False
        
        # Set default delays
        pyautogui.PAUSE = BOT_SETTINGS.get('action_delay', 0.1)
    
    def set_window_region(self, window_region: Optional[Tuple[int, int, int, int]]):
        """Set the window region for actions."""
        self.window_region = window_region
        self.logger.info(f"Action handler window region set to: {window_region}")
    
    async def teleport(self):
        """
        Execute teleport action by pressing the configured key and waiting.
        """
        self.logger.info("🔄 Starting teleport action...")
        
        try:
            # Get teleport settings
            teleport_key = ACTION_SETTINGS['teleport']['key']
            wait_time = ACTION_SETTINGS['teleport']['wait_time']
            
            # Press the teleport key
            self.logger.debug(f"Pressing key '{teleport_key}' for teleport")
            pyautogui.press(teleport_key)
            
            # Wait for teleport to complete
            self.logger.debug(f"Waiting {wait_time} seconds for teleport to complete...")
            await asyncio.sleep(wait_time)
            
            self.logger.info("✅ Teleport action completed successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Teleport action failed: {e}")
            raise
    
    async def walking_to_beach(self):
        """
        Execute walking to beach sequence:
        - Down arrow for 4 seconds
        - Left arrow for 2 seconds  
        - Down arrow for 1 second
        - Right arrow for 2 seconds
        - Down arrow for 1 second
        """
        self.logger.info("🏖️ Starting walking to beach action...")
        
        try:
            # Step 1: Down for 4 seconds
            self.logger.debug("Step 1: Walking down for 4 seconds")
            await self.press_key('down', 4.0)
            
            # Step 2: Left for 2 seconds
            self.logger.debug("Step 2: Walking left for 2 seconds")
            await self.press_key('left', 2.0)
            
            # Step 3: Down for 1 second
            self.logger.debug("Step 3: Walking down for 1 second")
            await self.press_key('down', 1.0)
            
            # Step 4: Right for 2 seconds
            self.logger.debug("Step 4: Walking right for 2 seconds")
            await self.press_key('right', 2.0)
            
            # Step 5: Down for 1 second
            self.logger.debug("Step 5: Walking down for 1 second")
            await self.press_key('down', 1.0)
            
            self.logger.info("✅ Walking to beach action completed successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Walking to beach action failed: {e}")
            raise
    
    async def fish(self):
        """
        Execute fish action by pressing the 'z' key.
        """
        self.logger.info("🎣 Starting fish action...")
        
        try:
            # Press the 'z' key to start fishing
            self.logger.debug("Pressing key 'z' to fish")
            pyautogui.press('z')
            
            self.logger.info("✅ Fish action completed successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Fish action failed: {e}")
            raise
    
    async def press_key(self, key: str, hold_duration: float = 0):
        """
        Press a key with optional hold duration.
        
        Args:
            key: The key to press (e.g., '4', 'space', 'w', etc.)
            hold_duration: How long to hold the key (0 for instant press)
        """
        try:
            if hold_duration > 0:
                self.logger.debug(f"Holding key '{key}' for {hold_duration} seconds")
                pyautogui.keyDown(key)
                await asyncio.sleep(hold_duration)
                pyautogui.keyUp(key)
            else:
                self.logger.debug(f"Pressing key '{key}'")
                pyautogui.press(key)
                
        except Exception as e:
            self.logger.error(f"Failed to press key '{key}': {e}")
            raise
    
    async def click_at_position(self, x: int, y: int, button: str = 'left', clicks: int = 1):
        """
        Click at a specific position.
        
        Args:
            x, y: Screen coordinates to click
            button: Mouse button ('left', 'right', 'middle')
            clicks: Number of clicks
        """
        try:
            self.logger.debug(f"Clicking at position ({x}, {y}) with {button} button, {clicks} clicks")
            pyautogui.click(x, y, clicks=clicks, button=button)
            
        except Exception as e:
            self.logger.error(f"Failed to click at position ({x}, {y}): {e}")
            raise
    
    async def wait(self, duration: float):
        """
        Wait for a specified duration.
        
        Args:
            duration: Time to wait in seconds
        """
        self.logger.debug(f"Waiting {duration} seconds...")
        await asyncio.sleep(duration)
