import shutil
import os
from PIL import Image
from os import path
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
print(file_path)

original = file_path
target = './imgs/02teste.jpg'

with Image.open(file_path) as img:
    # Mostra o tamanho da imagen aberta
    if img.width > 200:
        print('top')
        

##shutil.copyfile(original, target)
