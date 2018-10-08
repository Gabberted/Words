import pymysql
import inspect

#strings
gDebugLevel=1
iLevel=0

def setDebugLevel(iDBLevel):
	global gDebugLevel

	debugprint("Entering")
	printDebugLevel()
	gDebugLevel=iDBLevel
	printDebugLevel()
	debugprint("Leaving")

def printDebugLevel():
	global gDebugLevel
	print(str(gDebugLevel))

def debugprint(strMessage):
	global iLevel
	boDebugPrint=False

	if strMessage=="Entering": 
		iLevel=int(iLevel)+1
		boDebugPrint=True
	if strMessage=="Leaving":
		boDebugPrint=True

	strTab=""
	if int(gDebugLevel)>1:
		for i in range(int(iLevel)):
			strTab=strTab + "\t"
		if boDebugPrint == True:
			print("debug (" + str(iLevel) + ") : " + strTab + inspect.stack()[1][3] + " -> "  + strMessage)
		else:
			print("Message (" + str(iLevel) + ") : " + strTab + inspect.stack()[1][3] + " -> "  + strMessage)

	if strMessage=="Leaving":  iLevel=int(iLevel)-1

def Connect():
	try:
		debugprint("Entering")
		connection=pymysql.connect(host='localhost',user='rakaut',password='ijQ84mTO',db='words')
		debugprint("Leaving")
		return connection
	except:
		print("Connection failed!")
		raise
		debugprint("Leaving")
		return null


def printQuery(strQuery):
	debugprint("Entering")
	try:
		strResult=""
		debugprint("Q:" + strQuery)
		_connect=Connect()
		cur=_connect.cursor()
		cur.execute(strQuery)
		debugprint("Query executed")
		for row in cur:
		        #if strResult != "":
			strResult=row[0]
			for cell in strResult:
				debugprint("DB_ROW: " + str(cell))
		_connect.commit()
		cur.close()
		_connect.close()
		debugprint("Return:	" + str(strResult))
		debugprint("Leaving")
		return str(strResult)

	except:
		print("Error executing query:")
		print(strQuery)
		raise
		debugprint("Leaving")


def ExecuteQuery(strQuery):
	debugprint("Entering")
	try:
		strResult=""
		debugprint("Q:" + strQuery)
		_connect=Connect()
		cur=_connect.cursor()
		cur.execute(strQuery)
		debugprint("Query executed")
		for row in cur:
		        #if strResult != "":
			strResult=row[0]
			debugprint("DB_ROW: " + str(strResult))
		_connect.commit()
		cur.close()
		_connect.close()
		debugprint("Return:	" + str(strResult))
		debugprint("Leaving")
		return str(strResult)

	except Exception:
		print("strQuery:	" + strQuery)
		raise
		return strResult
		debugprint("Leaving")

def ExecuteSingleQuery(strQuery):
	debugprint("Entering")
	try:
		strResult=""
		#print("Q:" + strQuery)
		_connect=Connect()
		cur=_connect.cursor()
		cur.execute(strQuery)
		strResult1=cur.fetchall()
		strResult=strResult1
		cur.close()
		_connect.close()
		#print("Return:	" + str(strResult))
		debugprint("Leaving")
		return str(strResult)

	except Exception:
		print("strQuery:	" + strQuery)
		raise
		return strResult
		debugprint("Leaving")

def boTableExcists(strTableName):
	debugprint("Entering")
	#print("Entering boTableExcists")
	boRet=True
	strQ="SELECT * FROM information_schema.TABLES WHERE (TABLE_SCHEMA = 'words') AND (TABLE_NAME = '" + strTableName + "')"
	print(strQ)
	iTables=ExecuteQuery(strQ)
	print("Num tables: " + iTables)
	if iTables=="":
		boRet = False
	debugprint("Leaving")
	return boRet

def CreateTable(strTableName):
	debugprint("Entering")
	try:
		strQ="CREATE TABLE [" + strTableName +  "] LIKE words.word;"
		#print(strQ)
		ExecuteQuery(strQ)
		debugprint("Leaving")
		#print("Table created:   " + strTableName)
	except:
		#raise
		return
		debugprint("Leaving")

def ReturnCursor(strQ):
	debugprint("Entering")
	try:
		_connect=Connect()
		cur=_connect.cursor()
		cur.execute(strQ)
		strCur=cur
		cur.close()
		_connect.close()
		debugprint("Leaving")
		return strCur

	except Exception:
		raise
		return strResult
		debugprint("Leaving")

def dropAllTablesExcept(strSaveTable):
	debugprint("Entering")
	strResult=""
	strQ="show tables"
	cur=ReturnCursor(strQ)
	for row in cur:
		if row!=strSaveTable:
			strQ="Drop table " + str(row[0])
			ExecuteQuery(strQ)
	cur.close()
	debugprint("Leaving")

def boWordKnown(strWord,strTable):
	debugprint("Entering")
	strRet=""
	try:
		#strQ="Select * from " + strTable + " where word='" + strWord + "'"
		strQ="Select count(*) from word where word='" + strWord + "'"
		print(strQ)
		strRet=ExecuteQuery(strQ)
		print("Known number of word:" + strRet)
	except:
		print("Word not found")

	debugprint("Leaving")
	return strRet

def getNextINDX():
	debugprint("Entering")
	strRet=0
	try:
		strQ="Select max(indx) from word"
		strRet=ExecuteQuery(strQ)
		print("Max indx: " + str(strRet))
		if strRet==None:
			strRet=0
			print("No Max found")
		else:
			strRet=addOneToString(strRet)
	except:
		raise

	debugprint("Leaving")
	return strRet

def addNewWordToWord(strWord,word):
	debugprint("Entering")
	debugprint("Adding new word: " + str(strWord))
	iNextIndx=getNextINDX()
	#debugprint("iNextIndx: " + str(iNextIndx))
	debugprint("next index: " + str(iNextIndx))
	#strQ="insert into words." + word + "(indx,word,connect,count)values('" + str(iNextIndx) + "','" + word + "','" + strWord + "','1')"
	strQ="insert into words.word(indx,word,connect,count)values('" + str(iNextIndx) + "','" + word + "','" + strWord + "','1')"
	debugprint("A:" + strQ)
	ExecuteQuery(strQ)
	debugprint("Leaving")
	#strQ="insert into words.word(indx,word,connect,count)values('" + str(iNextIndx) + "','" + strWord + "','Genesis','1')"
	#print("B:" + strQ)
	#ExecuteQuery(strQ)

	#print(strQ)


def getIndx(word,strTable):
	debugprint("Entering")
	#print("getIndx_word:" + word)
	#print("getIndx_strTable:" + str(strTable))
	strIndx="None"

	if str(strTable)!="None":
		strQ="Select indx from words." + strTable + " where word='" + word + "'"
		strIndx=ExecuteQuery(strQ)
		#print("INDX: "	+ strIndx)
	return strIndx
	debugprint("Leaving")

def getCount(word,strTable):
	debugprint("Entering")
	strIndx="None"
	if str(strTable)!="None":
		strQ="Select count from words." + strTable + " where word='" + word + "'"
		#print("getCount Quer: " + strQ)
		strIndx=ExecuteQuery(strQ)
	return strIndx
	debugprint("Leaving")

def getConn(word,strTable):
	debugprint("Entering")
	strIndx="None"

	if str(strTable)!="None":
		strQ="Select connect from words." + strTable + " where word='" + word + "'"
		strIndx=ExecuteQuery(strQ)
	debugprint("Leaving")
	return strIndx

def addKnownWordToWord(strWord,strSearch):
	debugprint("Entering")
	print("Word:" + strWord)
	print("Search:" + str(strSearch))

	strIndx=getIndx(strWord,"word")
	print("StrIndx:	" + strIndx)
	strConn=getConn(strWord,"word")
	print("Compare: " + strSearch + " in " + strConn)

	if str(strSearch) not in str(strConn):
		strConn=getConn(strWord,"word") + "," + str(strSearch)
		print("Word not found:	" + strSearch + " in " + strConn)


	print("StrConn:	" + strConn)
	strCount=getCount(strWord,"word")
	strCount=addOneToString(strCount)
	print("Count:	" + str(strCount))
	#print(iNextIndx)
	strQ="update words.word set connect='" + strConn + "',count='" + str(strCount) + "' where indx='" + strIndx + "'"
	print("1:" + strQ)
	ExecuteQuery(strQ)
	debugprint("Leaving")
	#if str(strSearch)!="None":
	#	try:
	#		strQ2="update words." + str(strSearch) + " set connect='" + strConn + "',count='" + str(strCount) + "' where indx='" + strIndx + "'"
	#		#print("2:" + strQ2)
	#		ExecuteQuery(strQ2)
	#	except Exception:
	#		print("Couldn't update ")

	#print(strQ)


def printQuery(strQ):
	debugprint("Entering")
	cur=ReturnCursor(strQ)
	for row in cur:
		strRow =""
		for cell in row:
			if len(strRow)==0:
				strRow = str(cell)
			else:
				strRow = strRow + "	" + str(cell)
		print(strRow)
	debugprint("Leaving")

def addOneToString(strNumber):
	debugprint("Entering")
	#print("strNumber: " + str(strNumber))
	iNumber=0
	if str(strNumber)!="None":
		if str(strNumber)!="":
			iNumber = float(strNumber)
			iNumber = int(iNumber)
			iNumber = iNumber + 1
			#printDebug(str(iNumber))
	debugprint("Leaving")
	return iNumber



