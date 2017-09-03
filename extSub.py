# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import requests
import pandas as pd
import shutil
import time
import os

millis = int(round(time.time() * 1000))

url = "http://www.viruscomix.com/page324.html"
proxies = {
  'http': 'http://172.16.83.164:808',
  'https': 'https://172.16.83.164:808',
}

urls = []
for i in range(100000):

	print("Getting page for " + url + ", iterations = " + str(i))
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
	
	Nat = soup.findAll('img')
	image_source = ""
	url_temp = ""
	for nats in Nat:
		if(nats['src'][len(nats['src'])-3:]=='jpg'):
			image_source = nats['src']
		if('next' in nats['src'] or 'Next' in nats['src'] or 'NEXT' in nats['src']):
			url_temp = "http://www.viruscomix.com/" + nats.parent['href']
	
	if((url not in urls) and image_source!=""):
		millis = int(round(time.time() * 1000))-millis	
		print("Book after " + str(millis) + "ms!\nTotal distinct books = " + str(len(os.listdir('Comics/'))))	
		millis = int(round(time.time() * 1000))
		while(True):
			try:
				response = requests.get("http://www.viruscomix.com/" + image_source, stream=True,proxies=proxies)
			except requests.exceptions.RequestException as e:  # This is the correct syntax
				print(e)
				time.sleep(5)
				continue
			break
		with open('Comics/'+ str(len(urls)) + ". " +  image_source, 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		del response
		urls.append(url)

	url = url_temp