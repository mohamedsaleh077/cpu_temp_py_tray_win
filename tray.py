import pystray
from PIL import Image, ImageDraw, ImageFont
from time import sleep
import threading
import clr # the pythonnet module.
import sys, os, pathlib, clr

base_dir = getattr(sys, "_MEIPASS", os.path.abspath("."))
dll_path = pathlib.Path(base_dir, "OpenHardwareMonitorLib.dll")
clr.AddReference(str(dll_path))          # robust path for dev & frozen
# e.g. clr.AddReference(r'OpenHardwareMonitor/OpenHardwareMonitorLib'), without .dll

from OpenHardwareMonitor.Hardware import Computer

import os
import sys
import win32com.shell.shell as shell
ASADMIN = 'asadmin'

if sys.argv[-1] != ASADMIN:
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
    shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
    sys.exit(0)

print("I am root now.")

def create_image(width, height, color1, color2, number):
    canvas = Image.new('RGB', (64, 64), "red")
    draw = ImageDraw.Draw(canvas)
    text = str(number)
    font = ImageFont.truetype("arial.ttf", 60)
    draw.text((0, 0), text, fill="white", font=font)
    return canvas

# In order for the icon to be displayed, you must provide an icon
icon = pystray.Icon(
    'test name',
    icon=create_image(64, 64, 'black', 'white', 56))

def update_icon():
    c = Computer()
    c.CPUEnabled = True # get the Info about CPU
    c.GPUEnabled = True # get the Info about GPU
    c.Open()
    while True:
        for a in range(0, len(c.Hardware[0].Sensors)):
            # print(c.Hardware[0].Sensors[a].Identifier)
            if "/temperature" in str(c.Hardware[0].Sensors[a].Identifier):
                temp = c.Hardware[0].Sensors[a].get_Value()
                img = create_image(64, 64, 'black', 'white', temp)
                icon.icon = img
                sleep(1)
                c.Hardware[0].Update()

def exit(icon: pystray.Icon) -> None:
    icon.visible = False
    exit_event.set()
    icon.stop()

if __name__ == "__main__":
    icon = pystray.Icon("CPU Tempreture tray")
    icon.menu = pystray.Menu(
        pystray.MenuItem('Quit', exit)
    )
    icon.icon = Image.new("RGB", (32, 32), (255, 255, 255))  # 32px32px, white
    # Create a new thread to run the update_icon() function
    thread = threading.Thread(target=update_icon)
    # Start the thread
    thread.start()
    icon.run()
