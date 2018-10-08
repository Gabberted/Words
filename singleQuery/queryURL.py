import urllib.request
import pymysql
import json
import time

from googleapiclient.discovery import build
from debugFnct import *
from stringFnct import *
from vars import *


def queryURL(strUrl):
	debugprint("Entering")
        #first we query the url
	debugprint("Requesting url: " + strUrl)
	response=urllib.request.urlopen(strUrl).read()
	str_page=response

	#then we get the empty page so we can substract all the html tagging
	#debugprint("reading response")
	#response=urllib.request.urlopen(strSUrl).read()
	#str_page_standard=response

	#clean up
	debugprint("cleaning up the data set")
	str_ListWords=replaceWordsFromArrayWithStringInString(str(str_page),strHTMLTags," ").split(" ")
	str_ListWords=removeEmptyItemsFromArray(str_ListWords)
	#str_ListWords=returnArrayUnique(str_ListWords)
	#debugprint("Removing empty entries")

	#debugprintlist(str_ListWords)
	debugprint("Leaving")
	return str_ListWords

def queryPageContent(strWord):
	debugprint("Entering")
	iCnt=0
	strAllPages=[]
	strUrlContent=queryGoogleRetLinks(strWord)
	debugprint("Number of urls found:" + str(len(strUrlContent)))
	for strLink in strUrlContent[0]:
		strUrl2=strLink
		debugprint("url:" + strUrl2)
		response=urllib.request.urlopen(strUrl2).read()
		str_page=response
		time.sleep(2)
		strAllPages[iCnt]=str_page
		debugprint(str(str_page[iCnt]))
		iCnt+=1

	debugprint("Leaving")
	return str_AllPages


def queryPageContentRetWords(strWord):
	debugprint("Entering")
	iCnt=0
	strAllPages=[]
	#strUrlContent=queryGoogleRetLinks(strWord)
	strUrlContent=getAllUrlsInHTML(strWord)
	debugprint("LIST Looping through links")
	debugprintlist(strUrlContent)
	for strLink in strUrlContent[0]:
		strUrl2=strLink
		debugprint("LIST url:" + strUrl2[0])
		response=urllib.request.urlopen(strUrl2).read()
		str_page=response
		debugprint("LIST Page fetched")
		time.sleep(2)
		debugprint("LIST wake up!")
		str_ListWords=replaceWordsFromArrayWithStringInString(str(str_page),strHTMLTags," ").split(" ")
		str_ListWords=removeEmptyItemsFromArray(str_ListWords)
		strAllPages.append(str_ListWords)
		#strAllPages.append(str_page)
		#debugprint(str(str_page[iCnt]))
		debugprint("Loop")
		iCnt+=1

	debugprint("Leaving")
	return str_AllPages


def getAllUrlsInHTML(strUrl):
	debugprint("Entering")
	strPage=queryGoogleRetLinks(strUrl)
	print("getAllUrlsInHTML: " + str(strPage)[1])

	debugprint("Leaving")
	return strPage

def queryGoogleRetLinks(strWord):
	debugprint("Entering")
	my_api_key="AIzaSyCwT1XDUNE3euUFJqJt1Fa0hvk34h-MadY"
	my_cse_id="017576662512468239146:omuauf_lfve"
	service = build("customsearch", "v1", developerKey=my_api_key) 
	res = service.cse().list(q=strWord, cx=my_cse_id).execute()

	debugprint("Leaving")
	return res['items']



