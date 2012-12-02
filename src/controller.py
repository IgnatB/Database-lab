#!/usr/bin/python3
# -*- coding: utf-8 -*-

from model import *
from view import *

class Controller:
    def __init__(self, root, user, filename):
        """Инициализация контроллера, присваивание каждому элементу меню его функции.
        """
        self.model = Model()
        time = self.model.open_database(filename)
        self.view = View(root, user, time)
        self.view.insertButton.config(command=self.new_movie_insert)
        self.view.deleteButton.config(command=self.delete_movie)
        self.view.changeButton.config(command=self.change_movie)
        self.view.appendButton.config(command=self.append_movie)
        self.view.saveButton.config(command=self.save_all)
        self.view.searchButton.config(command=self.search_and_show)
        self.view.showallButton.config(command=self.show_all)
        
        self.view.sortnameButton.config(command=self.sort_name_show)
        self.view.sortyear1Button.config(command=self.sort_year1_show)
        self.view.sorttypeofButton.config(command=self.sort_typeof_show)
        self.view.sortseriesnameButton.config(command=self.sort_seriesname_show)
        self.view.sortseasonButton.config(command=self.sort_season_show)
        self.view.sortseriesButton.config(command=self.sort_series_show)
        self.view.sortsuspendedButton.config(command=self.sort_suspended_show)
        self.view.sortyear2Button.config(command=self.sort_year2_show)

        self.view.upButton.config(command=self.move_list_up)
        self.view.downButton.config(command=self.move_list_down)
        self.view.pageupButton.config(command=self.move_list_page_up)
        self.view.pagedownButton.config(command=self.move_list_page_down)
        self.view.scale1.config(command=self.scale_onMove_show)
        self.view.scale1.config(to=self.model.length())

        self.view.moviesbox.bind('<<ListboxSelect>>', self.show_movie_from_list)
        self.view.year1box.bind('<<ListboxSelect>>', self.show_movie_from_list)
        self.view.typeofbox.bind('<<ListboxSelect>>', self.show_movie_from_list)
        self.view.seriesnamebox.bind('<<ListboxSelect>>', self.show_movie_from_list)
        self.view.seasonbox.bind('<<ListboxSelect>>', self.show_movie_from_list)
        self.view.seriesbox.bind('<<ListboxSelect>>', self.show_movie_from_list)
        self.view.suspendedbox.bind('<<ListboxSelect>>', self.show_movie_from_list)
        self.view.year2box.bind('<<ListboxSelect>>', self.show_movie_from_list)
        self.view.indexbox.bind('<<ListboxSelect>>', self.show_index_from_list)
 
        self.refresh_yearboxes()
        self.make_listbox_list()


    def new_movie_insert (self):
        """Вставляет новое кино
        
        mas - массив данных, None в случае неправильного ввода
        idn - айди записи
        """
        mas, idn = self.view.insert_interface(self.model.length())
        if not mas == None:
            self.model.insert(mas, idn)
            self.refresh_yearboxes()
            self.make_listbox_list()
            

    def delete_movie (self):
        """Удаляет кино
        
        idn - айди удаляемой записи, False в случае неправильного ввода
        """
        idn = self.view.delete_interface(self.model.length())
        if not idn == None:
            self.model.delete(idn)
            self.refresh_yearboxes()
            self.make_listbox_list()
            
        
    def change_movie (self):
        """Меняет данные о кино
        
        mas - массив данных, None в случае неправильного ввода
        idn - айди записи
        """
        mas, idn = self.view.change_interface(self.model.length())
        if not mas == None:
            self.model.change(mas, idn)
            self.refresh_yearboxes()
            self.make_listbox_list()


    def append_movie (self):
        """Добавляет кино в конец
        
        mas - массив данных, None в случае неправильного ввода
        """
        mas = self.view.append_interface()
        if not mas == None:
            self.model.add_last(mas)
            self.refresh_yearboxes()
            self.make_listbox_list()
                 

    def save_all (self):
        """Сохранить базу данных
        """
        filename = self.view.save()
        if self.model.save(filename):
            self.view.alarm_message('Saved', 'green')
        else:
            self.view.alarm_message('No File', 'red')


    def search_and_show(self):
        """Поиск
        """
        find = self.model.search(self.view.searchname.get(), self.view.boxyear1.get(),
                           self.view.vartypeof.get(), self.view.searchseriesname.get(),
                           self.view.searchseason.get(), self.view.searchseries.get(),
                           self.view.varsuspended.get(), self.view.boxyear2.get())
        if find == 0:
            self.view.alarm_message('Search Failed', 'red')
            self.view.listposition = 0
            self.make_listbox_list()      
        else:
            self.view.alarm_message('Finded: ' + str(find), 'green')
            self.view.listposition = 0
            self.make_listbox_list()
                

    def show_all(self):
        """Показывает всю базу данных
        """
        self.view.listposition = 0
        self.model.return_all_list()
        self.make_listbox_list()
        

    def sort_name_show(self):
        """Сортировать по имени
        """
        self.view.listposition = 0
        self.model.sort_by_name()
        self.make_listbox_list()
   
        
    def sort_year1_show(self):
        """Сортировать по году создания
        """
        self.view.listposition = 0
        self.model.sort_by_year1()
        self.make_listbox_list()
 
        
    def sort_typeof_show(self):
        """Сортировать по типу
        """
        self.view.listposition = 0
        self.model.sort_by_typeof()
        self.make_listbox_list()
  
        
    def sort_seriesname_show(self):
        """Сортировать по имени серии
        """
        self.view.listposition = 0
        self.model.sort_by_seriesname()
        self.make_listbox_list()
  
        
    def sort_season_show(self):
        """Сортировать по сезону
        """
        self.view.listposition = 0
        self.model.sort_by_season()
        self.make_listbox_list()
        
    def sort_series_show(self):
        """Сортировать по номкру серии
        """
        self.view.listposition = 0
        self.model.sort_by_series()
        self.make_listbox_list()
   
        
    def sort_suspended_show(self):
        """Сортировать по отменонности
        """
        self.view.listposition = 0
        self.model.sort_by_suspended()
        self.make_listbox_list()
    
        
    def sort_year2_show(self):
        """Сортировать по году выпуска
        """
        self.view.listposition = 0
        self.model.sort_by_year2()
        self.make_listbox_list()
        

    def move_list_down(self):
        """Прокрутка списка на один вниз
        """
        if self.view.listposition < len(self.model.indx) - self.view.LISTBOX_HEIGHT:
            self.view.listposition += 1
            self.make_listbox_list()
                      

    def move_list_up(self):
        """Прокрутка списка на один вверх
        """
        if self.view.listposition > 0:
            self.view.listposition -= 1
            self.make_listbox_list()
            
            
    def move_list_page_down(self):
        """Прокрутка списка на один вниз
        """
        if self.view.listposition < len(self.model.indx) - self.view.LISTBOX_HEIGHT:
            self.view.listposition += self.view.LISTBOX_HEIGHT
            self.make_listbox_list()
                      

    def move_list_page_up(self):
        """Прокрутка списка на один вверх
        """
        if self.view.listposition > 0:
            self.view.listposition -= self.view.LISTBOX_HEIGHT
            if self.view.listposition < 0:
                self.view.listposition = 0
            self.make_listbox_list()
            

    def scale_onMove_show(self, pos):
        """Прокрутка списка подзунком
        """
        self.view.listposition = int(pos)
        self.make_listbox_list()
        

    def show_movie_from_list(self, *args):  
        """Показать выделенное в полях для ввода
        """    
        selected_id = self.view.listposition + self.view.selection_return()
        item = self.model.give_element(selected_id)
        self.view.show_selected_movie(selected_id, item)      


    def show_index_from_list(self, *args):
        """Вывести выделенное айди в поле для ввода
        """
        self.view.idnumber.set(self.view.listposition + int(self.view.indexbox.curselection()[0]))

                
    def make_listbox_list(self):
        """Обновить выводимый список
        """
        pieceOfData = self.model.give_slice(self.view.listposition,
                                            self.view.listposition + self.view.LISTBOX_HEIGHT)
        self.view.show_listbox_list(pieceOfData, self.model.length())
    
        
    def refresh_yearboxes(self):
        """Обновить множества годов
        """
        self.view.boxyear1.config(values = ['<Any>'] + [x for x in self.model.dictyear1.keys()])
        self.view.boxyear2.config(values = ['<Any>'] + [x for x in self.model.dictyear2.keys()])
