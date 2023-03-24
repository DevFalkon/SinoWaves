# SinoWaves

## Running the project as a python project

**Using python virtaul environ ment**
1. Open terminal in the project directory
2. Run the following command: 
```
python -m venv venv
venv\Scripts\activate
pip install pygame
python main.py
```

## Compiling the project to windows exe

**After creating the venv folder**
```
venv\Scripts\activate
pip install pyinstaller
pyinstaller main.py --onefile --noconsole --clean
```

the executable will be in the dist folder
move dist\main.exe to the root directory
delete the build and venv folders, and main.py file
