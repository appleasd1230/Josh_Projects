#coding:utf-8
from types import resolve_bases
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs4
import requests
import os
import logging
from pathlib import Path
import time as t
import traceback

"""log紀錄"""
path = str(Path(os.getcwd()))
# 若路徑不存在則新增
if not os.path.exists(path + '\\' + 'log' + '\\' + 'spider'):
    os.makedirs(path + '\\' + 'log' + '\\' + 'spider')
Info_Log_path = os.path.join(path, "log/spider", t.strftime('%Y%m%d', t.localtime()) + ".log")
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)-4s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers = [logging.FileHandler(Info_Log_path, 'a+', 'utf-8'),])


"""設定chrome option"""
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080") # 指定網頁視窗大小
chrome_options.add_argument('–log-level=3')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--headless') # 使用無頭模式

"""錯誤訊息追蹤"""
def exception_to_string(excp):
   stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__) 
   pretty = traceback.format_list(stack)
   return ''.join(pretty) + '\n  {} {}'.format(excp.__class__,excp)

"""取得新聞列表"""
def getETtodayNewsList(keyword, page=1, index=0):
    logging.info('開始查詢ETtoday，關鍵字使用 : ' + keyword)
    result_lst = [] # 存取新聞連結以及標題
    ETtoday_url = 'https://www.ettoday.net/news_search/doSearch.php?keywords=' + keyword + '&kind=20&idx=1' # 蘋果日報網址
    r = requests.get(ETtoday_url)
    soup = bs4(r.text, 'html.parser')
    try:
        main_area = soup.find(id = 'result-list') # 取得主要區塊列表
        news_lst = main_area.find_all(class_ = 'archive clearfix') # 取得新聞列表
        # 將每一篇新聞的標題以及連結存取起來
        news = news_lst[index]
        href = news.find(class_ = 'box_2').find('a').get('href')
        title = news.find(class_ = 'box_2').find('a').text
        result_lst.append(title)
        result_lst.append(href)
        result_lst.append(index)
        result_lst.append(page)
        print(result_lst)
        return result_lst
    except Exception as err:
        logging.info('ETtoday抓取關鍵字「' + keyword + '」時出錯，原因為 : ' + exception_to_string(err))
        return '0'

"""抓取新聞內容"""
def getETtodayNewContent(href):
    try:
        r = requests.get(href)
        soup = bs4(r.text, 'html.parser')
        contents = soup.find(class_ = 'story').find_all('p') # 內文
        result = ''
        # 將內文多個p組合起來
        for content in contents:
            result = result + str(content)
        return result
    except Exception as err:
        logging.info('取得此篇ETtoday新聞(' + href + ')內文失敗，原因為 : ' + exception_to_string(err))
        return '0'

"""取得新聞列表"""
def getLtnNewsList(keyword, page=1, index=0):
    try:
        # 如果超過當頁20筆，則換頁
        if index >= 20:
            getLtnNewsList(keyword, page+1, 0)
        logging.info('開始查詢自由時報3C，關鍵字使用 : ' + keyword)
        result_lst = [] # 存取新聞連結以及標題
        ltn_url = 'https://search.ltn.com.tw/list?keyword=' + keyword + \
                '&start_time=' + t.strftime('%Y0101', t.localtime()) + \
                '&end_time=' + t.strftime('%Y%m%d', t.localtime()) + '&sort=date&type=3c&page=' + str(page) # 自由時報3C網站
        r = requests.get(ltn_url)
        soup = bs4(r.text, 'html.parser')
        # 查看是否有資料
        news_lst = soup.find_all(class_ = 'list boxTitle') # 取得新聞列表

        # 將每一篇新聞的標題以及連結存取起來
        news = news_lst[index]
        href = news.find('a').get('href')
        title = news.find(class_ = 'tit').text
        result_lst.append(title)
        result_lst.append(href)
        result_lst.append(index)
        result_lst.append(page)
        return result_lst
    except Exception as err:
        logging.info('自由時報3C抓取關鍵字「' + keyword + '」時出錯，原因為 : ' + exception_to_string(err))
        return '0'

"""抓取新聞內容"""
def getLtnNewContent(href):
    try:
        result = ''
        r = requests.get(href)
        soup = bs4(r.text, 'html.parser')
        contents = soup.find(class_ = 'text').find_all('p')[:-3]
        for content in contents:
            result = result + str(content)
    except Exception as err:
        logging.info('取得此篇自由時報3C(' + href + ')內文失敗，原因為 : ' + exception_to_string(err))
        return '0'
if __name__ == '__main__':
    getETtodayNewContent('https://www.ettoday.net/news/20210330/1949350.htm')
