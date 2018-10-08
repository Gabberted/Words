import argparse
import inspect


from debugFnct import *
from queryURL import *
from dbConn import *
from vars import *
from arrayFunctions import *
from gui import *
from fileFnct import *

def createParser():
	debugprint("Entering")
	debugprint("initializing Argument Parser")
	parser = argparse.ArgumentParser()
	parser.add_argument("-v"			, "--debug_level"				, help="Sets debug level\n '0' is the default. The higher the level set, the more information will be provided")
	parser.add_argument("-listCount"		, "--listCount"					, help="Lists words with the count specified")
	parser.add_argument("-qpage"			, "--qpage"					, help="Queries a page and returns content")
	parser.add_argument("-qgurlret"			, "--qgurlret"					, help="Queries a page and returns all linked urls related to word")
	parser.add_argument("-p"			, "--probe"					, help="Probing the net for the word provided")
	parser.add_argument("-i"			, "--info"					, help="Prints out information about the data")
	parser.add_argument("-clone"			, "--clone"					, help="Clones the current word table to _<word> table.")
	parser.add_argument("-store"			, "--store"					, help="Stores the word in the words database.")
	parser.add_argument("-file"			, "--fileName"					, help="Stores the word in the words database.")
	parser.add_argument("-r"			 			,action="store_true"	, help="Starts recursive probing using the words table of the dataset.")
	parser.add_argument("-gui"			 			,action="store_true"	, help="Starts the gui of this program.")
	parser.add_argument("-delDB"			 			,action="store_true"	, help="Resets the db, CANNOT BE UNDONE !")
	args=parser.parse_args()
	debugprint("Argument Parser ready")
	debugprint("Leaving")

	return args


def parseAction(parse_args):
	if parse_args.debug_level:
		gboDebugLevel=parse_args.debug_level
		setDebugLevel(gboDebugLevel)
		debugprint("Setting debug level to: " + str(gboDebugLevel))
	if parse_args.probe:
		print("Probe: " + parse_args.probe)

		#we should try to get all the urls in the page
		#instead of the content of the searchPage

		#getAllUrlsInHTML(strUrl)

		#Build the list of words
		_strListWords=""
		for strUrl in strUrls:
			debugprint("")
			_strUrl=strUrl+parse_args.probe
			_istrListWords=queryURL(_strUrl)

			if _strListWords=="":
				_strListWords=_istrListWords
			else:
				_strListWords=  _strListWords + _istrListWords

		#now we got a list, lets clean it up
		debugprint("Word List Array Item Count: " + str(len(_strListWords)))
		_strListWords=returnArrayUnique(_strListWords)
		debugprint("Word List Array Item Count: " + str(len(_strListWords)))

		#debugTrace(inspect)
		#debugprintlist(_strListWords)
		debugprint("Probing Table")
		CreateTable(parse_args.probe)
		debugprint("Continueing after table creation")
		#We loop through the words and store then in the db
		for _word in _strListWords:
			print("Storing " + _word)
			storeWord(_word,parse_args.probe)
	if parse_args.clone:
		BackUpTable(parse_args.clone)
	if parse_args.info:
		printInfo(parse_args.info)
	if parse_args.r:
		recursiveProbing()
	if parse_args.gui:
		print("Not implemented yet")
	if parse_args.delDB:
		dropAllTablesExcept("word")
	if parse_args.listCount:
		listCount(parse_args.listCount)
	if parse_args.store:
		storeWord(parse_args.store, "word")
	if parse_args.qpage:
		print("Entering qpage with: " + str(parse_args.qpage))
		queryPageContent(parse_args.qpage)
	if parse_args.qgurlret:
		for link in queryGoogleRetLinks(parse_args.qgurlret):
			strLink=link['formattedUrl']
			if ".html" in strLink:
				print(strLink)
	if parse_args.fileName:
		print("Reading file for import to words database: " + str(parse_args.fileName))
		list=ReadFileRetWords(parse_args.fileName)
		print(list)


