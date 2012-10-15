import re
import time


class Dbp:
        def __init__(self):
                self.datalist = []
                self.index = []
                self.setyear1 = set()
                self.setyear2 = set()
                self.p = re.compile('''"?([^"]+)"?\s+                 # Название
                                  \(([\d?IVX/-]{4,})\)\s+             # Год
                                  (?:\(([VGT]{1,2})\)\s+)?            # Тип
                                  (?:(?:\{(?:((?!\(\#)[^{}]+?))?\s*)? # Название серии
                                  (?:\(\#(\d+).(\d+)\))?  \}\s+)?     # Сезон, серия
                                  (?:\{\{(SUSPENDED)\}\}\s+)?         # Отменен?
                                  ([\d?-]+)                           # Год
                                  $''',re.VERBOSE)


        def open_database(self,filename = 'E:\Coding\Python\datasets\movieslist\shortmovies.list'):                
                f = open(filename, 'r')
                start = time.time()
                self.datalist.append(tuple(self.split_line(f.readline())))
                self.index.append(0)
                for line in f:
                        self.add_last(self.split_line(line))
                finish = time.time()
                print (finish - start)
                
                f.close()


        def add_last (self,splittedline):
                self.index.append(len(self.datalist))
                self.datalist.append(tuple(splittedline))
                return


        def insert (self,splittedline,beforeid):
                self.index.insert(beforeid + 1, len(self.datalist))
                self.datalist.append(tuple(splittedline))                       
                print('done1111')

        def delete (self, deleteid):
                del self.index[deleteid]

        def srt (self,num):
                return self.datalist[num][1]

        def sort_by_year (self):
                self.index.sort(key = lambda x: self.datalist[x][1])

                                               
        def split_line (self,line):
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
                    except: tmp[7] = None
                    self.setyear1.add(tmp[1])
                    self.setyear2.add(tmp[7])
                    return tmp
                else:
                    return 0
                
                

        def clear_database(self):
                self.dataset = []


        def enter_check(self,name, year1, typeof, seriesname,
                        season, series, suspended, year2):
            tmp=[]           
            m = re.match('\s*([^"(){}]+)',name)
            if m:
                tmp.append(m.group(1))
            else:
                return (0,'Wrong name')               
            m = re.match('^[?\d]{4,4}$',year1)
            if m:
                try: localyear1 = int(year1)
                except: localyear1 = None
                tmp.append(localyear1)
            else:
                return (0,'Wrong year of creation')              
            m = re.match('^[VGTvgt]{1,2}$',typeof)
            if m:
                tmp.append(typeof.upper())
            elif typeof == '':
                tmp.append(None)
            else:
                return (0,'Wrong type')               
            m = re.match('\s*([^"(){}]+)',seriesname)
            if m:
                tmp.append(m.group(1))
            elif seriesname == '':
                tmp.append(None)
            else: 
                return (0,'Wrong series name')               
            m = re.match('^\d+$',season)
            m1 = re.match('^\d+$',series)
            if m and m1:
                tmp.append(int(season))
                tmp.append(int(series))
            elif season == '' and series == '':
                tmp.append(None)
                tmp.append(None)
            else:
                return (0,'Wrong season or series')               
            m = re.match('SUSPENDED',suspended)
            if m:
                tmp.append(1)
            elif suspended == '':
                tmp.append(None)
            else:
                return (0,'So suspended or not?')
            m = re.match('^[?\d]{4,4}$',year2)
            if m:
                try: localyear2 = int(year2)
                except: localyear2 = None
                tmp.append(localyear2)
            else:
                return (0,'Wrong year of release')
            self.setyear1.add(tmp[1])
            self.setyear2.add(tmp[7])
            return tmp


        def print_10(self):
            j = 0
            for i in self.index:
            #for i in self.index[len(self.index)-10:len(self.index)]:
                print(j)
                print(self.datalist[i])
                j += 1
            print(':::::::::::::::::::::::::::::::::::::::::::::::::')
        
