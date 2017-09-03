# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import requests
import pandas as pd
import shutil
import time
import os

millis = int(round(time.time() * 1000))


proxies = {
  'http': 'http://172.16.83.164:808',
  'https': 'https://172.16.83.164:808',
}

urls = []
for i in range(12,369):

	url = "http://www.viruscomix.com/page" + str(i) + ".html"
	print("Getting page for " + str(i))
	while(True):
		try:
			page = requests.get(url,proxies=proxies)
		except requests.exceptions.RequestException as e:  # This is the correct syntax
			print(e)
			time.sleep(5)
			continue
		break

	html = page.content
	soup = BeautifulSoup(html,'lxml')
	
	Nat = soup.find('img')

	if(Nat is not None):
		image_source = "http://www.viruscomix.com/" + Nat['src']
		
		millis = int(round(time.time() * 1000))-millis	
		print("Book after " + str(millis) + "ms!\nTotal distinct books = " + str(len(os.listdir('Others/'))))	
		millis = int(round(time.time() * 1000))
		
		while(True):
			try:
				response = requests.get(image_source, stream=True,proxies=proxies)
			except requests.exceptions.RequestException as e:  # This is the correct syntax
				print(e)
				time.sleep(5)
				continue
			break
		
		with open('Others/'+ str(i) + ". " + Nat['src'], 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		del response