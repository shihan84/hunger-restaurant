"""
Update Desktop Shortcut with Custom Icon
"""

import os
from pathlib import Path
import win32com.client

try:
    # Get paths
    desktop = Path.home() / "Desktop"
    shortcut_path = desktop / "HUNGER Billing Software.lnk"
    exe_path = Path(__file__).parent / "dist" / "HUNGER_Billing_Software.exe"
    icon_path = Path(__file__).parent / "restaurant_icon.ico"
    
    # Convert to absolute paths
    exe_path = exe_path.resolve()
    icon_path = icon_path.resolve()
    
    # Get shortcut
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(shortcut_path))
    
    # Update shortcut properties
    shortcut.Targetpath = str(exe_path)
    shortcut.WorkingDirectory = str(exe_path.parent)
    shortcut.IconLocation = str(icon_path)
    shortcut.Description = "HUNGER Family Restaurant - Billing Software"
    
    # Save shortcut
    shortcut.save()
    
    print(f"[OK] Desktop shortcut updated with restaurant icon!")
    print(f"Shortcut: {shortcut_path}")
    print(f"Icon: {icon_path}")
    print(f"Target: {exe_path}")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nNote: The shortcut may need to be manually updated.")
    print(f"Right-click on the desktop shortcut > Properties > Change Icon")
    print(f"And select: {icon_path}")

