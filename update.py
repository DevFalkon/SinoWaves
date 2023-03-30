import os
import subprocess
import urllib.request
import re

html = urllib.request.urlopen(f"https://github.com/DevFalkon/SinoWaves/releases")
versions = re.findall(r"href=\"/DevFalkon/SinoWaves/releases/tag/v(\S{5})\"", html.read().decode())
highest_version = versions[0]

os.mkdir("del")
for i in os.listdir():
    if i != "saved" and i != "del":
        os.rename(i, f"del\\{i}")

urllib.request.urlretrieve(f"https://github.com/DevFalkon/SinoWaves/archive/refs/tags/v{highest_version}.zip",
                           "new")
os.rename("new", "new.zip")
subprocess.run("tar -xf new.zip", shell=True)
os.remove("new.zip")
for i in os.listdir(f"SinoWaves-{highest_version}"):
    if i != "update.py":
        os.rename(f"SinoWaves-{highest_version}\\{i}", i)

subprocess.run(f"rmdir /s /Q SinoWaves-{highest_version}", shell=True)
subprocess.run(f"python setup.py", shell=True)
