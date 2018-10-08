import sys
import os
import pymysql
import urllib.request
import argparse


#from stringArrayFunctions import *
from functions.debugFunctions import *
from functions.arrayFunctions import *
from functions.mainFunctions import *
from functions.databaseFunctions import *

#define the parcer and help interface
parser = argparse.ArgumentParser()
parser.add_argument("-v"			, "--debug_level"				, help="Sets debug level\n '0' is the default. The higher the level set, the more information will be provided")
parser.add_argument("-r"			, "--recursive"					, help="Starts a recursive search on word:\n\npython doWord.py -r <word>\n\n\tpython doWord.py cat")
parser.add_argument("-db_tables"					, action="store_true"	, help="Shows all the tables in the 'words' database")
parser.add_argument("-reset_db_tables"					, action="store_true"	, help="Removes all data from the words database, except for the template data. CANNOT DE UNDONE !")
parser.add_argument("-process_db_tables"				, action="store_true"	, help="Loops through the 'word' table and processes all the words")
parser.add_argument("-s"			, "--show_db_table"				, help="Shows the content of <table_name> :python doWord.py --show_db_table word")
parser.add_argument("-top"			, "--show_top_words"				, help="Shows the top list of words in the words table")
parser.add_argument("-g"			, "--genesis_sead"				, help="Resets the entire db and seads with a new value: python doWord.py -g <sead_word>")
parser.add_argument("-getnext_index"					, action="store_true"	, help="Prints the next index for the word table in with the current dataset.")
parser.add_argument("-get_index"		, "--get_index"				 	, help="Prints the current index for the word table in with the current dataset.")
parser.add_argument("-query"			, "--query"					, help="Executes the query: python doWord.py -query \"<MYSQL-QUERY>\"")
parser.add_argument("-queryUrl"			, "--queryurl"					, help="Query's an url and returns the word list generated: python doWord.py -query \"<HTTP://WWW.URL.COM>\"")
parser.add_argument("-add"			, "--add_word"					, help="Adds a word to the list: python doWord.py -add \"<WORD>\"")
parser.add_argument("-createtemplate"					, action="store_true"	, help="Dumps an empty template of the search engine in the words db")
parser.add_argument("-dumpinfo"						, action="store_true"	, help="Displays some general information about the dataset")
args=parser.parse_args()
#print(args.db_tables)



#variables used
strWord=sys.argv[1]
strQUrl="https://duckduckgo.com/?q=" + strWord
strSUrl="https://duckduckgo.com/q="
strHTMLTags=["<br>","<a>","\"","[","]","{","}",".",":",";","</script>","<script>","<html>",
                "</html>","<a href=\\","\\",",","<div>","</div>","<body>","</body>","`",">",
                "<div","id=","/",")","(","=","0","1","2","3","4","5","6","7","8","9",
                "'","https","<!","-","en_US","<","null","_","<","js_","src_url","dev_date","url","URL",
		"png","%","html","DOCTYPE","&p","q","src","js","&s","&ct","NL&ss","?","a>"]


def version():
	return "2.0.2"

def ProcessWord(_word,word):
	debugprint("Entering")
	try:
		debugprint("Processing: " + _word)
		#check if we already know the word
		boKnown=boWordKnown(_word,word)
		print("====================================")
		print("Do we know the word : " + str(boKnown))
		if int(boKnown)==0:
			#not found so lets add it to word
			print("No, so lets add it: " + str(boKnown))
			addNewWordToWord(word,_word)
		else:
			#word=args.recursive
			print("Yes, so lets update it: " + str(boKnown))
			addKnownWordToWord(word,_word)

		print("====================================")
	except Exception:
		raise

	debugprint("Leaving")
	return str(_word)

def ProcessWordGenesis(_word,word):
	debugprint("Entering")
	try:
		debugprint("Generating sead: " + _word)
		#check if we already know the word
		#boKnown=boWordKnown(_word,word)
		boKnown=0
		print("====================================")
		print("Do we know the word : " + str(boKnown))
		if int(boKnown)==0:
			#not found so lets add it to word
			print("No, so lets add it: " + str(boKnown))
			addNewWordToWord(word,_word)
		else:
			#word=args.recursive
			print("Yes, so lets update it: " + str(boKnown))
			addKnownWordToWord(word,_word)

		print("====================================")
	except Exception:
		raise

	debugprint("Leaving")
	return str(_word)


def PrintSum():
	strQ="Select max(count) from word"
	strCnt=ExecuteQuery(strQ)
	strQ="Select indx from word where count='" + strCnt + "'"
	strIndx=ExecuteQuery(strQ)

	#now we got the count and the indx we can show some info
	print("Highest wordcount: " + strCnt)
	print("Words:" + strCnt)
	strQ="Select count(indx) from word"
	strWordCount=ExecuteQuery(strQ)
	print("Total words found: " + strWordCount)

def initWord(strWord):
	word=strWord
	if str(strWord)!="None":
		try:
			boTable=boTableExcists(word)
			print("Table excists:" + str(boTable))
			#print("Table lenght: " + len(boTable))
			if boTable==False:
			        #we need to create the table
			        print("Create table: " + word)
			        CreateTable(word)
		except Exception:
			raise
			print("Error creating table")

def doLoop(word):
	strQ="Select word from " + word
	cur=ReturnCursor(strQ)
	for row in cur:
		initWord(word)
		strWord=ProcessWord(str(row[0]),word)
		print("Recursive: " + strWord)
		if strWord!="":
			if len(strWord)>3:
				initWord(strWord)
				doLoop(strWord)
		else:
			return 
	PrintSum()

def doOwnLoop(word):
	strQ="Select word from " + word
	cur=ReturnCursor(strQ)
	for row in cur:
		#initWord(word)
		strWord=ProcessWord(str(row[0]),word)
		print("Recursive: " + strWord)
		#if strWord!="":
		#	if len(strWord)>3:
		#		#initWord(strWord)
		#		doLoop(strWord)
		#else:
		#	return 
	PrintSum()

def globalReset():
	print("Removing all databases and emptying 'word'")
	strQ="show tables"
	cur=ReturnCursor(strQ)
	print("-----------")
	for row in cur:
		strRow=row[0]
		if strRow != "word":
			print("Deleting " + strRow)
			strQ1="drop table " + strRow
			ExecuteQuery(strQ1)

	#clean up the word table
	strQ2="delete from word"
	ExecuteQuery(strQ2)
	print("-----------")

def queryURL(strQUrl,strSUrl):
	debugprint("Entering")
        #first we query the url 
	debugprint("requesting url")
	response=urllib.request.urlopen(strQUrl).read()
	str_page=response

	#then we get the empty page so we can substract all the html tagging
	debugprint("reading response")
	response=urllib.request.urlopen(strSUrl).read()
	str_page_standard=response

	#clean up
	debugprint("cleaning up the data set")
	str_ListWords=replaceWordsFromArrayWithStringInString(str(str_page),strHTMLTags," ").split(" ")
	debugprint("Removing empty entries")
	str_ListWords=removeEmptyItemsFromArray(str_ListWords)

	debugprint("Leaving")
	return str_ListWords




#Main Functions
if args.debug_level:
	gboDebugLevel=args.debug_level
	setDebugLevel(gboDebugLevel)
	debugprint("Setting debug level to: " + str(gboDebugLevel))
if args.dumpinfo:
	PrintSum()
if args.createtemplate:
	initWord("Template")
	strList=queryURL("http://www.duckduckgo.com",strSUrl)
	for word in strList:
		ProcessWord(word,"Template")
if args.queryurl:
	strList=queryURL(args.queryurl,strSUrl)
	for word in strList:
		print(word)
if args.add_word:
	ProcessWord("word",args.add_word)
	print(args.add_word)
if args.get_index:
	strInx=getIndx(args.get_index,"word")
	print(strInx)
if args.query:
	printQuery(args.query)
if args.getnext_index:
	strNextINDX=getNextINDX()
	print(strNextINDX)
if args.genesis_sead:
	strWord=args.genesis_sead
	print("Clears the db and seads with genesis word:" + str(args.genesis_sead))
	globalReset()
	print("Removing all databases and emptying 'word'")
	initWord(strWord)
	print("processing word")
	ProcessWordGenesis(strWord,"template")
	print("Now recursive probing")
	doOwnLoop(strWord)
if args.show_top_words:
	print("Show top words still has to be implemented")
	print("Number of top words: " + args.show_top_words)
if args.show_db_table:
	try:
		strQ="Select * from " + args.show_db_table
		printQuery(strQ)
	except:
		print("==========================  ERROR ==========================================")
		print("There was an error. Are you sure table: " + args.show_db_table + " excists ?")
		print("==========================  ERROR ==========================================")
#if args.parse_known_args:
#	print("Argument unknown, please use -h for help")
if args.recursive:
	print("Starting " + version())
	print("Querying on word: " + strWord)

	strArg=args
	str_ListWords=queryURL(strQUrl,strSUrl)


	#We need to create the table for datastorage
	word=args.recursive
	print("init word")
	initWord(word)

	#we continue with the code


	#we now have an array of words we can loop through
	for _word in str_ListWords:
		#print("================================================================" + _word  + "," +  word + "=======================================================================")
		print("ProcessWord: " + _word + "," + word)
		ProcessWord(_word,word)
		#print("===================================================================================================================================================================")

	#now lets loop through the words and itterate them
	try:
		doOwnLoop(word)
	except:
		pass


if args.db_tables:
	print("Listing all tables in words")
	strQ="show tables"
	cur=ReturnCursor(strQ)
	print("-----------")
	for row in cur:
		print(row[0])
	print("-----------")

if args.reset_db_tables:
	globalReset()
if args.process_db_tables:
	print("Processing word table")
	strQ="select word from word"
	cur=ReturnCursor(strQ)
	#print("-----------")
	for row in cur:
		strRow=row[0]
		if str(strRow)!="None":
			initWord(strRow)
			ProcessWord(strRow,strRow)
	#print("-----------")


print("Bye!")
