import subprocess
import os
from sys import argv

print('setting up virtual python environment')
subprocess.run("python -m venv env", shell=True)
subprocess.run("env\\Scripts\\pip.exe install pygame pyinstaller", shell=True)
subprocess.run("env\\Scripts\\pyinstaller.exe\
 main.py --noconsole --icon=Graphics\\icon.ico", shell=True)
for i in os.listdir("dist\\main"):
    os.rename(f"dist\\main\\{i}", i)
os.remove("main.py")
os.remove("main.spec")
os.rename("main.exe", "SinoWaves.exe")
subprocess.run("rmdir /s /Q env", shell=True)
subprocess.run("rmdir /s /Q build", shell=True)
subprocess.run("rmdir /s /Q dist", shell=True)
os.remove(argv[0])
subprocess.Popen(['SinoWaves.exe'])
