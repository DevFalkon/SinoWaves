import subprocess
import time
import os
from sys import argv

subprocess.run("python -m venv env", shell=True)
print('setting up virtual python environment')
subprocess.run("env\\Scripts\\pip.exe install pygame pytube pyinstaller", shell=True)
subprocess.run("env\\Scripts\\pyinstaller.exe\
 main.py --onefile --noconsole --clean --icon=Graphics\\icon.ico", shell=True)
os.replace("dist\\main.exe", "main.exe")
os.remove("main.py")
os.remove("main.spec")
subprocess.run("rmdir /s /Q env", shell=True)
subprocess.run("rmdir /s /Q build", shell=True)
subprocess.run("rmdir /s /Q dist", shell=True)
print("done")
for i in range(5):
    print(f"closing in {5-i}s")
    time.sleep(1)

os.remove(argv[0])
