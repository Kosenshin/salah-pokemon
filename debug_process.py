#!/usr/bin/env python3
"""
Debug script to help identify the correct PokéMMO process name.
"""

import subprocess
import re

def check_all_processes():
    """Show all running processes to help identify PokéMMO."""
    print("🔍 Searching for potential PokéMMO processes...")
    
    try:
        # Get all processes
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            
            # Look for anything that might be related to PokéMMO
            keywords = ['pokemon', 'pokemmo', 'mmo', 'java', 'jar']
            
            print("\n📋 All processes containing potential keywords:")
            print("-" * 80)
            
            for line in lines:
                for keyword in keywords:
                    if keyword.lower() in line.lower() and 'grep' not in line.lower():
                        print(f"🎯 {line}")
                        break
            
            print("\n" + "=" * 80)
            print("💡 Look for processes that might be PokéMMO above.")
            print("   Common PokéMMO process names might be:")
            print("   - java (if it's a Java application)")
            print("   - pokemmo, PokeMMO, PokéMMO")
            print("   - Or something with a .jar file")
            
    except Exception as e:
        print(f"❌ Error getting process list: {e}")

def test_process_names():
    """Test different possible process names."""
    possible_names = [
        'pokemmo',
        'PokeMMO', 
        'PokéMMO',
        'java',
        'pokemon'
    ]
    
    print("\n🧪 Testing different process names...")
    print("-" * 50)
    
    for name in possible_names:
        try:
            result = subprocess.run(['pgrep', '-i', name], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0 and result.stdout.strip():
                process_ids = result.stdout.strip().split('\n')
                print(f"✅ Found '{name}': PIDs {', '.join(process_ids)}")
                
                # Get more details about this process
                for pid in process_ids:
                    try:
                        cmd_result = subprocess.run(['ps', '-p', pid, '-o', 'comm,args'], 
                                                 capture_output=True, text=True, timeout=5)
                        if cmd_result.returncode == 0:
                            print(f"   Details: {cmd_result.stdout.strip()}")
                    except:
                        pass
            else:
                print(f"❌ No process found for '{name}'")
                
        except Exception as e:
            print(f"💥 Error checking '{name}': {e}")

if __name__ == "__main__":
    print("🚀 PokéMMO Process Detective")
    print("=" * 50)
    
    check_all_processes()
    test_process_names()
    
    print("\n" + "=" * 50)
    print("📝 Instructions:")
    print("1. Make sure PokéMMO is running")
    print("2. Run this script again to see what process name appears")
    print("3. Update the 'process_name' in config/settings.py accordingly")
