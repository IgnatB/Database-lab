#!/usr/bin/python3
# -*- coding: utf-8 -*-

import hashlib
import sys
from tkinter import *
from tkinter import ttk


def autorisation_window():
    global user
    user = 0
    
    root = Tk()
    root.title("Log in")
    mainframe = ttk.Frame(root)
    mainframe.pack()

    logEntry = StringVar()
    pasEntry = StringVar()
    desk = StringVar()
    desk.set('')

    def checkPerson():
        global user
        login = logEntry.get()
        password = pasEntry.get()
        password = password.encode('utf-8')
        s = hashlib.md5()
        s.update(password)
        f = open('secure.txt', 'r')
        for line in f:
            try: savedLogin, savedPassword = line.split('>')
            except: break
            savedPassword = savedPassword.replace("\n", "")
            if (savedLogin == login and s.hexdigest() == savedPassword):
                f.close()
                user = login
                desk.set('Welcome ' + login)
                return
        f.close()
        user = 0
        desk.set('Wrong login or password')      
        return

    def New_User_Register():
        global user
        login = logEntry.get()
        password = pasEntry.get()
        password = password.encode('utf-8')
        s = hashlib.md5()
        s.update(password)
        f = open('secure.txt', 'r+')
        for line in f:
            try: savedLogin, savedPassword = line.split('>')
            except: break
            if login == savedLogin:
                f.close()                
                user = 0
                desk.set('Login already exists')
                return
        f.seek(0, 2)
        towrite = login + '>' + s.hexdigest() + '\n'
        f.write(towrite)
        f.close()
        user = login
        desk.set('You autorised as: ' + login + ' Welcome!')
        return

    def close():
        root.destroy()
       
    ttk.Label(mainframe, text='Please log in or register:').pack()
    ttk.Label(mainframe, text='Login:').pack()
    ttk.Entry(mainframe, width=30, textvariable=logEntry).pack()
    ttk.Label(mainframe, text='Password:').pack()
    ttk.Entry(mainframe, width=30, textvariable=pasEntry).pack()
    ttk.Button(mainframe, text="Log in", command=checkPerson).pack()
    ttk.Button(mainframe, text="Register", command=New_User_Register).pack()
    ttk.Label(mainframe, textvariable=desk).pack()
    ttk.Button(mainframe, text="Done", command=close).pack()

    root.mainloop()

    return user
