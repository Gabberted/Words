def returnArrayUnique(strCheck1):
	try:
		strArr=""
		print("Entering uniqify")
		#print("Page 1: \n" + strCheck1)
		#print("Page 2: \n" + strCheck2)
		
		strRetArr=""
		for word in strCheck1:
			print("Checking " + word)
			if word in strRetArr:
				if len(strRetArr) == 0:
					strRetArr = word
				else:
					strRetArr = word + " | " + strRetArr
		print("Returning from uniqifying")
		return strRetArr.split(",")

	except Exception:
		print(Exception)
		raise



