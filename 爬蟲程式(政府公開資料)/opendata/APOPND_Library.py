#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
import os, sys, io
import re
import logging
import datetime
import xmltodict, json
from pathlib import Path
import WriteFile as W
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

City = ['Kinmen', 'Lienchiang','Chiayi', 'Hsinchu', 'Penghu', 'Miaoli']
City_Id = ['City000021', 'City000022', 'City000013', 'City000006', 'City000020', 'City000007']

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
path = str(Path(os.getcwd()))

Log_path = os.path.join(path,"log","APOPND_Library.log")

logging.basicConfig(level=logging.INFO,
					format='[%(asctime)-4s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers = [logging.FileHandler(Log_path, 'w', 'utf-8'),])
class APOPND_Library(): #主要抓的地方
	def __init__(self):
		self.APOPND_Library_crawler()

	def APOPND_Library_crawler(self):
		record = 0

		for city_id in City_Id:
			url = "https://plisnet.nlpi.edu.tw/Frontend/LibraryFamily/LibraryList"
			'''建立Return機制, 因為可能會建立多組連線'''
			res = requests.Session()
			res.keep_alive = False
			retry = Retry(connect=5, backoff_factor=0.5)
			adapter = HTTPAdapter(max_retries=retry)
			res.mount('https://', adapter)
			res = res.post(url, headers = headers, data = {'City': city_id})
			res.encoding = ('utf-8')

			soup = bs4(res.text, 'html.parser')
			# print(soup)
			table = soup.findAll('table', class_ = 'table')

			ContentList = []

			for tr in table:
				data = tr.findAll('tr')
				name = data[0].find('td').text
				phone = data[1].find('td').text
				address = data[2].find('td').text
				url = data[3].find('a').attrs['href']
				ContentList.append([name, phone, address, url])

			Filename = 'APOPND_' + City[record] + '_Library.csv' #這裡要改
			storage_dir = "data/csv/"  #這裡要改

			df = pd.DataFrame(data=ContentList, columns=['Name', 'Phone', 'Address', 'URL'])
			df.to_csv(storage_dir + Filename , sep=',', encoding='utf_8_sig', index=False)			

			record += 1
			# print(data_url)

			# global URL_LIST
			# URL_LIST.append(data_url)

if __name__ == "__main__":
	APOPND_Library()