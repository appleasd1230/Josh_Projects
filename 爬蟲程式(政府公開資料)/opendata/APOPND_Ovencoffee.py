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

Log_path = os.path.join(path,"log","APOPND_Ovencoffee.log")

logging.basicConfig(level=logging.INFO,
					format='[%(asctime)-4s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers = [logging.FileHandler(Log_path, 'w', 'utf-8'),])
class APOPND_Ovencoffee(): #主要抓的地方
	def __init__(self):
		self.APOPND_Ovencoffee_crawler()

	def APOPND_Ovencoffee_crawler(self):
		ContentList = []

		for hundreds in range(10):
			for tens in range(10):
				for units in range(10):
					page = str(hundreds) + str(tens) + str(units)
					url = "http://www.ovencoffee.com.tw/store_list.asp?storeid=" + page
					'''建立Return機制, 因為可能會建立多組連線'''
					res = requests.Session()
					res.keep_alive = False
					retry = Retry(connect=5, backoff_factor=0.5)
					adapter = HTTPAdapter(max_retries=retry)
					res.mount('https://', adapter)
					res = res.get(url, headers = headers)
					res.encoding = ("utf-8")

					soup = bs4(res.text, 'html.parser')
					# print(soup)
					data = soup.findAll('p')

					if data[1].text != "" and data[1].text is not None:
						name = data[1].text
						phone = re.split(':', data[2].text)[1]
						business_time = str.join('', re.split(':', data[3].text))
						ContentList.append([name, phone, business_time])

		Filename = 'APOPND_Ovencoffee.csv' #這裡要改
		storage_dir = "data/csv/"  #這裡要改

		df = pd.DataFrame(data=ContentList, columns=['Name', 'Phone', 'Business_time'])
		df.to_csv(storage_dir + Filename , sep=',', encoding='utf_8_sig', index=False)

if __name__ == "__main__":
	APOPND_Ovencoffee()