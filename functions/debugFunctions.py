from time import *

#vars
dblSleepTime=0.01

def printDebug(strMessage, gDebugLevel):
	sleep(dblSleepTime)
	if gDebugLevel>0:
		print(strMessage)

def printUrlDebug(strMessage):
	sleep(dblSleepTime)
	if gDebugLevel>0:
		print(strMessage)
