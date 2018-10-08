from debug import *
from functions.mainFunctions import *
from vars import *
import urllib.request

debugPrint = C("HELP",2)

class myUrlPage:

    def __init__(self, url):
        def queryURL():
            debugPrint.print("Entering")
            #first we query the url
            debugPrint.print("requesting url")
            response=urllib.request.urlopen(self.url).read()
            str_page=response

            #then we get the empty page so we can substract all the html tagging
            debugPrint.print("reading response")
            response=urllib.request.urlopen(self.url).read()
            str_page_standard=response

        	#clean up
            debugPrint.print("cleaning up the data set")
            str_ListWords=replaceWordsFromArrayWithStringInString(str(str_page),strHTMLTags," ").split(" ")
            debugPrint.print("Removing empty entries")
            str_ListWords=removeEmptyItemsFromArray(str_ListWords)

            debugPrint.print("Leaving")
            return str_ListWords

        self.url = url
        self.content=queryURL()
        #debugPrint = C("myUrlPage",2)
        #self.html = html
        #print("Self done")

    def printNames(self):
        #print("Hello my name is " + self.name)
        print(self.url)
