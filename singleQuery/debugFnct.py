import inspect

#from debugFnct import *

#strings
gDebugLevel=1
iLevel=0
iLine=0
from vars import *

def setDebugLevel(iDBLevel):
    global gDebugLevel

    debugprint("Entering")
    debugprint("Level old: " + str(gDebugLevel))
    gDebugLevel=iDBLevel
    debugprint("Level new: " + str(gDebugLevel))
    debugprint("Leaving")

def debugprint(strMessage):
	global iLevel
	global iLine

	boDebugPrint=False

	if strMessage=="Entering":
		iLevel=int(iLevel)+1
		boDebugPrint=True
	if strMessage=="Leaving":
		boDebugPrint=True

	strTab=":"
	#strPref=str(iLine) + "debug(" + str(iLevel) + ")"
	if int(gDebugLevel)>1:
		if iLevel>3:
			iLevel=3
		for i in range(int(iLevel)):
			strTab=strTab + "\t"
		if int(gDebugLevel)>3:
			strTab=str(inspect.stack()[2][4]) + ":"
		if boDebugPrint == True:
			print(str(iLine)+ " debug (" + str(iLevel) + ") : " + strTab + inspect.stack()[1][3] + " -> "  + strMessage)
			iLine=iLine+1
		else:
			if "Error" in strMessage:
				print(str(iLine) + " ERROR (" + str(iLevel) + ") : " + strTab + inspect.stack()[1][3] + " -> "  + strMessage)
				iLine=iLine+1
			else:
				print(str(iLine) + " Message (" + str(iLevel) + ")" + "'" +  str(inspect.stack()[1][1]) + ": " + strTab + inspect.stack()[1][3] + " -> "  + strMessage)
				iLine=iLine+1

	if strMessage=="Leaving":  iLevel=int(iLevel)-1

def debugprintlist(strList):
	global iLevel
	global iLine

	strTab=""
	for i in range(int(iLevel)):
		strTab=strTab + "\t"
	for word in strList:
		#print(str(iLine) + " LIST: (" + str(iLevel) + ") : " + strTab + str(inspect.stack()[0][5]) + "." + inspect.stack()[1][3] + " -> "  + word)
		#print(str(iLine) + " LIST: (" + str(iLevel) + ") : " + inspect.stack()[1][3] + " -> "  + word)
		print(str(iLine) + " LIST: (" + str(iLevel) + "):" + str(word))
		#print("d")
		iLine=iLine+1

def debugTrace(inspect):
	for str1 in inspect[1]:
		#for str2 in str1:
		print(str(str2))
