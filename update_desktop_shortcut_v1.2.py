"""
Update desktop shortcut for HUNGER Billing Software v1.2
"""
import os
import win32com.client

def update_desktop_shortcut():
    """
    Updates the desktop shortcut for HUNGER_Billing_Software.exe to point to the latest compiled version.
    If the shortcut doesn't exist, it creates a new one.
    """
    shortcut_name = "HUNGER Billing Software.lnk"
    exe_name = "HUNGER_Billing_Software.exe"
    icon_name = "restaurant_icon.ico"

    # Get paths
    desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
    shortcut_path = os.path.join(desktop_path, shortcut_name)
    
    # Assuming the script is run from the project root, and exe is in dist/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dist_path = os.path.join(current_dir, "dist")
    exe_path = os.path.join(dist_path, exe_name)
    icon_path = os.path.join(current_dir, icon_name)

    shell = win32com.client.Dispatch("WScript.Shell")

    if os.path.exists(shortcut_path):
        # Update existing shortcut
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.IconLocation = icon_path
        shortcut.save()
        print(f"[OK] Desktop shortcut updated to v1.2")
        print(f"Location: {shortcut_path}")
    else:
        # Create new shortcut
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.IconLocation = icon_path
        shortcut.save()
        print(f"[OK] Desktop shortcut created for v1.2")
        print(f"Location: {shortcut_path}")
    
    print(f"Target: {exe_path}")
    print(f"Icon: {icon_path}")
    

if __name__ == "__main__":
    update_desktop_shortcut()

