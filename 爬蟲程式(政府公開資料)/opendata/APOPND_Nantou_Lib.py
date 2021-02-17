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

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
path = str(Path(os.getcwd()))

Log_path = os.path.join(path,"log","APOPND_Nantou_Library.log")

logging.basicConfig(level=logging.INFO,
					format='[%(asctime)-4s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers = [logging.FileHandler(Log_path, 'w', 'utf-8'),])
class APOPND_Nantou_Library(): #主要抓的地方
	def __init__(self):
		self.GetCSVurl()
		self.APOPND_Nantou_Library_crawler()

	def GetCSVurl(self):
		url = "https://data.gov.tw/dataset/38349"
		'''建立Return機制, 因為可能會建立多組連線'''
		res = requests.Session()
		res.keep_alive = False
		retry = Retry(connect=5, backoff_factor=0.5)
		adapter = HTTPAdapter(max_retries=retry)
		res.mount('https://', adapter)
		res = res.get(url,headers = headers)

		soup = bs4(res.text, 'html.parser')
		# print(soup)
		data_url = soup.find('a', class_ = 'dgresource').attrs['href']
		global URL_LIST
		URL_LIST.append(data_url.replace('https', 'http'))

	def APOPND_Nantou_Library_crawler(self):
		logging.info("南投圖書館資料")
		
		global URL_LIST

		for url in URL_LIST:

			'''建立Return機制, 因為可能會建立多組連線'''
			res = requests.get(url, verify = False)
			res.encoding=('utf-8')
			string = "Download URL : " + res.url

			logging.info(string)

			if(res.status_code == 200):
				Filename = 'APOPND_Nantou_Library.csv' #這裡要改
				storage_dir = path + "/data/csv/"  #這裡要改
				try:
					#寫入資料
					W.WritetoFile(res.text,Filename,storage_dir)
					#由於資料有空白列因此重存, 先讀取再用pandas儲存
					data = pd.read_csv('data/csv/' + Filename)
					data.to_csv('data/csv/' + Filename, encoding='utf_8_sig',index=0)
					string = Filename + 'is Saving Done.'
					logging.info(string)
				except:
					logging.exception("ErrMsg :　")
			res.close()
if __name__ == "__main__":
	URL_LIST = []
	APOPND_Nantou_Library()