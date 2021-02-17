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

# headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
path = str(Path(os.getcwd()))

Log_path = os.path.join(path,"log","APOPND_Church.log")

logging.basicConfig(level=logging.INFO,
					format='[%(asctime)-4s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers = [logging.FileHandler(Log_path, 'w+', 'utf-8'),])
class APOPND_Church(): #主要抓的地方
	def __init__(self):
		self.GetPages()
		self.APOPND_church_crawler()

	def GetPages(self):
		page_url = "https://church.oursweb.net/slocation.php?w=1&c=TW&a=&t="
		res = requests.get(page_url)
		soup = bs4(res.text, 'html.parser')
		page_div = soup.find('table', class_ = 'tb_pages')
		page_info = page_div.find('td').text
		max_page = int(re.split(' ', re.split("/ ", page_info)[1])[0])
		global URL_LIST
		for page in range(1, max_page):
			URL_LIST.append(page_url + '&p=' + str(page))

	def APOPND_church_crawler(self):
		ContentList = []
		global URL_LIST
		for url in URL_LIST:
			res = requests.get(url)
			soup = bs4(res.text, 'html.parser')
			tb_a = soup.findAll('tr', class_ = 'tb_line_a')
			for a_datas in  tb_a:
				lst = []
				for a_data in a_datas.findAll('td'):
					lst.append(a_data.text)
				ContentList.append([lst[0], lst[1], lst[2], lst[3], lst[4]])

			tb_b = soup.findAll('tr', class_ = 'tb_line_b')
			for b_datas in  tb_b:
				lst = []
				for b_data in b_datas.findAll('td'):
					lst.append(b_data.text)
				ContentList.append([lst[0], lst[1], lst[2], lst[3], lst[4]])		 
				
		fileName = 'APOPND_church'
		df = pd.DataFrame(data=ContentList, columns=['名稱', '國家城市', '服務性質', '電話', '負責人'])
		df.to_csv('data/csv/' + fileName + '.csv', sep=',', encoding='utf_8_sig', index=False)
		

"""
		page = res.find('')
	
		url = "https://church.oursweb.net/slocation.php?w=1&c=TW&a=&t=&p=" + str(page)#這裡要改
		logging.info("url : " + url) 
		
		'''建立Return機制, 因為可能會建立多組連線'''
		res = requests.Session()
		res.keep_alive = False
		retry = Retry(connect=5, backoff_factor=0.5)
		adapter = HTTPAdapter(max_retries=retry)
		res.mount('https://', adapter)
		res = res.get(url,headers = headers)
		print(res.text)
		string = "Download URL : " + res.url
		logging.info(string)

		if(res.status_code == 200):
			o = xmltodict.parse(res.text)
			oo = json.dumps(o)
			print(oo)
			Filename = 'APOPND_post.csv' #這裡要改
			storage_dir = path + "/data/csv/"  #這裡要改
			#print(storage_dir,Filename)
			# try:
			# 	#寫入資料
			# 	W.WritetoFile(res.text,Filename,storage_dir)
			# 	#由於資料有空白列因此重存, 先讀取再用pandas儲存
			# 	storage_dir = path + "/data/csv/"
			# 	filename = storage_dir+"\\"+ 'APOPND_post.csv'
			# 	data = pd.read_csv(filename)
			# 	data.to_csv(filename, encoding='utf_8_sig',index=0)
			# 	string = 'APOPND_post.csv is Saving Done.' 
			# 	logging.info(string) 
			# except:
			# 	string = 'APOPND_post.csv is Saving Failed.'
			# 	logging.info(string)
		res.close()
"""
if __name__ == "__main__":
	URL_LIST = []
	APOPND_Church()