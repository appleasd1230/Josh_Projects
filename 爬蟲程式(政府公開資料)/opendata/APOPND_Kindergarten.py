#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
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

Log_path = os.path.join(path,"log","APOPND_Kindergarten.log")

logging.basicConfig(level=logging.INFO,
					format='[%(asctime)-4s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers = [logging.FileHandler(Log_path, 'w', 'utf-8'),])
class APOPND_Kindergarten(): #主要抓的地方
	def __init__(self):
		self.APOPND_Kindergarten_crawler()
	def APOPND_Kindergarten_crawler(self):
		logging.info("全國幼稚園資料")	
	
		for i in range(3, 8):
			url = "http://stats.moe.gov.tw/files/school/10" + str(i) + "/k1_new.csv"

			logging.info("url : " + url) 		
			'''建立Return機制, 因為可能會建立多組連線'''
			res = requests.Session()
			res.keep_alive = False
			retry = Retry(connect=5, backoff_factor=0.5)
			adapter = HTTPAdapter(max_retries=retry)
			res.mount('https://', adapter)
			res = res.get(url,headers = headers)
			res.encoding=('utf-8')
			string = "Download URL : " + res.url

			logging.info(string)

			if(res.status_code == 200):
				Filename = 'APOPND_Kindergarten_10' + str(i) + '.csv' #這裡要改
				storage_dir = path + "/data/csv/"  #這裡要改
				try:
					#寫入資料
					W.WritetoFile(res.text,Filename,storage_dir)

					#由於資料有空白列因此重存, 先讀取再用pandas儲存
					data = pd.read_csv('data/csv/' + Filename)
					data.to_csv('data/csv/' + Filename, encoding='utf_8_sig',index=0)					
					string = 'APOPND_Kindergarten_10' + str(i) + '.csv is Saving Done.' 
					logging.info(string) 
				except:
					logging.exception("ErrMsg :　")
			res.close()
if __name__ == "__main__":
	APOPND_Kindergarten()