import requests
import webbrowser
import keyboard
from tkinter import Tk
from time import sleep
import urllib.parse
import os


URL = ''
sleep(2)
keyboard.press_and_release('ctrl+l')
sleep(0.1)
keyboard.press_and_release('ctrl+c')
sleep(0.1)
path = urllib.parse.unquote(Tk().selection_get(selection='CLIPBOARD').replace('file:///', ''))
if path.startswith('http'):
    open('', 'wb').write(requests.get(path).content)
    path = ''
loc = requests.post(f'{URL}/', files={'file': open(path, 'rb')}).json()['loc']
webbrowser.open(f'{URL}{loc}', )
os.remove('pdf.pdf')