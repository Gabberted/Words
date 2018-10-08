#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line example for Custom Search.

Command-line application that does a search.
"""

__author__ = 'jcgregorio@google.com (Joe Gregorio)'

import pprint
import json

from googleapiclient.discovery import build


def main():
	# Build a service object for interacting with the API. Visit
	# the Google APIs Console <http://code.google.com/apis/console>
	# to get an API key for your own application.
	service = build("customsearch", "v1",
		developerKey="AIzaSyCwT1XDUNE3euUFJqJt1Fa0hvk34h-MadY")

	res = service.cse().list(
	q='cat',
	cx='017576662512468239146:omuauf_lfve'
	).execute()



#	res = service.cse().list(
#	q=' +  + ',
#	cx='017576662512468239146:omuauf_lfve',
#	).execute()
	#res=str(res)
#	for item in res:
#		print(res)
	Json_string=json.loads(res[])
	for item in Json_string:
		print(item)
if __name__ == '__main__':
  main()
