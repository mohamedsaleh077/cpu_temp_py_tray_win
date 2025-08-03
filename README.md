# CPU temperature Windows system tray

## How to use
just clone the repo, install python and some python stuff like
```
pip install pystray pythonnet 
```
then double click on tray.py 🤷‍♀️

## How to build?
```
pip install pyinstaller

python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install pyinstaller==6.* pystray pillow pythonnet pywin32

pyinstaller --onefile --name CpuTempTray --windowed --icon=tray.ico --hidden-import=clr --add-binary ".\OpenHardwareMonitorLib.dll;." --clean tray.py

```

## How to make it start everytime you turn on your device?
- Win + R
- type `shell:startup` then startup folder will appear
- make a shortcut of the app in this folder by:
  - right click on the exe file
  - press create shortcut
  - move the shortcut to the startup folder

## How to terminate the script?
just right click and Quit Idk why I left that here.