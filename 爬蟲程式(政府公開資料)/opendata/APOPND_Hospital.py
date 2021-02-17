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

Log_path = os.path.join(path,"log","APOPND_Church.log")

logging.basicConfig(level=logging.INFO,
					format='[%(asctime)-4s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers = [logging.FileHandler(Log_path, 'w+', 'utf-8'),])

def replace_all(text, dic):
	for i, j in dic.items():
		text = text.replace(i, j)
	return text	

class APOPND_Hospiatl(): #主要抓的地方
	def __init__(self):
		self.APOPND_hospital_crawler()

	def APOPND_hospital_crawler(self):
		ContentList = []
		d = {'\n': '', '\r': '', '\xa0': '',' ': ''}

		logging.info("全國醫療機構")

		url = 'https://www.nhi.gov.tw/QueryN/Query3_Print.aspx?HospID=&HospName=&AreaID=&Address=&SpecialCode=&ServiceCode=&FuncCode=&ProtectCode=&HospType=&AntifluCode=&HospAlliance='
		res = requests.Session()
		res.keep_alive = False
		retry = Retry(connect=5, backoff_factor=0.5)
		adapter = HTTPAdapter(max_retries=retry)
		res.mount('https://', adapter)
		res = res.get(url,headers = headers)
		res.encoding=('utf-8')
		string = "Download URL : " + res.url
		logging.info(string)

		soup = bs4(res.text, 'html.parser')

		table = soup.find('table', class_ = 'GridView')
		table = table.findAll('tr')
		for tr in table[1:]:
			lst = []
			for td in tr.findAll('td'):
				lst.append(replace_all(td.text, d))
			ContentList.append([lst[0], lst[1], lst[2], lst[3], lst[4]])		 
				
		fileName = 'APOPND_hospital'
		df = pd.DataFrame(data=ContentList, columns=['醫療機構名稱', '地址', '電話', '垂直整合策略聯盟/主責醫事機構', '終止合約或歇業日期'])
		df.to_csv('data/csv/' + fileName + '.csv', sep=',', encoding='utf_8_sig', index=False)
		
if __name__ == "__main__":
	APOPND_Hospiatl()