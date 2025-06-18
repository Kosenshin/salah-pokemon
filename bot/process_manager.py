import psutil
import time
import platform
from typing import Optional, Tuple, Dict, Any
from utils.logger import setup_logger

# Windows-specific imports (will be imported only on Windows)
if platform.system() == "Windows":
    import win32gui
    import win32process
    import win32con
    import win32api


class ProcessManager:
    """Manages process detection and window handling for PokéMMO on Windows."""
    
    def __init__(self):
        self.logger = setup_logger()
        self.pokemmo_process = None
        self.pokemmo_window = None
        self.window_rect = None
        
        # Check if we're on Windows
        if platform.system() != "Windows":
            raise RuntimeError("This bot is designed to run on Windows only")
        
    def find_pokemmo_process(self) -> bool:
        """
        Find the PokéMMO process.
        
        Returns:
            bool: True if process found, False otherwise
        """
        self.logger.info("🔍 Searching for PokéMMO process...")
        
        try:
            # Common PokéMMO process names
            pokemmo_names = [
                "PokeMMO.exe",
                "pokemmo.exe", 
                "PokeMMO",
                "pokemmo"
            ]
            
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    proc_name = proc.info['name']
                    if any(name.lower() in proc_name.lower() for name in pokemmo_names):
                        self.pokemmo_process = proc
                        self.logger.info(f"✅ Found PokéMMO process: {proc_name} (PID: {proc.info['pid']})")
                        return True
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
                    
            self.logger.error("❌ PokéMMO process not found!")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error searching for PokéMMO process: {e}")
            return False
    
    def find_pokemmo_window(self) -> bool:
        """
        Find the PokéMMO window handle.
        
        Returns:
            bool: True if window found, False otherwise
        """
        self.logger.info("🔍 Searching for PokéMMO window...")
        
        try:
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if window_title:
                        windows.append((hwnd, window_title))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            # Look for PokéMMO window
            pokemmo_keywords = ["pokemmo", "pokemon"]
            
            for hwnd, title in windows:
                title_lower = title.lower()
                if any(keyword in title_lower for keyword in pokemmo_keywords):
                    self.pokemmo_window = hwnd
                    self.logger.info(f"✅ Found PokéMMO window: '{title}' (Handle: {hwnd})")
                    return True
            
            # If no window found by title, try to match by process ID
            if self.pokemmo_process:
                for hwnd, title in windows:
                    try:
                        _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                        if window_pid == self.pokemmo_process.pid:
                            self.pokemmo_window = hwnd
                            self.logger.info(f"✅ Found PokéMMO window by PID: '{title}' (Handle: {hwnd})")
                            return True
                    except:
                        continue
            
            self.logger.error("❌ PokéMMO window not found!")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error searching for PokéMMO window: {e}")
            return False
    
    def get_window_info(self) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about the PokéMMO window.
        
        Returns:
            Dict containing window information or None if window not found
        """
        if not self.pokemmo_window:
            self.logger.error("❌ No PokéMMO window handle available")
            return None
        
        try:
            # Get window rectangle
            rect = win32gui.GetWindowRect(self.pokemmo_window)
            self.window_rect = rect
            
            # Get window title
            title = win32gui.GetWindowText(self.pokemmo_window)
            
            # Calculate window dimensions
            x, y, right, bottom = rect
            width = right - x
            height = bottom - y
            
            # Get window state
            placement = win32gui.GetWindowPlacement(self.pokemmo_window)
            is_minimized = placement[1] == win32con.SW_SHOWMINIMIZED
            is_maximized = placement[1] == win32con.SW_SHOWMAXIMIZED
            
            window_info = {
                'handle': self.pokemmo_window,
                'title': title,
                'position': (x, y),
                'size': (width, height),
                'rect': rect,
                'is_minimized': is_minimized,
                'is_maximized': is_maximized,
                'is_visible': win32gui.IsWindowVisible(self.pokemmo_window)
            }
            
            self.logger.info(f"📊 Window Info:")
            self.logger.info(f"   Title: {title}")
            self.logger.info(f"   Position: {x}, {y}")
            self.logger.info(f"   Size: {width}x{height}")
            self.logger.info(f"   Minimized: {is_minimized}")
            self.logger.info(f"   Maximized: {is_maximized}")
            self.logger.info(f"   Visible: {window_info['is_visible']}")
            
            return window_info
            
        except Exception as e:
            self.logger.error(f"❌ Error getting window info: {e}")
            return None
    
    def focus_window(self) -> bool:
        """
        Focus on the PokéMMO window and bring it to foreground.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.pokemmo_window:
            self.logger.error("❌ No PokéMMO window handle available")
            return False
        
        try:
            self.logger.info("🎯 Focusing PokéMMO window...")
            
            # If window is minimized, restore it
            if win32gui.IsIconic(self.pokemmo_window):
                self.logger.debug("Restoring minimized window...")
                win32gui.ShowWindow(self.pokemmo_window, win32con.SW_RESTORE)
                time.sleep(0.5)  # Wait for restore animation
            
            # Bring window to foreground
            win32gui.SetForegroundWindow(self.pokemmo_window)
            
            # Additional methods to ensure window is focused
            win32gui.BringWindowToTop(self.pokemmo_window)
            win32gui.SetActiveWindow(self.pokemmo_window)
            
            # Verify window is now in foreground
            time.sleep(0.2)
            foreground_window = win32gui.GetForegroundWindow()
            
            if foreground_window == self.pokemmo_window:
                self.logger.info("✅ PokéMMO window focused successfully")
                return True
            else:
                self.logger.warning("⚠️ Window focus may not have worked as expected")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error focusing window: {e}")
            return False
    
    def check_pokemmo_running(self) -> bool:
        """
        Check if PokéMMO is currently running and accessible.
        
        Returns:
            bool: True if PokéMMO is running and accessible, False otherwise
        
        Raises:
            RuntimeError: If PokéMMO is not running
        """
        self.logger.info("🔄 Checking PokéMMO status...")
        
        # Step 1: Find the process
        if not self.find_pokemmo_process():
            raise RuntimeError(
                "PokéMMO process not found! Please make sure PokéMMO is running before starting the bot."
            )
        
        # Step 2: Find the window
        if not self.find_pokemmo_window():
            raise RuntimeError(
                "PokéMMO window not found! The game might be running but not visible."
            )
        
        # Step 3: Get window information
        window_info = self.get_window_info()
        if not window_info:
            raise RuntimeError(
                "Could not get PokéMMO window information!"
            )
        
        # Step 4: Focus the window
        if not self.focus_window():
            self.logger.warning("⚠️ Could not focus PokéMMO window, but continuing...")
        
        self.logger.info("✅ PokéMMO is running and accessible!")
        return True
    
    def get_window_region(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Get the window region for action targeting.
        
        Returns:
            Tuple of (x, y, width, height) or None if not available
        """
        if not self.window_rect:
            return None
        
        x, y, right, bottom = self.window_rect
        width = right - x
        height = bottom - y
        
        return (x, y, width, height)
