import pymysql

from debugFnct import *
from stringFnct import *
from queryURL import *

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


def ExecuteQuery(strQuery):
        debugprint("Entering")
        try:
                strResult=""
                debugprint("query:" + strQuery)
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
                debugprint("Return:     " + str(strResult))
                debugprint("Leaving")
                return str(strResult)

        except Exception:
                print("strQuery:        " + strQuery)
                raise
                return strResult
                debugprint("Leaving")


def boWordKnown(strWord):
	debugprint("Entering")
	strRet=True
	try:
		#strQ="Select * from " + strTable + " where word='" + strWord + "'"
		strQ="Select count(*) from word where word='" + strWord + "'"
		debugprint("QUERY: " + strQ)
		strRet=ExecuteQuery(strQ)
		debugprint("StrQ:" + strQ)
		debugprint("strRet StrQ: " + strRet)
		if strRet=="":
			strRet=False
		if strRet=="0":
			strRet=False
		print("Known number of word (" + strWord + "):" + strRet)
	except:
		print("Word not found")

	debugprint("Leaving")
	return strRet


def getNextINDX(strTable):
	debugprint("Entering")
	strRet=0
	try:
		strQ="Select max(indx) from " + strTable
		strRet=ExecuteQuery(strQ)
		debugprint("Max indx: " + str(strRet))
		if str(strRet)=="None":
			strRet=0
			debugprint("No Max found")
		if str(strRet)=="":
			strRet=0
			debugprint("No Max found")
		else:
			strRet=addOneToString(strRet)
	except:
		raise

	debugprint("Leaving")
	return strRet

def getValue(word,strTable,strColumn):
	debugprint("Entering")
	strIndx=""
	try:
		if str(strTable)!="":
			strQ="Select " + str(strColumn) + " from words." + str(strTable) + " where word='" + str(word) + "'"
			debugprint("QUERY: " + strQ)
			debugprint("word: " + str(word))
			strIndx=ExecuteQuery(strQ)
			debugprint("Leaving")
	except:
		debugprint("ERROR")
		raise

	debugprint("Leaving")
	return strIndx



def getIndx(word,strTable):
	try:
		strReturn= getValue(word,strTable,"indx")
		debugprint("getIndx.strReturn: " + str(strReturn))
		if strReturn=="": strReturn="0"

		return strReturn
	except:
		debugprint("Error")
		raise

def getCount(word,strTable):
	try:
		debugprint("Entering")
		debugprint("Leaving")
	except:
		debugprint("Error")
		raise

	return getValue(word,strTable,"count")


def getConn(word,strTable):
	try:
	        return getValue(word,strTable,"connect")
	except:
		debugprint("Error")
		raise

def boTableExcists(strTableName):
	boRet=True
	try:
		debugprint("Entering")
		#print("Entering boTableExcists")
		strQ="SELECT * FROM information_schema.TABLES WHERE (TABLE_SCHEMA = 'words') AND (TABLE_NAME = '" + strTableName + "')"
		print(strQ)
		iTables=ExecuteQuery(strQ)
		print("Num tables: " + iTables)
		if iTables.strip()=="":
			boRet = False
			debugprint("boTableExcists: Table not found")
		else:
			debugprint("boTableExcists: Table found !")
		debugprint("Leaving")
	except:
		debugprint("Error")
		raise

	return boRet

def CreateTable(strTableName):
	debugprint("Entering")
	strRet=str(boTableExcists(strTableName))
	debugprint("VARS: " + strRet)
	try:
		if strRet=="False":
			strQ="CREATE TABLE " + strTableName +  " LIKE words.word;"
			debugprint("Creating table")
			ExecuteQuery(strQ)
			debugprint("Table created")
			debugprint("Leaving")
			#print("Table created:   " + strTableName)
		else:
			debugprint("Table excists")
		debugprint("Leaving")
	except:
		raise
		debugprint("Error")
		debugprint("Leaving")
		return

def BackUpTable(strTableName):
	debugprint("Entering")
	strRet=str(boTableExcists("_"+strTableName))
	debugprint("Cloning: " + strRet)
	try:
		if strRet=="False":
			strQ="CREATE TABLE _" + strTableName +  " LIKE words.word;"
			debugprint("Creating table")
			ExecuteQuery(strQ)
			debugprint("Table created")
			debugprint("Restoring data")
			strQ="INSERT  _" + strTableName +  " select * from words.word;"
			ExecuteQuery(strQ)
			debugprint("Data restored")
			debugprint("Leaving")
			#print("Table created:   " + strTableName)
		else:
			debugprint("Table excists")
		debugprint("Leaving")
	except:
		raise
		debugprint("Error")
		debugprint("Leaving")
		return



def printInfo(iLevel):
	try:
		strQ="Select max(count) from word"
		strCnt=ExecuteQuery(strQ)
		strQ="Select indx from word where count='" + strCnt + "'"
		strIndx=ExecuteQuery(strQ)
		strQ="select count(*) from word"
		strTot=ExecuteQuery(strQ)
		strQ="select distinct count(*) from word"
		strTotD=ExecuteQuery(strQ)

		infoList=[]
		print("Highest wordcount: 	" + strCnt)
		print("Highest Indx:		" + strIndx)
		print("Total words:		" + strTot)
		print("Words Distinct:		" + strTotD)

		infoList.append(strCnt)
		infoList.append(strIndx)
		infoList.append(strTot)
		infoList.append(strTotD)


		strQ="Select distinct count from word order by count"
		cur=ReturnCursor(strQ)
		lstWordCount=[]
		iCount=0
		for count in cur:
			strCount=count[0]
			strQ="Select count(*) from word where count='" + str(strCount) + "' limit 10"
			strCntCount=ExecuteQuery(strQ)
			print("Count:	" +  str(strCount) + "=" + str(strCntCount))
			lstWordCount.append(str(strCntCount))
			iCount+=1

		infoList.append(str(iCount))
		infoList.append(lstWordCount)
		for iCounter in range(iCount,10):
			infoList.append("0")
		if int(iLevel) > 1:
			print("===================================")
			print("=             TOP words           =")
			print("===================================")
			for cnt in lstWordCount:
				print("Letters: " + str(cnt))
				print("-----------------------------------")
				strQ="Select word from word where count='" + str(cnt) + "' order by word limit 5"
				cur=ReturnCursor(strQ)
				for _word in cur:
					print(_word[0])
		return infoList
	except:
		raise
		debugprint("Error")



def dropAllTablesExcept(strSaveTable):
	try:
		debugprint("Entering")
		strResult=""
		strQ="show tables"
		cur=ReturnCursor(strQ)
		for row in cur:
			debugprint("Dropping Table: " + row[0])
			if str(row[0])!=strSaveTable:
				if "_" not in str(row[0]):
					strQ="Drop table " + str(row[0])
					ExecuteQuery(strQ)
		cur.close()
		debugprint("Closing cursor")

		#now we need to clean out word
		strQ="delete from word"
		ExecuteQuery(strQ)
		debugprint("Leaving")
	except:
		raise
		debugprint("Error")


def recursiveProbing():
	try:
		strQ="Select word from word"
		cur=ReturnCursor(strQ)
		for _word in cur:
			debugprint("Storing word: " + _word[0])
			#fetch urls connected to this word
			#strLinks=queryPageContentRetWords(_word[0])
			strLinks=getAllUrlsInHTML(_word[0])
			debugprint("recursiveProbing")
			#debugprintlist(str(strLinks))
			for strLink in strLinks:
				strWord=strLink
				debugprint("VAR: " + strWord)
				debugprint("Storing subword: " + strWord)
				#storeWord(strWord,"word")
			debugprint("==================================================================")
	except:
		raise
		debugprint("Error")

def addNewWord(iNextIndx,_word,strConn):
	debugprint("Entering")
	try:
		debugprint("Adding new word to the db: " + str(_word))
		strQ="insert into words.word(indx,word,connect,count)values('" + str(iNextIndx) + "','" + _word + "','" + strConn + "','1')"
		ExecuteQuery(strQ)
		debugprint("strQ: " + strQ)
		debugprint("Leaving")
	except:
		raise
		debugprint("Error")

def updateWord(strConn,_word,iCount,strIndx):
	try:
		print("Word known, we need to update: " + str(_word))
		strQ="update words.word set connect='" + strConn + "," + _word + "',count='" + str(iCount) + "' where indx='" + str(strIndx) + "'"
		ExecuteQuery(strQ)
		debugprint("strQ: " + strQ)
	except:
		raise
		debugprint("Leaving")

def storeWord(_word, strSead):
	try:
		debugprint("Entering")
		debugprint("Storing " + str(_word))
		iNextIndx=getNextINDX("word")
		strIndx2=getIndx(str(_word),"word")
		debugprint("iNextIndx:" + str(iNextIndx))
		iCount=getCount(_word,"word")
		debugprint("iCount:" + str(iCount))
		if boWordKnown(_word)==False:
			debugprint("storeWord.boWordKnown Trigger addNewWord")
			addNewWord(iNextIndx,str(_word),strSead)
		else:
			debugprint("storeWord.boWordKnown=True")

			debugprint("storeWord.strIndx: " + str(strIndx2))
			strConn=getConn(str(_word),"word")
			iCount=addOneToString(iCount)
			debugprint("storeWord.boWordKnown Trigger updateWord")
			updateWord(strConn,_word,iCount,strIndx2)
		listInfo=printInfo
		print("LIST INFO:" + str(listInfo(0)))
		strEmpty=""
		strTopList=listInfo(0)[5]
		print("HighCount: " + str(strTopList))

		#we need to fill all the empty entried to "0"
		iLenghtList=len(strTopList)
		print("List lenght: " + str(iLenghtList))

		iLenght=len(strTopList)
		print("List iLenght: " + str(iLenght))
		for iCnt in range(iLenght,10):
			print("Nullifying")
			strTopList.append("0")

		#we store some information in seperate columns
		#strQ="insert into _topList(indx,highwcnt,highestindx,totwcnt, top1,top2, top3,top4,top5,top6,top7,top8,top9,top10) values('" \
		strQ="insert into _topList(indx,highwcnt,highestindx,totwcnt,top1,top2,top3,top4,top5,top6,top7,top8,top9,top10) values('" \
		+ str(strIndx2) + "','" + str(listInfo(0)[1]) + "','" +  str(listInfo(0)[2]) + "','" + str(listInfo(0)[3]) + "','" + str(strTopList[iLenght-0]) + "','" \
		+ str(strTopList[iLenght-1]) + "','" + str(strTopList[iLenght-2]) + "','" + str(strTopList[iLenght-3]) + "','" + str(strTopList[iLenght-4]) + "','" + str(strTopList[iLenght-5]) + "','" + str(strTopList[iLenght-6]) \
		+ "','" + str(strTopList[iLenght-7]) + "','" + str(strTopList[iLenght-8])  + "','" + str(strTopList[iLenght-9]) + "')"
		#+ str(strTopList[int(len(strTopList))-8]) +  "','" + str(strTopList[int(len(strTopList))-9]) + "')"

		print(strQ)
		ExecuteQuery(strQ)
	except:
		raise
		debugprint("Error")

	debugprint("Leaving")

def listCount(iCnt):
	strQ="select word from word where count='" + str(iCnt) + "'"
	cur = ReturnCursor(strQ)
	iCount=0
	for word in cur:
		print("Item (" + str(iCount) + ") :" + str(word[0]))
		iCount+=1
