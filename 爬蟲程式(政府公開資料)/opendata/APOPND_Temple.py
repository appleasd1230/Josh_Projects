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

Log_path = os.path.join(path,"log","APOPND_Temple.log")

logging.basicConfig(level=logging.INFO,
					format='[%(asctime)-4s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers = [logging.FileHandler(Log_path, 'w', 'utf-8'),])
class APOPND_Temple(): #主要抓的地方
	def __init__(self):
		self.APOPND_post_crawler()
	def APOPND_post_crawler(self):
		logging.info("全國宗教資訊系統資料-寺廟")	
	
		url = "http://religion.moi.gov.tw/Report/temple.xml"#這裡要改
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
			Filename = 'APOPND_Temple.xml' #這裡要改
			storage_dir = path + "/data/xml/"  #這裡要改
			try:
				#寫入資料
				W.WritetoFile(res.text,Filename,storage_dir)
				#由於資料有空白列因此重存, 先讀取再用pandas儲存
				string = 'APOPND_Temple.xml is Saving Done.' 
				logging.info(string) 
			except:
				logging.exception("ErrMsg :　")
		res.close()
if __name__ == "__main__":
	APOPND_Temple()