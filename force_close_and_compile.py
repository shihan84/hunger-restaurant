"""Force close and compile"""
import subprocess
import time
import os

# Kill any running instances
subprocess.run("taskkill /F /IM HUNGER_Billing_Software.exe", shell=True, capture_output=True)
subprocess.run("taskkill /F /IM python.exe", shell=True, capture_output=True)

time.sleep(2)

# Compile
os.system("pyinstaller build_app.spec --clean")

