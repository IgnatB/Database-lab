#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
import re

class View(Toplevel):
    def __init__(self, master, user, time):
        """Инициализация и создание интерфейса программы
        
        idnumber - поле ввода которое показывает после какого элемента вставлять,
        какой изменить, какой удалить
        name,year1,typeof,seriesname,season,series,suspended,year2 - поля ввода для
        изменения, добавления, удаления элементов
        message - сообщение о выполненой операции
        movieslist,year1list,typeoflist,seriesnamelist,seasonlist,serieslist,suspendedlist,year2list,
        indexlist - видимые элементы в столбцах таблицы
        searchname,searchseriesname,searchseason,searchseries,vartypeof,varsuspended - поля и значения
        для задания поиска
        listposition - с какого номера элемента начинается вывод 15 кинолент в таблицу
        LISTBOX_HEIGHT - количество выводимых элементов
        Все координаты компонент меню заданы попиксельно
        """
        Toplevel.__init__(self, master)
        self.title("Movie database. User: " + user)
        self.geometry('1150x370-5+40')
        self.idnumber = StringVar()
        self.name = StringVar()
        self.year1 = StringVar()
        self.typeof = StringVar()
        self.seriesname = StringVar()
        self.season = StringVar()
        self.series = StringVar()
        self.suspended = StringVar()
        self.year2 = StringVar()
        self.message = StringVar()
        self.movieslist = StringVar()
        self.year1list = StringVar()
        self.typeoflist = StringVar()
        self.seriesnamelist = StringVar()
        self.seasonlist = StringVar()
        self.serieslist = StringVar()
        self.suspendedlist = StringVar()
        self.year2list = StringVar()
        self.indexlist = StringVar()
        self.searchname = StringVar()
        self.searchseriesname = StringVar()
        self.searchseason = StringVar()
        self.searchseries = StringVar()
        self.vartypeof = StringVar()
        self.vartypeof.set('0')
        self.varsuspended = IntVar()
        self.vartypeof.set(0)
        self.listposition = 0

        self.LISTBOX_HEIGHT = 15
  
   
        ttk.Label(self, text='Movie:').place(x=10, y=295)
        ttk.Entry(self, width=33, textvariable=self.name).place(x=10, y=315)
        ttk.Label(self, text='Year:').place(x=215, y=295)
        ttk.Entry(self, width=4, textvariable=self.year1).place(x=217, y=315)
        ttk.Label(self, text='Type:').place(x=250, y=295)
        ttk.Entry(self, width=3, textvariable=self.typeof).place(x=254, y=315)
        ttk.Label(self, text='Series name:').place(x=285, y=295)
        ttk.Entry(self, width=33, textvariable=self.seriesname).place(x=285, y=315)
        ttk.Label(self, text='Season:').place(x=490, y=295)
        ttk.Entry(self, width=5, textvariable=self.season).place(x=493, y=315)
        ttk.Label(self, text='Series:').place(x=535, y=295)
        ttk.Entry(self, width=5, textvariable=self.series).place(x=537, y=315)
        ttk.Label(self, text='Suspended:').place(x=575, y=295)
        ttk.Entry(self, width=11, textvariable=self.suspended).place(x=578, y=315)
        ttk.Label(self, text='Year:').place(x=652, y=295)
        ttk.Entry(self, width=4, textvariable=self.year2).place(x=654, y=315)

        ttk.Label(self, text='Insert after\Delete\Change:').place(x=10, y=342)
        ttk.Entry(self, width=8, textvariable=self.idnumber).place(x=160, y=342)
        self.insertButton = ttk.Button(self, text="Insert")
        self.insertButton.place(x=217, y=340)
        self.deleteButton = ttk.Button(self, text="Delete")
        self.deleteButton.place(x=296, y=340)
        self.changeButton = ttk.Button(self, text="Change")
        self.changeButton.place(x=375, y=340)
        self.appendButton = ttk.Button(self, text="Append")
        self.appendButton.place(x=454, y=340)
        self.saveButton = ttk.Button(self, text="Save")
        self.saveButton.place(x=531, y=340)
        self.newButton = ttk.Button(self, text="New", command=self.clear_entry)
        self.newButton.place(x=609, y=340)
        
        self.searchButton = ttk.Button(self, text="Search")
        self.searchButton.place(x=10, y=3)
        ttk.Label(self, text='Movie:').place(x=88, y=6)
        ttk.Entry(self, width=20, textvariable=self.searchname).place(x=130, y=6)
        ttk.Label(self, text='Year:').place(x=259, y=6)
        self.boxyear1 = ttk.Combobox(self, height=20)
        self.boxyear1.place(x=291, y=6, width=60)
        ttk.Radiobutton(self, text="Any", variable=self.vartypeof, value='0').place(x=355, y=6)
        ttk.Radiobutton(self, text="V", variable=self.vartypeof, value='V').place(x=401, y=6)
        ttk.Radiobutton(self, text="TV", variable=self.vartypeof, value='TV').place(x=432, y=6)
        ttk.Radiobutton(self, text="VG", variable=self.vartypeof, value='VG').place(x=470, y=6)
        ttk.Label(self, text='Series:').place(x=508, y=6)
        ttk.Entry(self, width=20, textvariable=self.searchseriesname).place(x=547, y=6)
        ttk.Label(self, text='Season:').place(x=676, y=6)
        ttk.Entry(self, width=5, textvariable=self.searchseason).place(x=722, y=6)
        ttk.Label(self, text='Series:').place(x=760, y=6)
        ttk.Entry(self, width=5, textvariable=self.searchseries).place(x=798, y=6)
        ttk.Radiobutton(self, text="Any", variable=self.varsuspended, value=0).place(x=838, y=6)
        ttk.Radiobutton(self, text="Suspended", variable=self.varsuspended, value=1).place(x=883, y=6)
        ttk.Label(self, text='Year:').place(x=967, y=6)
        self.boxyear2 = ttk.Combobox(self, height=20)
        self.boxyear2.place(x=999, y=6, width=60)
        self.showallButton = ttk.Button(self, text="Show All")
        self.showallButton.place(x=1065, y=3)

        self.sortnameButton = ttk.Button(self, text="⇊")
        self.sortnameButton.place(x=10, y=30, width=205)
        self.sortyear1Button = ttk.Button(self, text="⇊")
        self.sortyear1Button.place(x=215, y=30, width=35)
        self.sorttypeofButton = ttk.Button(self, text="⇊")
        self.sorttypeofButton.place(x=250, y=30, width=35)
        self.sortseriesnameButton = ttk.Button(self, text="⇊")
        self.sortseriesnameButton.place(x=285, y=30, width=205)
        self.sortseasonButton = ttk.Button(self, text="⇊")
        self.sortseasonButton.place(x=490, y=30, width=45)
        self.sortseriesButton = ttk.Button(self, text="⇊")
        self.sortseriesButton.place(x=535, y=30, width=40)
        self.sortsuspendedButton = ttk.Button(self, text="⇊")
        self.sortsuspendedButton.place(x=575, y=30, width=70)
        self.sortyear2Button = ttk.Button(self, text="⇊")
        self.sortyear2Button.place(x=645, y=30, width=45)
              
        self.upButton = ttk.Button(self, text="Up")
        self.upButton.place(x=690, y=30, width=80)
        self.downButton = ttk.Button(self, text="Down")
        self.downButton.place(x=690, y=290, width=80)
        
        self.pageupButton = ttk.Button(self, text="Page Up")
        self.pageupButton.place(x=775, y=30, width=80)
        self.pagedownButton = ttk.Button(self, text="Page Down")
        self.pagedownButton.place(x=775, y=290, width=80)
          
        self.moviesbox = Listbox(self, listvariable=self.movieslist, height=self.LISTBOX_HEIGHT, bd=1)
        self.moviesbox.place(x=10, y=50, width=205)
        self.year1box = Listbox(self, listvariable=self.year1list, height=self.LISTBOX_HEIGHT, bd=1)
        self.year1box.place(x=215, y=50, width=45)
        self.typeofbox = Listbox(self, listvariable=self.typeoflist, height=self.LISTBOX_HEIGHT, bd=1)
        self.typeofbox.place(x=250, y=50, width=35)
        self.seriesnamebox = Listbox(self, listvariable=self.seriesnamelist, height=self.LISTBOX_HEIGHT, bd=1)
        self.seriesnamebox.place(x=285, y=50, width=205)
        self.seasonbox = Listbox(self, listvariable=self.seasonlist, height=self.LISTBOX_HEIGHT, bd=1)
        self.seasonbox.place(x=490, y=50, width=45)
        self.seriesbox = Listbox(self, listvariable=self.serieslist, height=self.LISTBOX_HEIGHT, bd=1)
        self.seriesbox.place(x=535, y=50, width=40)
        self.suspendedbox = Listbox(self, listvariable=self.suspendedlist, height=self.LISTBOX_HEIGHT, bd=1)
        self.suspendedbox.place(x=575, y=50, width=70)
        self.year2box = Listbox(self, listvariable=self.year2list, height=self.LISTBOX_HEIGHT, bd=1)
        self.year2box.place(x=645, y=50, width=45)
        self.indexbox = Listbox(self, listvariable=self.indexlist, height=self.LISTBOX_HEIGHT, bd=1)
        self.indexbox.place(x=690, y=50, width=80)
        
        self.scale1 = Scale(self, showvalue=0, from_=0, length=240, orient='vertical')
        self.scale1.place(x=750, y=50)
      
        self.informframe = Canvas(self, width=10, height=10, bg='green')
        self.informframe.place(x=691, y=317)
        ttk.Label(self, textvariable=self.message).place(x=691, y=330)
        
        self.alarm_message(time, 'green')
 

    def enter_check(self):
        """Проверяет поля ввода, формирует массив значений
        
        при неправильно
        введеном поле указывает на ошибку
        """
        name = self.name.get()
        year1 = self.year1.get() 
        typeof = self.typeof.get()
        seriesname = self.seriesname.get()
        season = self.season.get()
        series = self.series.get() 
        suspended = self.suspended.get()
        year2 = self.year2.get()
        
        tmp = []           
        m = re.match('\s*([^"(){}]+)', name)
        if m:
            tmp.append(m.group(1))
        else:
            return (0, 'Wrong name')               
        m = re.match('^[?\d]{4,4}$', year1)
        if m:
            if year1 == '????':
                localyear1 = 0
            else:
                try: localyear1 = int(year1)
                except: return (0, 'Wrong year of creation') 
            tmp.append(localyear1)
        else:
            return (0, 'Wrong year of creation')              
        m = re.match('^[VGTvgt]{1,2}$', typeof)
        if m:
            tmp.append(typeof.upper())
        elif typeof == '':
            tmp.append(None)
        else:
            return (0, 'Wrong type')               
        m = re.match('\s*([^"(){}]+)', seriesname)
        if m:
            tmp.append(m.group(1))
        elif seriesname == '':
            tmp.append(None)
        else: 
            return (0, 'Wrong series name')               
        m = re.match('^\d+$', season)
        m1 = re.match('^\d+$', series)
        if m and m1:
            tmp.append(int(season))
            tmp.append(int(series))
        elif season == '' and series == '':
            tmp.append(None)
            tmp.append(None)
        else:
            return (0, 'Wrong season or series')               
        m = re.match('SUSPENDED', suspended)
        if m:
            tmp.append(1)
        elif suspended == '':
            tmp.append(None)
        else:
            return (0, 'So suspended or not?')
        m = re.match('^[?\d]{4,4}$', year2)
        if m:
            if year2 == '????':
                localyear2 = 0
            else:
                try: localyear2 = int(year2)
                except: return (0, 'Wrong year of release') 
            tmp.append(localyear2)
        else:
            return (0, 'Wrong year of release')       
        return tmp


    def insert_interface(self, length):
        """Возвращает разбитую запись и айди после которого стоит вставить запись
        
        В случае ошибки возвращает False
        """
        mas = self.enter_check()
        if mas[0] == 0:
            self.alarm_message(mas[1], 'red')
            return None, 0
        else:
            try:
                idn = int(self.idnumber.get())
            except:
                self.alarm_message('wrong ID', 'red')
                return None, 0
            if idn < length and idn >= 0:
                self.alarm_message('Inserted', 'green')
                return (mas, idn)
            else:
                self.alarm_message('wrong ID', 'red')
                return None, 0

            
    def delete_interface (self, length):
        """Возвращает айди записи, которую стоит удалить
        
        В случае ошибки возвращает False
        """
        try:
            idn = int(self.idnumber.get())
        except:
            self.alarm_message('wrong ID', 'red')
            return None
        if idn < length and idn >= 0:         
            if self.listposition > length:
                self.listposition = 0
            self.alarm_message('Deleted', 'green')
            return idn
        else:
            self.alarm_message('wrong ID', 'red')
            return None
        
    
    def change_interface (self, length):
        """Возвращает разбитую запись и айди записи, которую стоит изменить\
        
        В случае ошибки возвращает False
        """
        mas = self.enter_check()
        if mas[0] == 0:
            self.alarm_message(mas[1], 'red')
            return None , 0
        else:
            try:
                idn = int(self.idnumber.get())
            except:
                self.alarm_message('wrong ID', 'red')
                return None , 0
            if idn < length and idn >= 0:
                self.alarm_message('Changed', 'green')
                return mas , idn            
            else:
                self.alarm_message('wrong ID', 'red')
                return None , 0
            
    
    def append_interface (self):
        """Возвращает разбитую запись
        
        В случае ошибки возвращает False
        """
        mas = self.enter_check()
        if mas[0] == 0:
            self.alarm_message(mas[1], 'red')
            return None
        else:
            self.alarm_message('Appended', 'green')
            return mas


    def alarm_message (self, message, color):
        """Выводит message события и цвет color
        """
        self.message.set(message)
        self.informframe.configure(bg=color)
            
           
    def show_listbox_list(self, pieceOfData, length):
        """Обновляет выводимый список
        
        pieceOfData - массив из 15 элементов с базы данных
        length - длинна базы данных
        """
        tmpnm = []
        tmpy1 = []
        tmpto = []
        tmpsr = []
        tmpse = []
        tmpsn = []
        tmpsu = []
        tmpy2 = []
        indexrange = 0
        
        for movieinfo in pieceOfData:
            tmpnm.append(movieinfo[0])
            if movieinfo[1] == 0: tmpy1.append('????')
            else: tmpy1.append(movieinfo[1])
            if movieinfo[2] == None: tmpto.append('')
            else: tmpto.append(movieinfo[2])
            if movieinfo[3] == None: tmpsr.append('')
            else: tmpsr.append(movieinfo[3])
            if movieinfo[4] == None: tmpse.append('')
            else: tmpse.append(movieinfo[4])
            if movieinfo[5] == None: tmpsn.append('')
            else: tmpsn.append(movieinfo[5])
            if movieinfo[6] == None: tmpsu.append('')
            else: tmpsu.append('SUSPENDED')
            if movieinfo[7] == 0: tmpy2.append('????')
            else: tmpy2.append(movieinfo[7])
            indexrange += 1

        self.movieslist.set(tuple(tmpnm))
        self.year1list.set(tuple(tmpy1))    
        self.typeoflist.set(tuple(tmpto))
        self.seriesnamelist.set(tuple(tmpsr))
        self.seasonlist.set(tuple(tmpse))
        self.serieslist.set(tuple(tmpsn))
        self.suspendedlist.set(tuple(tmpsu))
        self.year2list.set(tuple(tmpy2))
        self.indexlist.set(tuple(range(self.listposition,
                                       self.listposition + indexrange)))
        self.scale1.config(to=length - 1)
        self.scale1.set(self.listposition)
        
        self.clear_selection()
        

    def selection_return (self):
        """В зависимости от выделеного элемента возвращает номер выделеной позиции
        """
        selection = 0
        if len(self.moviesbox.curselection()) > 0:
            selection = int(self.moviesbox.curselection()[0])
        if len(self.year1box.curselection()) > 0:
            selection = int(self.year1box.curselection()[0])
        if len(self.typeofbox.curselection()) > 0:
            selection = int(self.typeofbox.curselection()[0])
        if len(self.seriesnamebox.curselection()) > 0:
            selection = int(self.seriesnamebox.curselection()[0])
        if len(self.seasonbox.curselection()) > 0:
            selection = int(self.seasonbox.curselection()[0])
        if len(self.seriesbox.curselection()) > 0:
            selection = int(self.seriesbox.curselection()[0])
        if len(self.suspendedbox.curselection()) > 0:
            selection = int(self.suspendedbox.curselection()[0])
        if len(self.year2box.curselection()) > 0:
            selection = int(self.year2box.curselection()[0])

        self.clear_selection()   
        self.moviesbox.itemconfig(selection, {'bg':'green'})   
        self.year1box.itemconfig(selection, {'bg':'green'}) 
        self.typeofbox.itemconfig(selection, {'bg':'green'})
        self.seriesnamebox.itemconfig(selection, {'bg':'green'}) 
        self.seasonbox.itemconfig(selection, {'bg':'green'})
        self.seriesbox.itemconfig(selection, {'bg':'green'}) 
        self.suspendedbox.itemconfig(selection, {'bg':'green'})
        self.year2box.itemconfig(selection, {'bg':'green'})
        
        return selection


    def show_selected_movie(self, id_number, selection):  
        """Заполняет поля для ввода записью selection и id_number
        """
        self.idnumber.set(id_number)
        self.name.set(selection[0])       
        if selection[1] == 0:
            self.year1.set('????')
        else:
            self.year1.set(selection[1])            
        if selection[2] == None:
            self.typeof.set('')
        else:
            self.typeof.set(selection[2])  
        if selection[3] == None:
            self.seriesname.set('')
        else:
            self.seriesname.set(selection[3])
        if selection[4] == None:
            self.season.set('')
        else:
            self.season.set(selection[4])    
        if selection[5] == None:
            self.series.set('')
        else:
            self.series.set(selection[5])
        if selection[6] == None:
            self.suspended.set('')
        else:
            self.suspended.set('SUSPENDED')   
        if selection[7] == 0:
            self.year2.set('????')
        else:
            self.year2.set(selection[7])


    def clear_selection(self):
        """Делает все поля списка белыми
        """
        for selection in range(0, self.moviesbox.size()):
            self.moviesbox.itemconfig(selection, {'bg':'white'})   
            self.year1box.itemconfig(selection, {'bg':'white'}) 
            self.typeofbox.itemconfig(selection, {'bg':'white'})
            self.seriesnamebox.itemconfig(selection, {'bg':'white'}) 
            self.seasonbox.itemconfig(selection, {'bg':'white'})
            self.seriesbox.itemconfig(selection, {'bg':'white'}) 
            self.suspendedbox.itemconfig(selection, {'bg':'white'})
            self.year2box.itemconfig(selection, {'bg':'white'})


    def clear_entry(self):
        """Делает все поля ввода пустыми
        """
        self.name.set('')
        self.year1.set('')
        self.typeof.set('')
        self.seriesname.set('')
        self.season.set('')
        self.series.set('')
        self.suspended.set('')
        self.year2.set('')


    def save(self):
        """Вызывает диалог сохранения, возвращает путь к файлу, в который стоит сохранить базу данных
        """
        filename = filedialog.asksaveasfilename()
        return filename


