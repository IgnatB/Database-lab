import re
import time


class Dbp:
        def __init__(self):
                self.datalist = []
                self.indx = []
                self.insearchflag = 0
                self.indx_save = []
                self.indx_compare = []
                self.setyear1 = {'<Any>',}
                self.setyear2 = {'<Any>',}
                self.p = re.compile('''"?([^"]+)"?\s+                 # Название
                                  \(([\d?IVX/-]{4,})\)\s+             # Год
                                  (?:\(([VGT]{1,2})\)\s+)?            # Тип
                                  (?:(?:\{(?:((?!\(\#)[^{}]+?))?\s*)? # Название серии
                                  (?:\(\#(\d+).(\d+)\))?  \}\s+)?     # Сезон, серия
                                  (?:\{\{(SUSPENDED)\}\}\s+)?         # Отменен?
                                  ([\d?-]+)                           # Год
                                  $''',re.VERBOSE)


        def open_database(self,filename = 'E:\Coding\Python\datasets\movieslist\savemovies.list'):                
                f = open(filename, 'r')
                start = time.time()
                self.datalist.append(tuple(self.split_line(f.readline())))
                self.indx.append(0)
                for line in f:
                        self.add_last(self.split_line(line))
                finish = time.time()
                print (finish - start)
                
                f.close()

        def add_to_sets(self,y1,y2):
                if y1 == 0: y1 = '????'
                if y2 == 0: y2 = '????'
                self.setyear1.add(y1)
                self.setyear2.add(y2)


        def add_last (self,splittedline):
                self.indx.append(len(self.datalist))
                self.add_to_sets(splittedline[1],splittedline[7])
                self.datalist.append(tuple(splittedline))
                return


        def insert (self,splittedline,beforeid):
                self.indx.insert(beforeid + 1, len(self.datalist))
                self.add_to_sets(splittedline[1],splittedline[7])
                self.datalist.append(tuple(splittedline))

        def change (self,splittedline,changeid):
                self.add_to_sets(splittedline[1],splittedline[7])
                self.datalist[self.indx[changeid]] = tuple(splittedline)


        def delete (self, deleteid):
                if len(self.indx) > 1:
                    del self.indx[deleteid]
                elif len(self.indx_compare) > 0 and len(self.indx) == 1:
                    del self.indx[deleteid]
                    self.return_all_list()

##        def srt (self,num):
##                return self.datalist[num][1]

        def sort_by_name (self):
                self.indx.sort(key = lambda x: self.datalist[x][0])


        def sort_by_year1 (self):
                self.indx.sort(key = lambda x: self.datalist[x][1])


        def fypeof_key (self,num):
                if self.datalist[num][2] == None:
                        return 'z'
                else:
                        return self.datalist[num][2]
                
        def sort_by_typeof (self):
                self.indx.sort(key = self.fypeof_key)


        def seriesname_key (self,num):
                if self.datalist[num][3] == None:
                        return '\8617'
                else:
                        return self.datalist[num][3]
        
        def sort_by_seriesname (self):
                self.indx.sort(key = self.seriesname_key)


        def season_key (self,num):
                if self.datalist[num][4] == None:
                        return 1000
                else:
                        return self.datalist[num][4]

        def sort_by_season (self):
                self.indx.sort(key = self.season_key)


        def series_key (self,num):
                if self.datalist[num][5] == None:
                        return 1000
                else:
                        return self.datalist[num][5]

        def sort_by_series (self):
                self.indx.sort(key = self.series_key)
                

        def suspended_key (self,num):
                if self.datalist[num][6] == None:
                        return 2
                else:
                        return self.datalist[num][6]

        def sort_by_suspended (self):
                self.indx.sort(key = self.suspended_key)


        def sort_by_year2 (self):
                self.indx.sort(key = lambda x: self.datalist[x][7])

                                               
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
                    except: tmp[7] = 0
                    return tmp
                else:
                    return 0
                
                

        def clear_database(self):
                self.dataset = []
                

        def save(self,filename = 'E:\Coding\Python\datasets\movieslist\savemovies.list'):
                f = open(filename, 'w')
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

        def search(self,name,year1,typeof,seriesname,season,series,suspended,year2):
                m = re.match('^\t*$', name)
                if m: name = None
                else: reexpname = re.compile(name,re.IGNORECASE)
                
                m = re.match('^\t*$', seriesname)
                if m: seriesname = None
                else: reexpseriesname = re.compile(seriesname,re.IGNORECASE)
                
                if year1 == '????': year1 = '0'
                try: year1 = int(year1)
                except: year1 = None
                
                if year2 == '????': year2 = '0'
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
                self.insearchflag = 1
                self.indx_save = self.indx
                self.indx = []
                self.indx_compare = []            
                for i in self.indx_save:
                        if not name == None:
                                m = reexpname.search(self.datalist[i][0])
                                if m: pass 
                                else: continue
                        if not year1 == None:
                                if self.datalist[i][1] == year1: pass 
                                else: continue
                        if not typeof == None:
                                if self.datalist[i][2] == typeof: pass 
                                else: continue
                        if not seriesname == None:
                                if not self.datalist[i][3] == None:
                                        m = reexpseriesname.search(self.datalist[i][3])
                                else: continue
                                if m: pass 
                                else: continue
                        if not season == None:
                                if self.datalist[i][4] == season: pass 
                                else: continue
                        if not series == None:
                                if self.datalist[i][5] == series: pass 
                                else: continue
                        if not suspended == None:
                                if self.datalist[i][6] == 1: pass 
                                else: continue
                        if not year2 == None:
                                if self.datalist[i][7] == year2: pass 
                                else: continue
                        self.indx.append(i)
                        self.indx_compare.append(i)      
                if len(self.indx) == 0:
                        self.indx = self.indx_save
                        self.insearchflag = 0
                        return 0
                return len(self.indx)
                        
                                

        def return_all_list(self):
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
                if year1 == '????':
                    localyear1 = 0
                else:
                    try: localyear1 = int(year1)
                    except: return (0,'Wrong year of creation') 
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
                if year2 == '????':
                    localyear2 = 0
                else:
                    try: localyear2 = int(year2)
                    except: return (0,'Wrong year of release') 
                tmp.append(localyear2)
            else:
                return (0,'Wrong year of release')
            self.setyear1.add(tmp[1])
            self.setyear2.add(tmp[7])
            return tmp


        def print_10(self):
            j = 0
            for i in self.indx:
            #for i in self.indx[len(self.indx)-10:len(self.indx)]:
                print(j)
                print(self.datalist[i])
                j += 1
            print(':::::::::::::::::::::::::::::::::::::::::::::::::')
        
