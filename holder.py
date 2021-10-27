import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()

file = filedialog.askopenfilename(initialdir="/", title="Selecione uma imagem",
                                  filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
print(file)
os.system("pause")
