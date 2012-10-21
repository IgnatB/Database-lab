from databasecore import *
from uiofdata import *
from autorisation import *

user = autorisation_window()
print(user)
#user = 'aaa'
if not user == 0:
    x = IU_Dbp()
    x.open_database()
    x.IU_window(user)
