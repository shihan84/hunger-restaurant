"""
Update desktop shortcut for HUNGER Billing Software v1.3
"""
import os
import win32com.client

def update_desktop_shortcut():
    """Update desktop shortcut"""
    shortcut_name = "HUNGER Billing Software.lnk"
    exe_name = "HUNGER_Billing_Software.exe"
    icon_name = "restaurant_icon.ico"

    desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
    shortcut_path = os.path.join(desktop_path, shortcut_name)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dist_path = os.path.join(current_dir, "dist")
    exe_path = os.path.join(dist_path, exe_name)
    icon_path = os.path.join(current_dir, icon_name)

    shell = win32com.client.Dispatch("WScript.Shell")

    if os.path.exists(shortcut_path):
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.IconLocation = icon_path
        shortcut.save()
        print("[OK] Desktop shortcut updated to v1.3")
    else:
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.IconLocation = icon_path
        shortcut.save()
        print("[OK] Desktop shortcut created for v1.3")
    
    print(f"Location: {shortcut_path}")
    print(f"Target: {exe_path}")
    print(f"Icon: {icon_path}")

if __name__ == "__main__":
    update_desktop_shortcut()

