###################################################################################
#			findword						###
###################################################################################
#  query www.duckduckgo.com with arguments 					  #
#  										  #
#  usage: python3 findword.py <args>                                              #
#  e.g.:  python3 findword.py word		                                      #
#  										  #
#										  #
# this will create a file called words.txt and query www.duckduckgo.com with all   #
# the <args>, including "word".
###################################################################################


import urllib.request
import sys
import os
import pymysql
from functions import *
from stringArrayFunctions import *

###################################################################################
## 			GLOBAL VARS						###
###################################################################################
urlQuery=sys.argv[1]
args=sys.argv
strQ1=urlQuery
strPath="words.txt"
urlStandard="https://duckduckgo.com/?q=" + urlQuery
strQuery=""

#WORDS.TXT
strTags=["<br>","<a>","\"","[","]","{","}",".",":",";","</script>","<script>","<html>",
		"</html>","<a href=\\","\\",",","<div>","</div>","<body>","</body>","`",">",
		"<div","id=","/",")","(","=","0","1","2","3","4","5","6","7","8","9",
		"'","https","<!","-","en_US","<","null","_","<","js_","src_url","dev_date","url"]
global iWordCnt
global iWordIgnored

###################################################################################
## 			FUNCTIONS						###
###################################################################################

#def printDebug(strMessage):
#	print(strMessage)


def fixURL(url,strIndicator,strValue):
	#printDebug("fixUrl")
	url=url.replace(strIndicator,strValue)
	return url

#def printError(ex):
#	printDebug("ERROR")
#	e = sys.exc_info()[0]
#	e2 = sys.exc_info()[1]
#	print("<p>Error: %s</p>" % e )
#	print("<p>Error: %s</p>" % e2 )
#	raise
	

#Urllib.request the url generateda and return the resulting object
def probeURL(url):
	try:
		printDebug("ProbeUrl")
		strQuery=""
		iCnt = 0
		for strArg in sys.argv:
			#we need to ditch the first args
			#it will allways be the name of the py file.
			if iCnt==0:
				iCnt=iCnt+1
			else:
				if strQuery=="":
					strQuery=strArg.replace("_","+")
				else:
					strQuery=strQuery + "+" + strArg

		url=url.replace(args[1],strQuery)
		response=urllib.request.urlopen(url).read()
		str_page=response
		return str_page

	except Exception:
		printError(Exception)

def checkFile(strFileName):
	try:
		printDebug("fixUrl")
		#print("CheckFile")
		boDirExcists=os.path.isfile(strPath)
		if boDirExcists == False:
			#print("Creating " + strPath)
			fo=open(strPath,"a")
		else:
			print("words.txt file found!")
			print("using that !")

	except Exception:
		printError(Exception)

def ripWord(strWord):
	try:
		printDebug("ripWord")
		str_page=str(probeURL(strWord))
		for strTag in strTags:
			str_page=str_page.replace(strTag," ")

		str_page_split=str_page.split(" ")
		return str_page_split

	except Exception:
		printError(Exception)


def readLearndWords(strPath):
	try:
		printDebug("readLearndWords")
		#rf=open(strPath,"r")
		#strWords=rf.readlines()
		#rf.close()
		strValues=""
		strQ="Select word from word"
		strWords = QueryGetALLValue(strQ)
		return strWords

	except Exception:
		printError(Exception)


def checkIfKnown(strCheck):
	try:
		#printDebug("checkIfKnown")
		boReturn=False
	#	strKnownWords2=readLearndWords(strPath)
	#	for word in strKnownWords2:
	#		if word.strip()== strCheck.strip():
	#			boReturn=True
	#			return boReturn
	#	return boReturn
		#print("		readLeandWords")
		strQ="select indx from word where word='" + strCheck + "'"
		#rows=QueryGetValue(strQ)
		rows=QueryReturnRows(strQ)
		if rows!="0":
			boReturn = True

		#print("Returning: " + str(boReturn))
		return boReturn

	except Exception:
		printError(Exception)



def checkIfDouble(strCheck1, strCheckValue):
	try:
		printDebug("checkifDouble")
		boReturn=True
		#for word in strCheck1:
		#	if word.strip()== strCheckValue.strip():
		#		boReturn=True
		#		return boReturn
		#print("checkIfDouble")
		strQ="select count(indx) from word where word='" + strCheckValue + "'"
		rows=QueryGetValue(strQ)
		#print("Rows: " + rows)
		if str(rows)=="0":
			#print("Return False")
			boReturn = False

		#print("Returning: " + str(boReturn))
		return boReturn

	except Exception:
		printError(Exception)


def makeUnique(str_Page,str_Template):
	try:
		#print("Uniquefying")
		strUniqueValues=""
		for word in str_Page:
			#if checkIfDouble(str_Template,word)==False:
			if checkIfKnown(word)==False:
				#print("adding " + word)
				if len(strUniqueValues.strip())==0:
					strUniqueValues=word
				else:
					strUniqueValues=strUniqueValues + "," + word

		return strUniqueValues.split(",")

	except Exception:
		printError(Exception)

def rip(strArg, iWordIgnored1, iWordCnt1):
	try:
		iWordIgnored = 0
		iWordCnt = 0
		#print("RIPPER !!!!!!!!!!!!!!!")
		try:
			str_page_split=ripWord(fixURL(urlStandard,args[1],strArg))

			#we grab a default empty space as template to substract
			#real data from
			#printDebug("str_page_template")
			str_page_template=ripWord(fixURL(urlStandard,args[1]," "))

			#now lets make one str_page with only unique words
			#printDebug("str_page_split")
			#str_page_split=makeUnique(str_page_split,str_page_template)

			printDebug("lenght > 0 ")
			printDebug(str(len(str_page_split)))
			if len(str_page_split) !=0:

				#We can also loop through the items in the array
				#That might actually be easier
				for word in str_page_split:
					#print("======================== - " + word + " - ======================")
					if len(word.strip())>1 :
						#we need to create a table to store data in, if not excists
						createWordTable(word)
						#check if we already know the word, if not add it to the file
						if checkIfKnown(word):
							#print("IGNORED: " + word)
							iWordIgnored=iWordIgnored+1
							updateWord(word)
							print("Word updated: " + word)
						else:
							#write word to the db
							strINDX=insertWord(word)
							#f.write(word + "\n")
							print("ADDED: " + word)
							iWordCnt=iWordCnt+1

				#f.close()
			else:
				print("No page found")


		except Exception:
			e = sys.exc_info()[0]
			e2 = sys.exc_info()[1]
			print(e)
			#print("<p>Error: %s</p>" % e2 )
			raise

		return [iWordIgnored,iWordCnt]

	except Exception:
		printError(Exception)

###################################################################################
## 			Main							###
###################################################################################

try:
	print("Url probe on query "+ urlQuery)

	printDebug("Main()")
	iArgCnt=0
	checkFile(strPath)
	strKnownWords=readLearndWords(strPath)

	#connect to the database
	Connect()

	iWordIgnored=0
	iWordCnt=0
	iWordsKnownCnt=0

	for strArg in args:
		if iArgCnt==0:
			print("Skipping first argument ")
		else:
			#print("RIPPING : " + strArg)
			iWord = rip(strArg, iWordIgnored, iWordCnt)
			iWordCnt = iWord[1]
			iWordIgnored = iWord[0]
	#
	#		#recursive loop()
			while(iWordIgnored>500):
				try:
					#print("Start recursive on: " + strKnownWords[iWordsKnownCnt])
					iWord = rip(strKnownWords[iWordsKnownCnt], iWordIgnored, iWordCnt)
				except Exception:
					break
					raise
	#
				iWordsKnownCnt=iWordsKnownCnt+1
				iWordCnt = iWord[1]
				iWordIgnored = iWord[0]

				print("Words found: " + str(iWordCnt))
				print("Words Ignored: " + str(iWordIgnored))
				print("Total words: " + str(iWordCnt+iWordIgnored))

		iArgCnt=iArgCnt+1

	print("Total Words found: " + str(iWordCnt))
	print("Total Words Ignored: " + str(iWordIgnored))
	print("Total words: " + str(iWordCnt+iWordIgnored))
	print("Bye")

except Exception:
	printError(Exception)
