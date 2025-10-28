"""
Update Desktop Shortcut to v1.1
Updates the existing desktop shortcut to point to the new executable
"""

import os
import sys

try:
    import win32com.client
    
    # Paths
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    shortcut_path = os.path.join(desktop_path, "HUNGER Billing Software.lnk")
    exe_path = os.path.join(os.getcwd(), "dist", "HUNGER_Billing_Software.exe")
    
    # Get the icon path
    icon_path = os.path.join(os.getcwd(), "restaurant_icon.ico")
    
    if not os.path.exists(exe_path):
        print(f"ERROR: Executable not found at {exe_path}")
        sys.exit(1)
    
    if os.path.exists(shortcut_path):
        # Update existing shortcut
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.IconLocation = icon_path
        shortcut.save()
        print(f"[OK] Desktop shortcut updated to v1.1")
        print(f"Location: {shortcut_path}")
    else:
        # Create new shortcut
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.IconLocation = icon_path
        shortcut.save()
        print(f"[OK] Desktop shortcut created for v1.1")
        print(f"Location: {shortcut_path}")
    
    print(f"Target: {exe_path}")
    print(f"Icon: {icon_path}")
    
except ImportError:
    print("ERROR: pywin32 not installed")
    print("\nTo create the shortcut manually:")
    print(f"1. Right-click on Desktop")
    print(f"2. Select 'New' > 'Shortcut'")
    print(f"3. Browse to: {os.path.join(os.getcwd(), 'dist')}")
    print(f"4. Select: HUNGER_Billing_Software.exe")
    print(f"5. Set icon to: {icon_path}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {str(e)}")
    sys.exit(1)

