def returnArrayUnique(strCheck1, strCheck2):
	try:
		strArr=""
		print("Entering uniqify")
		print("Page 1: \n" + strCheck1)
		print("Page 2: \n" + strCheck2)

		for word in strCheck1:
			print("Checking " + word)
			if word in strCheck2:
				if len(strArr) == 0:
					strArr = word
				else:
					strArr = word + "," + strArr

		print("Returning from uniqifying")
		return strArr

	except Exception:
		print(Exception)
		raise



