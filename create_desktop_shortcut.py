"""
Create Desktop Shortcut for HUNGER Billing Software
"""

import os
import sys
from pathlib import Path

try:
    import win32com.client
    
    # Get paths
    desktop = Path.home() / "Desktop"
    exe_path = Path(__file__).parent / "dist" / "HUNGER_Billing_Software.exe"
    
    # Convert to absolute paths
    exe_path = exe_path.resolve()
    
    # Create shortcut
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(desktop / "HUNGER Billing Software.lnk"))
    
    # Set shortcut properties
    shortcut.Targetpath = str(exe_path)
    shortcut.WorkingDirectory = str(exe_path.parent)
    shortcut.IconLocation = str(exe_path)
    shortcut.Description = "HUNGER Family Restaurant - Billing Software"
    
    # Save shortcut
    shortcut.save()
    
    print(f"[OK] Desktop shortcut created successfully!")
    print(f"Location: {desktop / 'HUNGER Billing Software.lnk'}")
    print(f"Target: {exe_path}")
    
except ImportError:
    print("Installing pywin32...")
    os.system("pip install pywin32")
    
    # Retry after installation
    try:
        import win32com.client
        
        # Get paths
        desktop = Path.home() / "Desktop"
        exe_path = Path(__file__).parent / "dist" / "HUNGER_Billing_Software.exe"
        
        # Convert to absolute paths
        exe_path = exe_path.resolve()
        
        # Create shortcut
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(desktop / "HUNGER Billing Software.lnk"))
        
        # Set shortcut properties
        shortcut.Targetpath = str(exe_path)
        shortcut.WorkingDirectory = str(exe_path.parent)
        shortcut.IconLocation = str(exe_path)
        shortcut.Description = "HUNGER Family Restaurant - Billing Software"
        
        # Save shortcut
        shortcut.save()
        
        print(f"[OK] Desktop shortcut created successfully!")
        print(f"Location: {desktop / 'HUNGER Billing Software.lnk'}")
        print(f"Target: {exe_path}")
        
    except Exception as e:
        print(f"Error creating shortcut: {e}")
        print("\nManual shortcut creation:")
        print(f"1. Right-click on HUNGER_Billing_Software.exe in the dist folder")
        print(f"2. Select 'Create shortcut'")
        print(f"3. Move the shortcut to Desktop")

except Exception as e:
    print(f"Error: {e}")
    print("\nYou can manually create the shortcut:")
    print(f"1. Navigate to: {Path(__file__).parent / 'dist'}")
    print(f"2. Right-click on HUNGER_Billing_Software.exe")
    print(f"3. Select 'Send to' > 'Desktop (create shortcut)'")
