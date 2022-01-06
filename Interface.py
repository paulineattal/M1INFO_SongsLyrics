# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 02:00:09 2022

@author: f_ati
"""

import tkinter as tk
from io import BytesIO
import matplotlib.pyplot as plt
import os
import glob
import natsort
from PIL import Image
from PIL import ImageTk
import mots

window = tk.Tk()

window.title('Search song')
window.iconbitmap('C:/Users/f_ati/OneDrive/Documents/Master1_Informatique/Algo/python_chanson/icon.ico')

window.config(padx=10, pady=10)

title_label = tk.Label(window, text = 'Search song')
title_label.config(font=('Arial', 32))
title_label.pack(padx=10, pady=10)

target_image = tk.Label(window)
target_image.pack(padx=10, pady=10)

target_information = tk.Label(window)
target_information.config(font=("Arial", 20))
target_information.pack(padx=10, pady=10)


photos_names_list = ["mask"]
#FUNCTION
def showimage():

    dir1 = r"C:\Users\f_ati\OneDrive\Documents\Master1_Informatique\Algo\python_chanson"
    path1 = os.path.join(dir1, '*g')
    files = glob.glob(path1)
    files1 = natsort.natsorted(files, reverse=False)
    for x in files1:
        img = plt.imread(x)
        image = Image.open(img)
        imag = ImageTk.PhotoImage(image)


    target_image.config(image=imag)
    target_image.image = imag




label_id_name = tk.Label(window, text=" The KEY WORD")
label_id_name.config(font=("Arial", 20))
label_id_name.pack(padx=10, pady=10)

text_id_name = tk.Text(window, height = 1)
text_id_name.config(font=("Arial", 20))
text_id_name.pack(padx=10, pady=10)

btn_load = tk.Button(window, text="Search ", command = showimage)
btn_load.config(font=("Arial", 20))
btn_load.pack(padx=10, pady=10)

window.mainloop()