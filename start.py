from debug import *
from worker import *
from vars import *

#init the classes we need
debugPrint = C("HELP",iGlobalDebugLevel)
debugPrint.print("Starting program")

#the main program


#room for args stuff

#we query the myUrlPage
url = myUrlPage(strUrl)
for word in url.content:
    print(word)

#store the content in the database

#write code for interfacing cli

debugPrint.print("Bye")
