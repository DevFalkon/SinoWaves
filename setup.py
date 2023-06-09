import subprocess
import os
from sys import argv
import urllib.request
import re

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
if "del" in os.listdir():
    subprocess.run("rmdir /s /Q del", shell=True)
with open('version.txt', 'w') as file:
    html = urllib.request.urlopen("https://github.com/DevFalkon/SinoWaves/releases")
    versions = re.findall(r"href=\"/DevFalkon/SinoWaves/releases/tag/v(\S{5})\"", html.read().decode())
    highest_version = versions[0]
    file.write(f"v{highest_version}")
os.remove(argv[0])
subprocess.Popen(['SinoWaves.exe'])
