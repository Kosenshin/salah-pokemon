#!/usr/bin/env python3
"""
Test script to check Windows imports and provide helpful error messages.
"""

import platform
import sys

def test_imports():
    """Test importing Windows-specific libraries."""
    
    print(f"🖥️  Current OS: {platform.system()}")
    print(f"🐍 Python version: {sys.version}")
    
    if platform.system() != "Windows":
        print("⚠️  Not running on Windows - Windows-specific imports will fail")
        print("💡 This is expected behavior when developing/testing on non-Windows systems")
    
    print("\n🔍 Testing Windows imports...")
    
    # Test psutil (should work on all platforms)
    try:
        import psutil
        print("✅ psutil imported successfully")
        
        # Show some running processes as a test
        process_count = len(list(psutil.process_iter()))
        print(f"📊 Found {process_count} running processes")
        
    except ImportError as e:
        print(f"❌ Failed to import psutil: {e}")
    
    # Test Windows-specific imports
    if platform.system() == "Windows":
        try:
            import win32gui
            import win32process
            import win32con
            import win32api
            print("✅ Windows API imports successful")
            
            # Test basic functionality
            windows = []
            def enum_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if title:
                        windows.append((hwnd, title))
                return True
            
            win32gui.EnumWindows(enum_callback, windows)
            print(f"📊 Found {len(windows)} visible windows")
            
            # Show first few windows as examples
            print("🪟 Example windows:")
            for i, (hwnd, title) in enumerate(windows[:5]):
                print(f"   {i+1}. {title}")
            
        except ImportError as e:
            print(f"❌ Failed to import Windows API: {e}")
            print("💡 Run: pip install pywin32")
    else:
        print("⏭️  Skipping Windows API imports (not on Windows)")
    
    print("\n" + "="*50)
    print("✅ Import test completed")

if __name__ == "__main__":
    test_imports()
