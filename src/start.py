#!/usr/bin/python3
# -*- coding: utf-8 -*-

from autorisation import *
from controller import *
from tkinter import *
from tkinter import filedialog
import sys, traceback

user = autorisation_window()
if user == 0:
    sys.exit(0)
user = '7'
root = Tk()
root.withdraw()
filename = filedialog.askopenfilename()
app = Controller(root, user, filename)
root.mainloop()
