import asyncio
import pyautogui
import cv2
import numpy as np
from typing import Tuple, Optional, List
import subprocess
import re
from config.settings import SCREEN_SETTINGS
from utils.logger import setup_logger

class ScreenCalibrator:
    """Handles screen size detection and window location calibration."""
    
    def __init__(self):
        self.logger = setup_logger()
        self.screen_size = None
        self.window_region = None
        
    async def calibrate(self) -> bool:
        """
        Perform full calibration: detect screen size and locate target window.
        Returns True if calibration successful, False otherwise.
        """
        self.logger.info("Starting screen calibration...")
        
        # Disable pyautogui failsafe for automation
        pyautogui.FAILSAFE = False
        
        # Step 0: Check if PokéMMO process is running
        if not await self._check_pokemmo_process():
            raise RuntimeError("PokéMMO process not found! Please start PokéMMO before running the bot.")
        
        # Step 1: Get screen dimensions
        self.screen_size = pyautogui.size()
        self.logger.info(f"Screen size detected: {self.screen_size}")
        
        # Step 2: Locate target window
        window_found = await self._locate_target_window()
        
        if window_found:
            self.logger.info(f"Calibration successful! Window region: {self.window_region}")
            return True
        else:
            self.logger.error("Calibration failed: Could not locate target window")
            return False
    
    async def _check_pokemmo_process(self) -> bool:
        """Check if PokéMMO process is running."""
        process_name = SCREEN_SETTINGS.get('process_name', 'java')
        
        try:
            # Use pgrep to find processes with the specified name (case-insensitive)
            result = subprocess.run(
                ['pgrep', '-i', process_name], 
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0 and result.stdout.strip():
                process_ids = result.stdout.strip().split('\n')
                
                # For Java processes, we need to check if it's actually PokéMMO
                if process_name.lower() == 'java':
                    pokemmo_found = False
                    for pid in process_ids:
                        try:
                            # Check the command line arguments to see if it's PokéMMO
                            cmd_result = subprocess.run(
                                ['ps', '-p', pid, '-o', 'args', '--no-headers'], 
                                capture_output=True, text=True, timeout=5
                            )
                            if cmd_result.returncode == 0:
                                cmd_line = cmd_result.stdout.strip()
                                # Check if this Java process is running PokéMMO
                                if 'pokeemu.client.Client' in cmd_line or 'PokeMMO.exe' in cmd_line:
                                    self.logger.info(f"Found PokéMMO Java process: {pid}")
                                    pokemmo_found = True
                                    break
                        except Exception as e:
                            self.logger.debug(f"Error checking Java process {pid}: {e}")
                            continue
                    
                    if pokemmo_found:
                        return True
                    else:
                        self.logger.error("Java processes found, but none are running PokéMMO")
                        return False
                else:
                    # For non-Java processes, just check if the process exists
                    self.logger.info(f"Found {process_name} process(es): {', '.join(process_ids)}")
                    return True
            else:
                self.logger.error(f"No {process_name} process found")
                return False
                
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.logger.error(f"Failed to check for {process_name} process: {e}")
            # Fallback: try using ps command with PokéMMO-specific search
            try:
                result = subprocess.run(
                    ['ps', 'aux'], 
                    capture_output=True, text=True, timeout=5
                )
                
                # Look for PokéMMO-specific indicators in the process list
                if ('pokeemu.client.Client' in result.stdout or 
                    'PokeMMO.exe' in result.stdout or
                    process_name.lower() in result.stdout.lower()):
                    self.logger.info(f"Found PokéMMO process using ps fallback")
                    return True
                else:
                    self.logger.error(f"No PokéMMO process found (ps fallback)")
                    return False
                    
            except Exception as fallback_error:
                self.logger.error(f"Process check completely failed: {fallback_error}")
                return False
    
    async def _locate_target_window(self) -> bool:
        """Locate the target application window."""
        
        # Method 1: Try to find window by title (Linux-specific)
        try:
            result = subprocess.run(
                ['xwininfo', '-name', SCREEN_SETTINGS['window_title']], 
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0:
                # Parse xwininfo output to get window geometry
                geometry = self._parse_xwininfo_output(result.stdout)
                if geometry:
                    self.window_region = geometry
                    return True
                    
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.logger.warning("xwininfo not available or timed out")
        
        # Method 2: Interactive window selection
        self.logger.info("Click on the target window to calibrate...")
        try:
            # Wait for user to click on the window
            await asyncio.sleep(2)  # Give user time to read the message
            
            # Take a screenshot and let user define the region
            screenshot = pyautogui.screenshot()
            
            # For now, use full screen as fallback
            # In a real implementation, you could use GUI for region selection
            self.window_region = (0, 0, self.screen_size.width, self.screen_size.height)
            
            self.logger.info("Using full screen as window region")
            return True
            
        except Exception as e:
            self.logger.error(f"Interactive calibration failed: {e}")
            return False
    
    def _parse_xwininfo_output(self, output: str) -> Optional[Tuple[int, int, int, int]]:
        """Parse xwininfo output to extract window geometry."""
        try:
            # Extract position and size from xwininfo output
            abs_x = re.search(r'Absolute upper-left X:\s+(\d+)', output)
            abs_y = re.search(r'Absolute upper-left Y:\s+(\d+)', output)
            width = re.search(r'Width:\s+(\d+)', output)
            height = re.search(r'Height:\s+(\d+)', output)
            
            if all([abs_x, abs_y, width, height]):
                x = int(abs_x.group(1))
                y = int(abs_y.group(1))
                w = int(width.group(1))
                h = int(height.group(1))
                
                return (x, y, w, h)
                
        except Exception as e:
            self.logger.error(f"Failed to parse xwininfo output: {e}")
            
        return None
    
    def get_window_region(self) -> Optional[Tuple[int, int, int, int]]:
        """Get the calibrated window region."""
        return self.window_region
    
    def get_screen_size(self) -> Optional[pyautogui.Size]:
        """Get the detected screen size."""
        return self.screen_size
    
    async def recalibrate_if_needed(self) -> bool:
        """Check if recalibration is needed and perform it if so."""
        current_screen_size = pyautogui.size()
        
        if self.screen_size != current_screen_size:
            self.logger.info("Screen size changed, recalibrating...")
            return await self.calibrate()
            
        return True
