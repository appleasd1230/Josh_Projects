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
import xml.etree.cElementTree as ET

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
path = str(Path(os.getcwd()))

Log_path = os.path.join(path,"log","APOPND_NewTaipei_Library.log")

logging.basicConfig(level=logging.INFO,
					format='[%(asctime)-4s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers = [logging.FileHandler(Log_path, 'w', 'utf-8'),])

def json2xml(json_str):
	Root = ET.Element('result')
	json_data = json.loads(json_str)

	for i1 in json_data['result']['records']:
		tmp = ET.SubElement(Root, 'records')
		for item in i1.items():
			ET.SubElement(tmp, item[0]).text = item[1]
	return ET.tostring(Root, encoding='unicode')

class APOPND_NewTaipei_Library(): #主要抓的地方
	def __init__(self):
		self.GetCSVurl()
		self.APOPND_NewTaipei_Library_crawler()

	def GetCSVurl(self):
		global URL_LIST

		url = "https://data.gov.tw/dataset/26601"
		'''建立Return機制, 因為可能會建立多組連線'''
		res = requests.Session()
		res.keep_alive = False
		retry = Retry(connect=5, backoff_factor=0.5)
		adapter = HTTPAdapter(max_retries=retry)
		res.mount('https://', adapter)
		res = res.get(url,headers = headers)

		soup = bs4(res.text, 'html.parser')
		# print(soup)
		data_url = soup.findAll('a', class_ = 'dgresource')
		for json_url in data_url:
			if 'JSON' in json_url.text and json_url.get('href').replace('https', 'http') not in URL_LIST:
				URL_LIST.append(json_url.get('href').replace('https', 'http'))

	def APOPND_NewTaipei_Library_crawler(self):
		logging.info("新北圖書館資料")
		
		global URL_LIST

		for url in URL_LIST:

			'''建立Return機制, 因為可能會建立多組連線'''
			res = requests.get(url, verify = False)
			# res.encoding=('utf-8')
			string = "Download URL : " + res.url

			logging.info(string)

			if(res.status_code == 200):
				Filename = 'APOPND_NewTaipei_Library.xml' #這裡要改
				storage_dir = path + "/data/xml/"  #這裡要改
				try:
					xml_data = json2xml(res.text)
					#寫入資料
					W.WritetoFile(xml_data, Filename, storage_dir)

					string = Filename + 'is Saving Done.' 
					logging.info(string) 
				except:
					logging.exception("ErrMsg :　")
			res.close()
if __name__ == "__main__":
	URL_LIST = []
	APOPND_NewTaipei_Library()