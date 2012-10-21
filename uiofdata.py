from tkinter import *
from tkinter import ttk
from tkinter import font
import re
from databasecore import *



import webbrowser
from PIL import Image, ImageTk
import urllib.request
import imdbparser

LISTBOX_HEIGHT = 15

class IU_Dbp(Dbp):
      
    def IU_window(self,user):
               
        self.position = 0
        
        root = Tk()
        root.title("Movie database. User: " + user)
        mainframe = ttk.Frame(root, width=1150, height=370)
        mainframe.pack()

        idnumber = StringVar()
        name = StringVar()
        year1 = StringVar()
        typeof = StringVar()
        seriesname = StringVar()
        season = StringVar()
        series = StringVar()
        suspended = StringVar()
        year2 = StringVar()
        message = StringVar()
        movieslist = StringVar()
        year1list = StringVar()
        typeoflist = StringVar()
        seriesnamelist = StringVar()
        seasonlist = StringVar()
        serieslist = StringVar()
        suspendedlist = StringVar()
        year2list = StringVar()
        indexlist = StringVar()

        searchname = StringVar()
        searchseriesname = StringVar()
        searchseason = StringVar()
        searchseries = StringVar()
        vartypeof = StringVar()
        vartypeof.set('0')
        varsuspended = IntVar()


        def make_listbox_list(pos):
            movieslist.set(tuple([self.datalist[i][0] for i in self.indx[pos:pos+LISTBOX_HEIGHT]]))
            tmpy1 = []
            tmpto = []
            tmpsr = []
            tmpse = []
            tmpsn = []
            tmpsu = []
            tmpy2 = []
            indexrange = 0
            for i in self.indx[pos:pos+LISTBOX_HEIGHT]:
                if self.datalist[i][1] == 0:
                     tmpy1.append('????')
                else:
                     tmpy1.append(self.datalist[i][1])
                if self.datalist[i][2] == None:
                     tmpto.append('')
                else:
                     tmpto.append(self.datalist[i][2])
                if self.datalist[i][3] == None:
                     tmpsr.append('')
                else:
                     tmpsr.append(self.datalist[i][3])
                if self.datalist[i][4] == None:
                     tmpse.append('')
                else:
                     tmpse.append(self.datalist[i][4])
                if self.datalist[i][5] == None:
                     tmpsn.append('')
                else:
                     tmpsn.append(self.datalist[i][5])
                if self.datalist[i][6] == None:
                     tmpsu.append('')
                else:
                     tmpsu.append('SUSPENDED')
                if self.datalist[i][7] == 0:
                     tmpy2.append('????')
                else:
                     tmpy2.append(self.datalist[i][7])
                indexrange += 1
            year1list.set(tuple(tmpy1))    
            typeoflist.set(tuple(tmpto))
            seriesnamelist.set(tuple(tmpsr))
            seasonlist.set(tuple(tmpse))
            serieslist.set(tuple(tmpsn))
            suspendedlist.set(tuple(tmpsu))
            year2list.set(tuple(tmpy2))
            indexlist.set(tuple(range(pos,pos + indexrange)))
            scale1.config(to=len(self.indx))
            scale1.set(self.position)
            

        def clear_selection():
            for selection in range(0,moviesbox.size()):
                moviesbox.itemconfig(selection, {'bg':'white'})   
                year1box.itemconfig(selection, {'bg':'white'}) 
                typeofbox.itemconfig(selection, {'bg':'white'})
                seriesnamebox.itemconfig(selection, {'bg':'white'}) 
                seasonbox.itemconfig(selection, {'bg':'white'})
                seriesbox.itemconfig(selection, {'bg':'white'}) 
                suspendedbox.itemconfig(selection, {'bg':'white'})
                year2box.itemconfig(selection, {'bg':'white'})

        def move_list_down():
            if self.position < len(self.indx) - LISTBOX_HEIGHT:
                self.position +=1
                make_listbox_list(self.position)
                clear_selection()          

        def move_list_up():
            if self.position > 0:
                self.position -=1
                make_listbox_list(self.position)
                clear_selection()

        def scale_onMove_show(pos):
            self.position = int(pos)
            make_listbox_list(self.position)
            clear_selection()


        def show_all():
            self.position = 0
            self.return_all_list()
            make_listbox_list(self.position)
            clear_selection()

            
        def sort_name_show():
            self.position = 0
            self.sort_by_name()
            make_listbox_list(self.position)
            clear_selection()
        def sort_year1_show():
            self.position = 0
            self.sort_by_year1()
            make_listbox_list(self.position)
            clear_selection()
        def sort_typeof_show():
            self.position = 0
            self.sort_by_typeof()
            make_listbox_list(self.position)
            clear_selection()
        def sort_seriesname_show():
            self.position = 0
            self.sort_by_seriesname()
            make_listbox_list(self.position)
            clear_selection()
        def sort_season_show():
            self.position = 0
            self.sort_by_season()
            make_listbox_list(self.position)
            clear_selection()
        def sort_series_show():
            self.position = 0
            self.sort_by_series()
            make_listbox_list(self.position)
            clear_selection()
        def sort_suspended_show():
            self.position = 0
            self.sort_by_suspended()
            make_listbox_list(self.position)
            clear_selection()
        def sort_year2_show():
            self.position = 0
            self.sort_by_year2()
            make_listbox_list(self.position)
            clear_selection()

        def search_and_show():
            find = self.search(searchname.get(), boxyear1.get(),
                        vartypeof.get(), searchseriesname.get(),
                        searchseason.get(), searchseries.get(),
                        varsuspended.get(), boxyear2.get())
            if find == 0:
                message.set('Search Failed')
                informframe.configure(bg = 'red')
                self.position = 0
                make_listbox_list(self.position)
                clear_selection()
                return
            else:
                message.set(find)
                informframe.configure(bg = 'green')
                self.position = 0
                make_listbox_list(self.position)
                clear_selection()

        def delete_movie():
            try:
                idn = int(idnumber.get())
            except:
                message.set('wrong ID')
                informframe.configure(bg = 'red')
                return
            if idn < len(self.indx) and idn >= 0:
                self.delete(idn)
                make_listbox_list(self.position)
                message.set('Done')
                informframe.configure(bg = 'green')
                clear_selection()
                return
            else:
                message.set('wrong ID')
                informframe.configure(bg = 'red')
                return

        def change_movie():
             mas = self.enter_check (name.get(), year1.get(),
                                   typeof.get(), seriesname.get(),
                                   season.get(), series.get(),
                                   suspended.get(), year2.get())
             if mas[0] == 0:
                 message.set(mas[1])
                 informframe.configure(bg = 'red')
                 return
             else:
                 try:
                     idn = int(idnumber.get())
                 except:
                     message.set('wrong ID')
                     informframe.configure(bg = 'red')
                     return
                 if idn < len(self.indx) and idn >= 0:
                     self.change(mas,idn)
                     make_listbox_list(self.position)
                     message.set('Done')
                     informframe.configure(bg = 'green')
                     clear_selection()
                 else:
                     message.set('wrong ID')
                     informframe.configure(bg = 'red')
                     return

        def new_movie_insert():
             mas = self.enter_check (name.get(), year1.get(),
                                   typeof.get(), seriesname.get(),
                                   season.get(), series.get(),
                                   suspended.get(), year2.get())
             if mas[0] == 0:
                 message.set(mas[1])
                 informframe.configure(bg = 'red')
                 return
             else:
                 try:
                     idn = int(idnumber.get())
                 except:
                     message.set('wrong ID')
                     informframe.configure(bg = 'red')
                     return
                 if idn == len(self.indx) - 1:
                     self.add_last(mas)
                     make_listbox_list(self.position)
                     message.set('Done')
                     informframe.configure(bg = 'green')
                     clear_selection()
                     return
                 elif idn < len(self.indx) and idn >= 0:
                     self.insert(mas,idn)
                     make_listbox_list(self.position)
                     message.set('Done')
                     informframe.configure(bg = 'green')
                     clear_selection()
                 else:
                     message.set('wrong ID')
                     informframe.configure(bg = 'red')
                     return

        def new_movie_in_the_end():
             mas = self.enter_check (name.get(), year1.get(),
                                   typeof.get(), seriesname.get(),
                                   season.get(), series.get(),
                                   suspended.get(), year2.get())
             if mas[0] == 0:
                 message.set(mas[1])
                 informframe.configure(bg = 'red')
             else:
                 self.add_last(mas)
                 make_listbox_list(self.position)
                 message.set('Done')
                 informframe.configure(bg = 'green')
                 clear_selection()

        def show_movie_from_list(*args):
            selection = 0
            clear_selection()
            if len(moviesbox.curselection()) > 0:
                selection = int(moviesbox.curselection()[0])
            if len(year1box.curselection()) > 0:
                selection = int(year1box.curselection()[0])
            if len(typeofbox.curselection()) > 0:
                selection = int(typeofbox.curselection()[0])
            if len(seriesnamebox.curselection()) > 0:
                selection = int(seriesnamebox.curselection()[0])
            if len(seasonbox.curselection()) > 0:
                selection = int(seasonbox.curselection()[0])
            if len(seriesbox.curselection()) > 0:
                selection = int(seriesbox.curselection()[0])
            if len(suspendedbox.curselection()) > 0:
                selection = int(suspendedbox.curselection()[0])
            if len(year2box.curselection()) > 0:
                selection = int(year2box.curselection()[0])
                
            moviesbox.itemconfig(selection, {'bg':'green'})   
            year1box.itemconfig(selection, {'bg':'green'}) 
            typeofbox.itemconfig(selection, {'bg':'green'})
            seriesnamebox.itemconfig(selection, {'bg':'green'}) 
            seasonbox.itemconfig(selection, {'bg':'green'})
            seriesbox.itemconfig(selection, {'bg':'green'}) 
            suspendedbox.itemconfig(selection, {'bg':'green'})
            year2box.itemconfig(selection, {'bg':'green'})
            
            i = self.indx[self.position + selection]
            idnumber.set(self.position + selection)
            name.set(self.datalist[i][0])       
            if self.datalist[i][1] == 0:
                year1.set('????')
            else:
                year1.set(self.datalist[i][1])            
            if self.datalist[i][2] == None:
                typeof.set('')
            else:
                typeof.set(self.datalist[i][2])  
            if self.datalist[i][3] == None:
                seriesname.set('')
            else:
                seriesname.set(self.datalist[i][3])
            if self.datalist[i][4] == None:
                season.set('')
            else:
                season.set(self.datalist[i][4])    
            if self.datalist[i][5] == None:
                series.set('')
            else:
                series.set(self.datalist[i][5])
            if self.datalist[i][6] == None:
                suspended.set('')
            else:
                suspended.set('SUSPENDED')   
            if self.datalist[i][7] == 0:
                year2.set('????')
            else:
                year2.set(self.datalist[i][7])

        def more_info():

            def clear_info():
                img1 = Image.open(r'blank.jpg')
                photo1 = ImageTk.PhotoImage(img1)
                poster.photo = photo1
                poster.configure(image = photo1)
                description.delete(1.0, END)
                rating.config(text = '')

            try: i = int(idnumber.get())
            except: return
            if not (i < len(self.indx) and i >= 0):
                return
            
            pictureUrl, descriptionText, ratingText = imdbparser.load_content_imdb(self.datalist[i][0],self.datalist[i][1])
            #print((pictureUrl,descriptionText,ratingText))
            if pictureUrl == -1:
                message.set('No internet')
                informframe.configure(bg = 'red')
                clear_info()
            elif pictureUrl == 0:
                message.set('Cannot find')
                informframe.configure(bg = 'red')
                clear_info()
            else:
                if pictureUrl == 1:
                    message.set('No poster')
                    informframe.configure(bg = 'red')
                    clear_info()
                else:
                    urllib.request.urlretrieve(pictureUrl,r'pic.jpg')
                    img1 = Image.open(r'pic.jpg')
                    photo1 = ImageTk.PhotoImage(img1)
                    poster.photo = photo1
                    poster.configure(image = photo1)
                    informframe.configure(bg = 'green')
                    
                if descriptionText == 0:
                    message.set('No text')
                    description.delete(1.0, END)
                else:
                    description.insert(INSERT, descriptionText)
                if ratingText == 0:
                    message.set('No rating')
                    rating.config(text = '')
                else:
                    rating.config(text = ratingText)

        def search_google():
            try: i = int(idnumber.get())
            except: return
            if not (i < len(self.indx) and i >= 0):
                return
            year = str(self.datalist[i][1])
            googlelink = r'http://www.google.com/search?q=' + self.datalist[i][0] +  ' ' + year
            webbrowser.open(googlelink, new = 2 )

        def search_imdb():
            try: i = int(idnumber.get())
            except: return
            if not (i < len(self.indx) and i >= 0):
                return
            url_imdb_search = r'http://www.imdb.com/find?q=' + self.datalist[i][0] + '&s=all'
            webbrowser.open(url_imdb_search, new = 2 )

        def search_exua():
            try: i = int(idnumber.get())
            except: return
            if not (i < len(self.indx) and i >= 0):
                return
            exlink = r'http://www.ex.ua/search?s=' + self.datalist[i][0] 
            webbrowser.open(exlink, new = 2 )

        def search_youtube():
            try: i = int(idnumber.get())
            except: return
            if not (i < len(self.indx) and i >= 0):
                return
            youtubelink = r'http://www.youtube.com/results?search_query=' + self.datalist[i][0] 
            webbrowser.open(youtubelink, new = 2 )

        def show_index_from_list(*args):
            idnumber.set(self.position + int(indexbox.curselection()[0]))

        def clear_entry(*args):
            name.set('')
            year1.set('')
            typeof.set('')
            seriesname.set('')
            season.set('')
            series.set('')
            suspended.set('')
            year2.set('')
            
        ttk.Button(mainframe, text="⇊", command=sort_name_show).place(x = 10, y = 30, width = 205)
        ttk.Button(mainframe, text="⇊", command=sort_year1_show).place(x = 215, y = 30, width = 35)
        ttk.Button(mainframe, text="⇊", command=sort_typeof_show).place(x = 250, y = 30, width = 35)
        ttk.Button(mainframe, text="⇊", command=sort_seriesname_show).place(x = 285, y = 30, width = 205)
        ttk.Button(mainframe, text="⇊", command=sort_season_show).place(x = 490, y = 30, width = 45)
        ttk.Button(mainframe, text="⇊", command=sort_series_show).place(x = 535, y = 30, width = 40)
        ttk.Button(mainframe, text="⇊", command=sort_suspended_show).place(x = 575, y = 30, width = 70)
        ttk.Button(mainframe, text="⇊", command=sort_year2_show).place(x = 645, y = 30, width = 45)

        
        ttk.Label(mainframe, text='Movie:').place(x = 10, y = 295)
        ttk.Entry(mainframe, width=33, textvariable=name).place(x = 10, y = 315)
        ttk.Label(mainframe, text='Year:').place(x = 215, y = 295)
        ttk.Entry(mainframe, width=4, textvariable=year1).place(x = 217, y = 315)
        ttk.Label(mainframe, text='Type:').place(x = 250, y = 295)
        ttk.Entry(mainframe, width=3, textvariable=typeof).place(x = 254, y = 315)
        ttk.Label(mainframe, text='Series name:').place(x = 285, y = 295)
        ttk.Entry(mainframe, width=33, textvariable=seriesname).place(x = 285, y = 315)
        ttk.Label(mainframe, text='Season:').place(x = 490, y = 295)
        ttk.Entry(mainframe, width=5, textvariable=season).place(x = 493, y = 315)
        ttk.Label(mainframe, text='Series:').place(x = 535, y = 295)
        ttk.Entry(mainframe, width=5, textvariable=series).place(x = 537, y = 315)
        ttk.Label(mainframe, text='Suspended:').place(x = 575, y = 295)
        ttk.Entry(mainframe, width=11, textvariable=suspended).place(x = 578, y = 315)
        ttk.Label(mainframe, text='Year:').place(x = 652, y = 295)
        ttk.Entry(mainframe, width=4, textvariable=year2).place(x = 654, y = 315)


        ttk.Label(mainframe, text='Insert after\Delete\Change:').place(x = 10, y = 342)
        ttk.Entry(mainframe, width=8, textvariable=idnumber).place(x = 160, y = 342)
        ttk.Button(mainframe, text="Insert", command=new_movie_insert).place(x = 217, y = 340)
        ttk.Button(mainframe, text="Delete", command=delete_movie).place(x = 296, y = 340)
        ttk.Button(mainframe, text="Change", command=change_movie).place(x = 375, y = 340)
        ttk.Button(mainframe, text="Append", command=new_movie_in_the_end).place(x = 454, y = 340)
        ttk.Button(mainframe, text="Save", command=self.save).place(x = 531, y = 340)
        ttk.Button(mainframe, text="New", command=clear_entry).place(x = 609, y = 340)
        

        ttk.Button(mainframe, text="Search", command=search_and_show).place(x = 10, y = 3)
        ttk.Label(mainframe, text='Movie:').place(x = 88, y = 6)
        ttk.Entry(mainframe, width=20, textvariable=searchname).place(x = 130, y = 6)
        ttk.Label(mainframe, text='Year:').place(x = 259, y = 6)
        boxyear1 = ttk.Combobox(mainframe,values = list(self.setyear1), height=20)
        boxyear1.place(x = 291, y = 6, width = 60)
        ttk.Radiobutton(root, text="Any", variable=vartypeof, value='0').place(x = 355, y = 6)
        ttk.Radiobutton(root, text="V", variable=vartypeof, value='V').place(x = 401, y = 6)
        ttk.Radiobutton(root, text="TV", variable=vartypeof, value='TV').place(x = 432, y = 6)
        ttk.Radiobutton(root, text="VG", variable=vartypeof, value='VG').place(x = 470, y = 6)
        ttk.Label(mainframe, text='Series:').place(x = 508, y = 6)
        ttk.Entry(mainframe, width=20, textvariable=searchseriesname).place(x = 547, y = 6)
        ttk.Label(mainframe, text='Season:').place(x = 676, y = 6)
        ttk.Entry(mainframe, width=5, textvariable=searchseason).place(x = 722, y = 6)
        ttk.Label(mainframe, text='Series:').place(x = 760, y = 6)
        ttk.Entry(mainframe, width=5, textvariable=searchseries).place(x = 798, y = 6)
        ttk.Radiobutton(root, text="Any", variable=varsuspended, value=0).place(x = 838, y = 6)
        ttk.Radiobutton(root, text="Suspended", variable=varsuspended, value=1).place(x = 883, y = 6)
        ttk.Label(mainframe, text='Year:').place(x = 967, y = 6)
        boxyear2 = ttk.Combobox(mainframe,values = list(self.setyear2), height=20)
        boxyear2.place(x = 999, y = 6, width = 60)
        ttk.Button(mainframe, text="Show All", command=show_all).place(x = 1065, y = 3)
        ttk.Button(mainframe, text="More Info", command=more_info).place(x = 1065, y = 40)

        img = Image.open(r'google.jpg')
        photogoogle = ImageTk.PhotoImage(img)
        ttk.Button(mainframe, image = photogoogle, command=search_google).place(x = 1014, y = 70)
        img = Image.open(r'youtube.png')
        photoyoutube = ImageTk.PhotoImage(img)
        ttk.Button(mainframe, image = photoyoutube, command=search_youtube).place(x = 1074, y = 70)
        img = Image.open(r'imdb.png')
        photoimdb = ImageTk.PhotoImage(img)
        ttk.Button(mainframe, image = photoimdb, command=search_imdb).place(x = 1015, y = 130)
        img = Image.open(r'exua.png')
        photoexua = ImageTk.PhotoImage(img)
        ttk.Button(mainframe, image = photoexua, command=search_exua).place(x = 1075, y = 130)
        
        
                       
        ttk.Button(mainframe, text="Up", command=move_list_up).place(x = 690, y = 30, width = 80)
        ttk.Button(mainframe, text="Down", command=move_list_down).place(x = 690, y = 290, width = 80)

        
        moviesbox = Listbox(mainframe, listvariable=movieslist, height=LISTBOX_HEIGHT, bd = 1)
        moviesbox.place(x = 10, y = 50, width = 205)
        year1box = Listbox(mainframe, listvariable=year1list, height=LISTBOX_HEIGHT, bd = 1)
        year1box.place(x = 215, y = 50, width = 45)
        typeofbox = Listbox(mainframe, listvariable=typeoflist, height=LISTBOX_HEIGHT, bd = 1)
        typeofbox.place(x = 250, y = 50, width = 35)
        seriesnamebox = Listbox(mainframe, listvariable=seriesnamelist, height=LISTBOX_HEIGHT, bd = 1)
        seriesnamebox.place(x = 285, y = 50, width = 205)
        seasonbox = Listbox(mainframe, listvariable=seasonlist, height=LISTBOX_HEIGHT, bd = 1)
        seasonbox.place(x = 490, y = 50, width = 45)
        seriesbox = Listbox(mainframe, listvariable=serieslist, height=LISTBOX_HEIGHT, bd = 1)
        seriesbox.place(x = 535, y = 50, width = 40)
        suspendedbox = Listbox(mainframe, listvariable=suspendedlist, height=LISTBOX_HEIGHT, bd = 1)
        suspendedbox.place(x = 575, y = 50, width = 70)
        year2box = Listbox(mainframe, listvariable=year2list, height=LISTBOX_HEIGHT, bd = 1)
        year2box.place(x = 645, y = 50, width = 45)
        indexbox = Listbox(mainframe, listvariable=indexlist, height=LISTBOX_HEIGHT, bd = 1)
        indexbox.place(x = 690, y = 50, width = 80)

        scale1 = Scale(mainframe, command=scale_onMove_show, showvalue = 0,
                       from_=0, to=len(self.indx), length=240, orient='vertical')
        scale1.place(x = 750, y = 50)

        informframe = Canvas(mainframe, width=10, height=10, bg = 'green')
        informframe.place(x = 691, y = 317)
        ttk.Label(mainframe, textvariable=message).place(x = 691, y = 330)
     
        
        img = Image.open(r'blank.jpg')
        photo = ImageTk.PhotoImage(img)
        poster = ttk.Label(mainframe, image = photo)
        poster.photo = photo
        poster.place(x = 780, y = 35)
        
        description = Text(mainframe, width='17', height='10')
        description.place(x = 1003, y = 191)
        appHighlightFont = font.Font(family='Helvetica', size=20, weight='bold')
        rating = ttk.Label(mainframe, text = '', font = appHighlightFont)
        rating.place(x = 1000, y = 35)

        #root.bind('<Return>', new_movie_in_the_end)
        moviesbox.bind('<<ListboxSelect>>', show_movie_from_list)
        year1box.bind('<<ListboxSelect>>', show_movie_from_list)
        typeofbox.bind('<<ListboxSelect>>', show_movie_from_list)
        seriesnamebox.bind('<<ListboxSelect>>', show_movie_from_list)
        seasonbox.bind('<<ListboxSelect>>', show_movie_from_list)
        seriesbox.bind('<<ListboxSelect>>', show_movie_from_list)
        suspendedbox.bind('<<ListboxSelect>>', show_movie_from_list)
        year2box.bind('<<ListboxSelect>>', show_movie_from_list)
        indexbox.bind('<<ListboxSelect>>', show_index_from_list)

        make_listbox_list(self.position)
        
        root.mainloop()


