# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import requests
import pandas as pd
import shutil
import time

millis = int(round(time.time() * 1000))

url = "http://www.viruscomix.com/page433.html"
proxies = {
  'http': 'http://172.16.114.112:3128',
  'https': 'https://172.16.114.112:3128',
}

urls = []
for i in range(100000):

	print("Getting page for " + url + ", iterations = " + str(i))
	if(url not in urls):
		while(True):
			try:
				page = requests.get(url,proxies=proxies)
				millis = int(round(time.time() * 1000))-millis	
				print("Distinct book after " + str(millis) + "ms!\nTotal distinct books = " + str(len(urls) + 1))	
				millis = int(round(time.time() * 1000))
			except requests.exceptions.RequestException as e:  # This is the correct syntax
				print(e)
				time.sleep(5)
				continue
			break

		html = page.content
		soup = BeautifulSoup(html,'lxml')
		
		Nat = soup.findAll('img')
		image_source = ""
		urls.append(url)
		for nats in Nat:
			if(nats['src'][len(nats['src'])-3:]=='jpg'):
				image_source = nats['src']
			if(nats['src'][len(nats['src'])-8:]=='next.gif'):
				url = "http://www.viruscomix.com/" + nats.parent['href']

		while(True):
			try:
				response = requests.get("http://www.viruscomix.com/" + image_source, stream=True,proxies=proxies)
			except requests.exceptions.RequestException as e:  # This is the correct syntax
				print(e)
				time.sleep(5)
				continue
			break
		with open('Comics/'+ image_source, 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		del response