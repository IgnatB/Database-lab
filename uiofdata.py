from tkinter import *
from tkinter import ttk
import re
from databasecore import *


class IU_Dbp(Dbp):

    def new_movie_in_the_end(self):
         mas = self.enter_check (name.get(), year1.get(),
                               typeof.get(), seriesname.get(),
                               season.get(), series.get(),
                               suspended.get(), year2.get())
         if mas[0] == 0:
             message.set(mas[1])
         else:
             self.add_last(mas)
             message.set('Done')


    def new_movie_insert(self):
         mas = self.enter_check (name.get(), year1.get(),
                               typeof.get(), seriesname.get(),
                               season.get(), series.get(),
                               suspended.get(), year2.get())
         if mas[0] == 0:
             message.set(mas[1])
             return
         else:
             try:
                 idn = int(idnumber.get())
             except:
                 message.set('wrong ID')
                 return
             if idn == len(self.index) - 1:
                 self.add_last(mas)
                 message.set('Done')
                 return
             elif idn < len(self.index) and idn >= 0:
                 self.insert(mas,idn)
                 message.set('Done')
             else:
                 message.set('wrong ID')
                 return

    def delete_movie(self):
        try:
            idn = int(idnumber.get())
        except:
            message.set('wrong ID')
            return
        if idn < len(self.index) and idn >= 0:
            self.delete(idn)
            message.set('Done')
            return
        else:
            message.set('wrong ID')
            return
       

    def IU_window(self):    
        root = Tk()
        root.title("add movie")
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        global idnumber
        idnumber = StringVar()
        global name
        name = StringVar()
        global year1
        year1 = StringVar()
        global typeof
        typeof = StringVar()
        global seriesname
        seriesname = StringVar()
        global season
        season = StringVar()
        global series
        series = StringVar()
        global suspended
        suspended = StringVar()
        global year2
        year2 = StringVar()
        global message
        message = StringVar()

        ttk.Entry(mainframe, width=30, textvariable=idnumber).grid()
        ttk.Button(mainframe, text="Show", command=self.print_10).grid()

        ttk.Entry(mainframe, width=70, textvariable=name).grid()
        ttk.Entry(mainframe, width=70, textvariable=year1).grid()
        ttk.Entry(mainframe, width=70, textvariable=typeof).grid()
        ttk.Entry(mainframe, width=70, textvariable=seriesname).grid()
        ttk.Entry(mainframe, width=70, textvariable=season).grid()
        ttk.Entry(mainframe, width=70, textvariable=series).grid()
        ttk.Entry(mainframe, width=70, textvariable=suspended).grid()
        ttk.Entry(mainframe, width=70, textvariable=year2).grid()
        ttk.Button(mainframe, text="Append Movie", command=self.new_movie_in_the_end).grid()
        ttk.Button(mainframe, text="Insert Movie", command=self.new_movie_insert).grid()
        ttk.Button(mainframe, text="Delete Movie", command=self.delete_movie).grid()
        ttk.Button(mainframe, text="Sort", command=self.sort_by_year).grid()
        ttk.Label(mainframe, textvariable=message, anchor='center').grid()

        #ttk.Combobox(mainframe,values = list(self.setyear1).sort(), height=3).grid()

        root.bind('<Return>', self.new_movie_in_the_end)

        root.mainloop()


