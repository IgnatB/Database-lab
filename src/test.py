
import unittest
import model

class Test(unittest.TestCase):

    lines_from_file = (('"$2 Bill" (2002) {Secret Machines and The Killers (#3.3)}    2004', 
               ['$2 Bill',2002,None,'Secret Machines and The Killers',3,3,None,2004]),
              ('"Sputnik" (1989) {(1991-02-04)}                1991', 
               ['Sputnik',1989,None,'(1991-02-04)',None,None,None,1991]),
              ('Moldiver (????) (V) {{SUSPENDED}}            ????',
               ['Moldiver',0,'V',None,None,None,1,0]),
              ('"Children of Stalinism" (2010) {For My Dad (#1.1)}    2010',
               ['Children of Stalinism',2010,None,'For My Dad',1,1,None,2010]),
              ('All Amateur Video #16: "Creampie Surprise" (2004) (V)    2004',
               0))


    def test_model_split_line(self): 
        md = model.Model()
        for line, elements in self.lines_from_file:
            result = md.split_line(line)
            self.assertEqual(result, elements)
            
     
    def test_model_open_file(self): 
        md = model.Model()
        tst = md.open_database('shotmovies.list')
        self.assertEqual(tst, "Can't open file") 
        tst = md.open_database('E:\Coding\Python\epydoc-3.0.1.win32')
        self.assertEqual(tst, "Can't open file")     

       
    def test_model_length(self): 
        md = model.Model()
        md.open_database('shortmovies.list')   
        tst = md.length()
        self.assertEqual(tst, 37)   
        
        
    def test_model_add_to_sets(self): 
        md = model.Model()
        md.open_database('shortmovies.list')   
        md.add_to_sets(37, 2222, 'TV', 77, 77, 1, 2222)
        self.assertEqual(md.dictyear1[2222], {37,})   
        self.assertEqual(md.dicttypeof['TV'], {37,})
        self.assertEqual(md.dictseason[77], {37,})
        self.assertEqual(md.dictseries[77], {37,})
        self.assertEqual(md.dictsuspended[1], {37,12,28})
        self.assertEqual(md.dictyear2[2222], {37,})
 
        
    def test_model_del_from_sets(self): 
        md = model.Model()
        md.open_database('shortmovies.list') 
        self.assertEqual(md.dictyear1['????'], {12,})   
        self.assertEqual(md.dictsuspended[1], {12,28})
        self.assertEqual(md.dictyear2['????'], {12,28})
        md.del_from_sets(12, 0, None, None, None, 1, 0)
        self.assertEqual('????' in md.dictyear1, False)   
        self.assertEqual(md.dictsuspended[1], {28,})
        self.assertEqual(md.dictyear2['????'], {28,})

        
    def test_model_add_last(self): 
        md = model.Model()
        md.open_database('shortmovies.list')
        md.add_last(['I Hate Vegans',2012,None,None,None,None,None,2012])
        self.assertEqual(md.datalist[md.indx[-1]], ('I Hate Vegans',2012,None,None,None,None,None,2012))
 
        
    def test_model_insert(self): 
        md = model.Model()
        md.open_database('shortmovies.list')
        md.insert(['I Hate Vegans',2012,None,None,None,None,None,2012], 14)
        self.assertEqual(md.datalist[md.indx[15]], ('I Hate Vegans',2012,None,None,None,None,None,2012))
        
    
    def test_model_change(self): 
        md = model.Model()
        md.open_database('shortmovies.list')
        md.change(['I Hate Vegans',2012,None,None,None,None,None,2012], 14)
        self.assertEqual(md.datalist[md.indx[14]], ('I Hate Vegans',2012,None,None,None,None,None,2012))

        
    def test_model_delete(self): 
        md = model.Model()
        md.open_database('shortmovies.list')
        md.delete(14)
        self.assertEqual(md.length(),36)
        
        
    def test_model_search(self): 
        md = model.Model()
        md.open_database('shortmovies.list')
        tst = md.search('Evil Bong','2007','0','','','',0,'')
        self.assertEqual(tst,0)
        tst = md.search('','<Any>','0','','','',0,'2000')
        self.assertEqual(tst,3)
        tst = md.search('','2006','0','','','',0,'')
        self.assertEqual(tst,1)
        
    
    def test_model_give_slice(self): 
        md = model.Model()
        md.open_database('shortmovies.list')
        tst = md.give_slice(0,4)
        self.assertEqual(tst,[('Awesome Movie', 2012, None, None, None, None, None, 2012), 
                              ('BASEketball', 1998, None, None, None, None, None, 1998), 
                              ('Digital Cinema Solutions', 2003, 'V', None, None, None, None, 2003), 
                              ('Bharathchandran I.P.S', 2005, None, None, None, None, None, 2005)])
        
        
    def test_model_give_element(self): 
        md = model.Model()
        md.open_database('shortmovies.list')
        tst = md.give_element(4)
        self.assertEqual(tst,('Bharatheeyam', 1997, None, None, None, None, None, 1997))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()