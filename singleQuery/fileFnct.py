def ReadFile(strFileName):
	file = open(strFileName,'r')
	strFile=file.read()
	file.close()

	return strFile

def ReadFileRetWords(strFileName):
	strWordList=ReadFile(strFileName)
	return strWordList
