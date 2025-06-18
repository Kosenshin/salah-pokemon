import asyncio
import pyautogui
from typing import Dict, Callable, Optional
from bot.calibrator import ScreenCalibrator
from bot.actions import ActionHandler
from config.settings import BOT_SETTINGS, CYCLE_SETTINGS
from utils.logger import setup_logger


class BotCoordinator:
    """Coordinates the bot's main action cycle and manages different components."""
    
    def __init__(self):
        self.logger = setup_logger()
        self.calibrator = ScreenCalibrator()
        self.action_handler = ActionHandler()
        self.is_running = False
        self.current_cycle = 0
        
    async def start(self):
        """Start the bot coordinator."""
        self.logger.info("Initializing Bot Coordinator...")
        
        try:
            # Step 1: Calibrate screen and locate game window
            if not await self.calibrator.calibrate():
                raise RuntimeError("Screen calibration failed")
            
            # Step 2: Initialize action handler with calibrated settings
            self.action_handler.set_window_region(self.calibrator.get_window_region())
            
            # Step 3: Start main action cycle
            self.is_running = True
            await self._run_main_cycle()
            
        except Exception as e:
            self.logger.error(f"Bot coordinator failed: {e}")
            raise
    
    async def stop(self):
        """Stop the bot coordinator."""
        self.logger.info("Stopping Bot Coordinator...")
        self.is_running = False
    
    async def _run_main_cycle(self):
        """Run the main action cycle."""
        self.logger.info("Starting main action cycle...")
        
        try:
            while self.is_running:
                self.current_cycle += 1
                self.logger.info(f"Starting cycle #{self.current_cycle}")
                
                # Execute the action sequence
                await self._execute_action_sequence()
                
                # Wait before next cycle
                await asyncio.sleep(CYCLE_SETTINGS['cycle_delay'])
                
        except KeyboardInterrupt:
            self.logger.info("Main cycle interrupted by user")
        except Exception as e:
            self.logger.error(f"Main cycle error: {e}")
            raise
        finally:
            self.is_running = False
    
    async def _execute_action_sequence(self):
        """Execute the sequence of actions for one cycle."""
        
        try:
            # Action 1: Teleport
            self.logger.info("Executing teleport action...")
            await self.action_handler.teleport()
            
            # Action 2: Walking to beach
            self.logger.info("Executing walking to beach action...")
            await self.action_handler.walking_to_beach()
            
            # Action 3: Fish
            self.logger.info("Executing fish action...")
            await self.action_handler.fish()
            
            # Future actions can be added here:
            # await self.action_handler.some_other_action()
            
        except Exception as e:
            self.logger.error(f"Action sequence failed: {e}")
            # Depending on requirements, we could retry or continue
            raise
