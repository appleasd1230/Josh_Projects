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

City = ['基隆市', '台北市', '新北市', '宜蘭縣', '新竹市', '新竹縣', '桃園市', '苗栗縣',  \
'台中市', '彰化縣', '南投縣', '嘉義市', '嘉義縣', '雲林縣', '台南市', '高雄市', '屏東縣',  \
'台東縣', '花蓮縣', '金門縣', '連江縣', '澎湖縣']

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
path = str(Path(os.getcwd()))

Log_path = os.path.join(path,"log","APOPND_Louisacoffee.log")

logging.basicConfig(level=logging.INFO,
					format='[%(asctime)-4s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers = [logging.FileHandler(Log_path, 'w', 'utf-8'),])
class APOPND_Louisacoffee(): #主要抓的地方
	def __init__(self):
		self.APOPND_Louisacoffee_crawler()

	def APOPND_Louisacoffee_crawler(self):
		record = 0

		for city in City:
			url = "http://www.louisacoffee.co/visit_result"		
			'''建立Return機制, 因為可能會建立多組連線'''
			res = requests.Session()
			res.keep_alive = False
			retry = Retry(connect=5, backoff_factor=0.5)
			adapter = HTTPAdapter(max_retries=retry)
			res.mount('https://', adapter)
			res = res.post(url, headers = headers, data = {'data':{"county":city}})
			res.encoding = ('utf-8')

			print(res.status)

			soup = bs4(res.text, 'html.parser')

			soup = soup.find('div', id = 'result')

			table = soup.findAll('table', class_ = 'col-md-6')

			ContentList = []

			for tr in table:
				data = tr.findAll('tr')
				name = data[0].find('td').text
				phone = data[1].find('td').text
				address = data[2].find('td').text
				url = data[3].find('a').attrs['href']
				ContentList.append([name, phone, address, url])

			Filename = 'APOPND_' + City[record] + '_Louisacoffee.csv' #這裡要改
			storage_dir = "data/csv/"  #這裡要改

			df = pd.DataFrame(data=ContentList, columns=['Name', 'Phone', 'Address', 'URL'])
			df.to_csv(storage_dir + Filename , sep=',', encoding='utf_8_sig', index=False)			

			record += 1
			# print(data_url)

			# global URL_LIST
			# URL_LIST.append(data_url)

if __name__ == "__main__":
	APOPND_Louisacoffee()