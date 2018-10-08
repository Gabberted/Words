from debugFnct import *


def replaceWordsFromArrayWithStringInString(strString, strArray, strReplaceWith):
	try:
		for word in strArray:
			strString=strString.replace(word,strReplaceWith)

		return strString
	except Exception:
		raise

def removeEmptyItemsFromArray(strArray):
	strString=""
	try:
		for word in strArray:
			if len(word.strip())!=0:
				if len(strString.strip())==0:
					strString=word
				else:
					strString=strString + "," + word

		return strString.split(",")
	except Exception:
		raise

def addOneToString(strNumber):
	debugprint("Adding 1 to: " + str(strNumber))
	iNumber=0
	if strNumber != "":
		iNumber = float(strNumber)
		iNumber = int(iNumber)
		iNumber = iNumber + 1
		debugprint(str(iNumber))
		return iNumber
