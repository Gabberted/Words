from stringArrayFunctions import *

#def printError(ex):
        #printDebug("ERROR")
#	print("Err: " + str(ex) )
        #raise

def Connect():
	#print("Connecting to database")
	try:
		connection=pymysql.connect(host='localhost',user='rakaut',password='ijQ84mTO',db='words')
		#print("Connection succesfull ! :) ")

		return connection
	except Ex:
		print("Connection failed!")
		raise
		return null

def ExecuteQuery(strQuery):
	try:
		strResult=""
		_connect=Connect()
		cur=_connect.cursor()
		cur.execute(strQuery)
		wait(0.05)
		#print(cur.description)
		#print(strQuery)
		for row in cur:
			if strResult=="":
				strResult=row[0]
				#print("ExecuteQuery Results found: " + str(strResult))
			#else:
				#print("ExecyteQuery Result ignored:" + str(row[0]))

		cur.close()
		_connect.close()
		#print(strResult)
		return str(strResult)

	except Exception:
		raise
		return strResult

def allWords():
	print("Fetching all words")
	sql="SELECT * from word"
	ExecuteQuery(sql)

def getLastWordINDX():
	#print("INDX PROBED !")
	strQuery="Select max(indx) from word"

	try:
		#_connect=Connect()
		#cur=_connect.cursor()
		#cur.execute(strQuery)
		##print(cur.description)
		#for row in cur:
		#	strResult=str(row[0])
		#cur.close()
		#_connect.close()
		strResult=ExecuteQuery(strQuery)

	except Exception:
		return 0

	#print("INDX RET: " + str(strResult))
	return strResult

def getNextWordINDX():
	iID=0
	try:
		iID=int(getLastWordINDX())+1
	except Exception:
		print(str(iID))
	return iID


def QueryReturnRows(strQuery):
	try:
		#print("		QueryReturnRows(strQuery)")
		strValue=""
		#iID=int(getLastWordINDX())+1
		#print("Q: " + strQuery)
		_connect=Connect()
		cur=_connect.cursor()
		cur.execute(strQuery)
		cur.fetchall()
		strValue=str(cur.rowcount)
		_connect.close()
		#print(strValue)
		return strValue

	except Exception:
		print("DB ERROR")
		raise





def QueryGetValue(strQuery):
	try:
		strValue=""
		iID=int(getLastWordINDX())+1
		#print("Q: " + strQuery)
		_connect=Connect()
		cur=_connect.cursor()
		cur.execute(strQuery)
		for row in cur:
			strValue=str(row[0])
		_connect.close()

		return strValue

	except Exception:
		print("DB ERROR")
		raise

def QueryGetALLValue(strQuery):
	try:
		strValue=""
		#iID=int(getLastWordINDX())+1
		#print("Q: " + strQuery)
		_connect=Connect()
		cur=_connect.cursor()
		cur.execute(strQuery)

		iCnt=0
		for row in cur:
			#print(str(row))
			if iCnt==0:
				strValue=str(row[0])
			else:
				strValue=strValue + "," + str(row[0])
		_connect.close()

		#print(strValue)
		return strValue.split(",")

	except Exception:
		print("DB ERROR")
		raise

def createWordTable(strTableName):
	strQ=""
	try:
		#first we need to check if the table is already created
		#print("Checking if Table=true")
		strQ="SELECT COUNT('" + strTableName + "') FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='words' AND TABLE_NAME LIKE '" + strTableName + "'"
		strRet= ExecuteQuery(strQ)
		#print("Table count executed")
		#print("Table count: " +  strRet)
		#print("Table already exsists, skipping!")
		#strQ="CREATE TABLE `words`.`" + strTableName + "` ( `indx` INT NOT NULL , `count` INT NULL , `connect` VARCHAR NULL , `word` VARCHAR NOT NULL , UNIQUE `indx_" + strTableName + "` (`indx`(256))) ENGINE = InnoDB;"
		if strRet.strip() == "0":
			strQ="CREATE TABLE " + strTableName +  " LIKE word;"
			#print(strQ)
			ExecuteQuery(strQ)
			print("Table created:	" + strTableName)

	except Exception:
		print("Error in : " + strQ)
		#raise

def getNextWordCount(strWord):
	#print("getNextWordCount PROBED !")
	strQuery="Select count from word where `word` = '" + strWord + "'"
	strResult=ExecuteQuery(strQuery)

	#print("Count RET: " + str(strResult))
	return strResult


def insertWord(strWord):
	#print("		insertWord")
	try:
		indX=getNextWordINDX()
		#strCount=getLastNextCount(strWord)
		strQuery="INSERT INTO `word`(`indx`,`word`,`count`,`connect`)values('" + str(indX) + "','" + strWord + "','1','Genesis')"
		#print("Q " + str(indX) + ": " + strQuery)
		_connect=Connect()
		#print("Connected")
		cur=_connect.cursor()
		#print("Executing Query")
		cur.execute(strQuery)
		_connect.commit()
		_connect.close()
		#print("Connection closed")

		return indX

	except Exception:
		print("DB ERROR")
		raise

def getCount(strWord):
	#print("getCount PROBED !")
	strQuery="Select count from word where `word` = '" + strWord + "'"
	strResult=ExecuteQuery(strQuery)

	#print("Result before  addition: " + str(strResult))
	strResult=addOneToString(strResult)
	#print("Result after   addition: " + str(strResult))

	#print("getcount: " + str(strResult))
	return strResult

def getConnect(strWord):
	#print("getConnect PROBED !")
	strQuery="Select connect from word where `word` = '" + strWord + "'"
	strResult=ExecuteQuery(strQuery)

	#print("getConnect RET: " + str(strResult))
	return strResult

def getWordINDX(strWord):
	printHeader("getWordINDX")
	iID=0
	try:
		strQuery="Select `indx` from `word` where `word`='" + strWord + "'"
		#print(strQuery)
		#iId=ExecuteQuery(strQuery)
		#iId=float(iID)
		#iID=int(iID)+1

		_connect=Connect()
		cur=_connect.cursor()
		cur.execute(strQuery)
		wait(0.05)
		strResult=""
		#print(cur.description)
		#print(strQuery)
		for row in cur:
			if strResult=="":
				strResult=row[0]
				#print("ExecuteQuery Results found: " + str(strResult))
			#else:
				#print("ExecyteQuery Result ignored:" + str(row[0]))

		cur.close()
		_connect.close()

	except Exception:
		print(strResult)

	return strResult



def updateWord(strWord):
	printDebug("		insertWord")
	try:
		indX=getWordINDX(strWord)
		#print("indX: " + str(indX))
		strCount=getCount(strWord)
		try:
			strCount=addOneToString(strCount)
			#print(strCount)

			#get the already connected words and
			#add if this word is not already part of it
			strConnect=getConnect(strWord) 
			if strWord not in strConnect:
				strConnect = strConnect + ", " + strWord
			#print("		inside insertWord")
			#if the word is the same as Genesis (the first sead of word planted) then we need to skip it

			if strWord.strip()!="Genesis":
				strQuery="update word set `count`='" + str(strCount) + "', `connect`='" + strConnect + "' where indx='" + str(indX) + "'"
				#print(strQuery)
				try:
					_connect=Connect()
					#print("Connected")
					cur=_connect.cursor()
					#print("Executing Query")
					cur.execute(strQuery)
					_connect.commit()
					_connect.close()
					#print("Connection closed")

				except Exception:
					print("DB ERROR")
					raise

		except Exception:
			#e=sys.exc_info()[0]
                        #e2 = sys.exc_info()[1]
                        #print(str(e))
                        #print("<p>Error: %s</p>" % e2 )
                        raise

	except Exception:
		print("DB ERROR")
		raise

	return indX
