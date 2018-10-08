from googleapiclient.discovery import build
from vars import *
import pprint

my_api_key = "AIzaSyCwT1XDUNE3euUFJqJt1Fa0hvk34h-MadY"
my_cse_id = "017576662512468239146:omuauf_lfve"

def google_search(search_term, api_key, cse_id, **kwargs):
	service = build("customsearch", "v1", developerKey=api_key)
	res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
	return res['items']

results = google_search('cat', my_api_key, my_cse_id)
for result in results:
	pprint.pprint(result['htmlFormattedUrl'])

