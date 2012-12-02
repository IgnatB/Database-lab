#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import time


class Model:
    def __init__(self):
        """Инициализализация класса даннных
        
        datalist - список значений элементов, возможно только добавление элементов
        indx - список ссылок на элементы в datalist, на экран выводится этот список
        insearchflag - работаем ли с списком найденых элементов
        indx_save - сохраняет таблицу indx во время поиска
        indx_compare - первоначально найденные элементы
        dictyear1..dictsuspended - словари для поиска по индексу  
        p - регулярное выражения для парсинга файла данных    
        """      
        self.datalist = []
        self.indx = []
        self.insearchflag = 0
        self.indx_save = []
        self.indx_compare = []
        self.dictyear1 = dict()
        self.dicttypeof = dict()
        self.dictyear2 = dict()
        self.dictseason = dict()
        self.dictseries = dict()
        self.dictsuspended = {None : set(), 1 : set()}
        self.p = re.compile('''"?([^"]+)"?\s+                 # Название
                          \(([\d?IVX/-]{4,})\)\s+             # Год
                          (?:\(([VGT]{1,2})\)\s+)?            # Тип
                          (?:(?:\{(?:((?!\(\#)[^{}]+?))?\s*)? # Название серии
                          (?:\(\#(\d+).(\d+)\))?  \}\s+)?     # Сезон, серия
                          (?:\{\{(SUSPENDED)\}\}\s+)?         # Отменен?
                          ([\d?-]+)                           # Год
                          $''', re.VERBOSE)


    def open_database(self, filename='E:\Coding\Python\datasets\movieslist\shortmovies.list'):
        """Читает данные из файла filename
        
        Разделляя каждую строку на элементы с
        помощью split_line и добавляя ее в конец indx c помощью add_last
        Возвращает время чтения файла
        """
        try: f = open(filename, 'r')
        except: return "Can't open file"
        start = time.time()
        try: self.datalist.append(tuple(self.split_line(f.readline())))
        except: return "Can't open file"
        self.indx.append(0)
        for line in f:
            self.add_last(self.split_line(line))
        finish = time.time()   
        f.close()
        if len(self.datalist) == 0:
            return "Can't open file"
        return str(finish - start) 


    def add_to_sets(self, position, y1, typeof, season, series, suspended, y2):
        """Добавляет элементы в словари
        
        Где каждому значению соответствует индекс элемента,который его хранит
        """
        if y1 == 0: y1 = '????'
        if y1 not in self.dictyear1:
            self.dictyear1[y1] = set()
        self.dictyear1[y1].add(position)
        
        if y2 == 0: y2 = '????'
        if y2 not in self.dictyear2:
            self.dictyear2[y2] = set()
        self.dictyear2[y2].add(position)
        
        if not typeof == None:
            if typeof not in self.dicttypeof:
                self.dicttypeof[typeof] = set()
            self.dicttypeof[typeof].add(position)
        
        if not season == None:
            if season not in self.dictseason:
                self.dictseason[season] = set()
            self.dictseason[season].add(position)
            
        if not series == None:
            if series not in self.dictseries:
                self.dictseries[series] = set()
            self.dictseries[series].add(position)
            
        self.dictsuspended[suspended].add(position)
 
        
    def del_from_sets (self, position, y1, typeof, season, series, suspended, y2):
        """Удаляет элементы из словаря      
        """
        if y1 == 0: y1 = '????'
        self.dictyear1[y1].discard(position)
        if len(self.dictyear1[y1]) == 0:
            del self.dictyear1[y1]     
    
        if y2 == 0: y2 = '????'
        self.dictyear2[y2].discard(position)
        if len(self.dictyear2[y2]) == 0:
            del self.dictyear2[y2]
            
        if not typeof == None:
            self.dicttypeof[typeof].discard(position)
            if len(self.dicttypeof[typeof]) == 0:
                del self.dicttypeof[typeof]
      
        if not season == None:
            self.dictseason[season].discard(position)
            if len(self.dictseason[season]) == 0:
                del self.dictseason[season]
                      
        if not series == None:
            self.dictseries[series].discard(position)
            if len(self.dictseries[series]) == 0:
                del self.dictseries[series]
                     
        self.dictsuspended[suspended].discard(position)


    def add_last (self, splittedline):
        """Записывает запись в конец datalist
        
        добавляет в конец indx
        позицию в массиве datalist записаной записи
        splittedline - запись уже разбитая по элементам
        """
        if not splittedline == 0:
            self.indx.append(len(self.datalist))
            self.add_to_sets(len(self.datalist), splittedline[1], splittedline[2],
                                                 splittedline[4], splittedline[5], 
                                                 splittedline[6], splittedline[7])
            self.datalist.append(tuple(splittedline))


    def insert (self, splittedline, beforeid):
        """ Записывает запись в конец datalist
    
        добавляет после beforeid в indx
        позицию в массиве datalist записаной записи
        splittedline - запись уже разбитая по элементам
        """
        if not splittedline == 0:
            self.indx.insert(beforeid + 1, len(self.datalist))
            self.add_to_sets(len(self.datalist), splittedline[1], splittedline[2],
                                                 splittedline[4], splittedline[5], 
                                                 splittedline[6], splittedline[7])
            self.datalist.append(tuple(splittedline))


    def change (self, splittedline, changeid):
        """ Изменяет запись 
        
        в datalist[indx[changeid]]
        splittedline - запись уже разбитая по элементам
        """
        if not splittedline == 0:
            self.del_from_sets(self.indx[changeid], self.datalist[self.indx[changeid]][1], self.datalist[self.indx[changeid]][2],
                                                    self.datalist[self.indx[changeid]][4], self.datalist[self.indx[changeid]][5], 
                                                    self.datalist[self.indx[changeid]][6], self.datalist[self.indx[changeid]][7])
            self.add_to_sets(self.indx[changeid], splittedline[1], splittedline[2],
                                                  splittedline[4], splittedline[5], 
                                                  splittedline[6], splittedline[7])
            self.datalist[self.indx[changeid]] = tuple(splittedline)


    def delete (self, deleteid):
        """Удаляет запись indx[deleteid], но не удаляет в datasets
        """
        if len(self.indx) > 1:
            self.del_from_sets(self.indx[deleteid], self.datalist[self.indx[deleteid]][1], self.datalist[self.indx[deleteid]][2],
                                                    self.datalist[self.indx[deleteid]][4], self.datalist[self.indx[deleteid]][5], 
                                                    self.datalist[self.indx[deleteid]][6], self.datalist[self.indx[deleteid]][7])
            del self.indx[deleteid]
        elif len(self.indx_compare) > 0 and len(self.indx) == 1:
            self.del_from_sets(self.indx[deleteid], self.datalist[self.indx[deleteid]][1], self.datalist[self.indx[deleteid]][2],
                                                    self.datalist[self.indx[deleteid]][4], self.datalist[self.indx[deleteid]][5], 
                                                    self.datalist[self.indx[deleteid]][6], self.datalist[self.indx[deleteid]][7])
            del self.indx[deleteid]
            self.return_all_list()


    def length(self):
        """Возвращает размер базы данных
        """
        return len(self.indx)


    def sort_by_name (self):
        """Сортирует по имени, изменяя indx
        """
        self.indx.sort(key=lambda x: self.datalist[x][0])


    def sort_by_year1 (self): 
        """Сортирует по году создания, изменяя indx
        """     
        self.indx.sort(key=lambda x: self.datalist[x][1])


    def fypeof_key (self, num):
        """Формирует ключ для sort_by_typeof
        """
        if self.datalist[num][2] == None:
                return 'z'
        else:
                return self.datalist[num][2]
   
            
    def sort_by_typeof (self):
        """Сортирует по типу, изменяя indx
        """
        self.indx.sort(key=self.fypeof_key)


    def seriesname_key (self, num):
        """Формирует ключ для sort_by_seriesname
        """
        if self.datalist[num][3] == None:
                return '\8617'
        else:
                return self.datalist[num][3]
  
    
    def sort_by_seriesname (self):
        """Сортирует по имени серии, изменяя indx
        """
        self.indx.sort(key=self.seriesname_key)


    def season_key (self, num):
        """Формирует ключ для sort_by_season
        """
        if self.datalist[num][4] == None:
                return 1000
        else:
                return self.datalist[num][4]


    def sort_by_season (self):
        """Сортирует по сезону, изменяя indx
        """
        self.indx.sort(key=self.season_key)


    def series_key (self, num):
        """Формирует ключ для sort_by_series
        """
        if self.datalist[num][5] == None:
                return 1000
        else:
                return self.datalist[num][5]


    def sort_by_series (self):
        """Сортирует по серии, изменяя indx
        """
        self.indx.sort(key=self.series_key)
            

    def suspended_key (self, num):
        """Формирует ключ для sort_by_suspended
        """
        if self.datalist[num][6] == None:
                return 2
        else:
                return self.datalist[num][6]


    def sort_by_suspended (self):
        """Сортирует по отмененности, изменяя indx
        """
        self.indx.sort(key=self.suspended_key)


    def sort_by_year2 (self):
        """Сортирует по году выпуска, изменяя indx
        """
        self.indx.sort(key=lambda x: self.datalist[x][7])

                                           
    def split_line (self, line):
        """Разбивает строку line на элементы 
        
        с помощью регулярного выражения p
        Возвращает уже разбитую строку или 0 в случае неправильной строки
        """
        m = self.p.match(line)
        if m:
            tmp = list(m.groups())
            try: tmp[1] = int(tmp[1][0:4])
            except: tmp[1] = 0
            try: tmp[4] = int(tmp[4])
            except: pass
            try: tmp[5] = int(tmp[5])
            except: pass
            if not tmp[6] == None : tmp[6] = 1
            try: tmp[7] = int(tmp[7][0:4])
            except: tmp[7] = 0
            return tmp
        else:
            return 0
         

    def save(self, filename='movies.list'):
        """Сохраняет базу данных 
        
        в указаный файл, преобразуя записи в строки определенного шаблона
        """
        try: f = open(filename, 'w')
        except: return 0
        for i in self.indx:
            line = self.datalist[i][0]
            if self.datalist[i][1] == 0:
                line = line + ' (????) '
            else:
                line = line + ' (' + str(self.datalist[i][1]) + ') '
            if not self.datalist[i][2] == None:
                line = line + '(' + self.datalist[i][2] + ') '
            if (not self.datalist[i][3] == None) or (not self.datalist[i][4] == None):
                line = line + '{'
            if not self.datalist[i][3] == None:
                line = line + self.datalist[i][3]
            if not self.datalist[i][4] == None:
                line = line + '(#' + str(self.datalist[i][4]) + '.' + str(self.datalist[i][5]) + ')'
            if (not self.datalist[i][3] == None) or (not self.datalist[i][4] == None):
                line = line + '} '
            if not self.datalist[i][6] == None:
                line = line + '{{SUSPENDED}} '
            if self.datalist[i][7] == 0:
                line = line + '????\n' 
            else:
                line = line + str(self.datalist[i][7]) + '\n'   
            f.write(line)
        f.close()
        return 1


    def search(self, name, year1, typeof, seriesname, season, series, suspended, year2):
        """Индексированый поиск в базе данных 
        
        по указаным параметрам
        Возвращает количество найденых элементов если что то найдет
        """
        m = re.match('^\t*$', name)
        if m: name = None
        else: reexpname = re.compile(name, re.IGNORECASE)
        
        m = re.match('^\t*$', seriesname)
        if m: seriesname = None
        else: reexpseriesname = re.compile(seriesname, re.IGNORECASE)
        
        if year1 == '????': pass
        else:
            try: year1 = int(year1)
            except: year1 = None
        
        if year2 == '????': pass
        else:
            try: year2 = int(year2)
            except: year2 = None

        if typeof == '0': typeof = None
        
        try: season = int(season)
        except: season = None
        
        try: series = int(series)
        except: series = None
        
        if not suspended == 1: suspended = None

        if name == year1 == typeof == seriesname == season == series == suspended == year2 == None:
            return 0

        if self.insearchflag == 1:
            self.return_all_list()
            
        somefind = set()
        dictandkey = [(self.dictyear1,year1),(self.dictyear2,year2),
                        (self.dicttypeof,typeof),(self.dictseries,series),
                        (self.dictseason,season),(self.dictsuspended,suspended)]
        for (dictionary, key) in dictandkey:
            if not key == None:
                if not key in dictionary:
                    return 0
                if len(somefind) == 0:
                    somefind = dictionary[key]
                else:
                    somefind = somefind & dictionary[key]
                if len(somefind) == 0:
                    return 0  
                
        if len(somefind) == 0:
            for i in self.indx:
                somefind.add(i)
        self.insearchflag = 1
        self.indx_save = self.indx
        self.indx = []
        self.indx_compare = []  
                        
        for i in somefind:
            if not name == None:
                m = reexpname.search(self.datalist[i][0])
                if m: pass 
                else: continue
            if not seriesname == None:
                if not self.datalist[i][3] == None:
                    m = reexpseriesname.search(self.datalist[i][3])
                else: continue
                if m: pass 
                else: continue
            self.indx.append(i)
            self.indx_compare.append(i)      
        if len(self.indx) == 0:
            self.indx = self.indx_save
            self.insearchflag = 0
            return 0
        return len(self.indx)
                                        

    def return_all_list(self):
        """Возвращает всю базу данных при выходе из поиска,
        
        обновляет базу данных в соответствии с изменениями, которые произошли со списком поиска
        """
        if self.insearchflag == 1:
            changed_search = set(self.indx)
            original_search = set(self.indx_compare)
            to_delete = original_search - changed_search
            to_add = changed_search - original_search
            self.insearchflag = 0
            self.indx = self.indx_save
            for del_el in to_delete:
                del self.indx[self.indx.index(del_el)]
            for add_el in to_add:
                self.indx.append(add_el)


    def give_slice(self, begin, end):
        """Возвращает срез базы данных от элемента begin до элемента end
        """
        return [self.datalist[i] for i in self.indx[begin : end]]


    def give_element(self, selection):
        """Возвращает элемент по номеру selection из базы данных
        """
        return self.datalist[self.indx[selection]]
