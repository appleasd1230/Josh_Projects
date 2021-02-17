#coding:utf-8
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
import requests
import time as t
import pandas as pd
import random
# import urllib3

"""取得各頁網址(抓出每頁的連結)"""
def get_url():
    global url_lst # 呼叫全域變數url_lst
    page = 1
    state = True
    
    # 透過迴圈自動判斷哪幾頁是有資料的，再將其連結儲存起來
    while state:
        t.sleep(random.randint(10,15))
        url = 'https://www.moneydj.com/KMDJ/News/NewsRealList.aspx?index1=' + str(page) + '&a=MB010000'
        r = requests.get(url)
        # 判斷當前頁面是否為最後一頁
        soup = bs4(r.text, 'html.parser')       
        paging = soup.find(class_ = 'paging3')
        next_page = paging.findAll('td')[-2].find('a').get('href')
        # 如果當前頁面為最後一頁則跳出While迴圈
        state = next_page not in url
        if state:
            page += 1
            url_lst.append(url)
        else:
            page -= 1    

"""取得頁面資訊"""
def get_content():
    global url_lst # 呼叫全域變數url_lst
    global csv_lst # 呼叫全域變數csv_lst
    driver = webdriver.Chrome('./chromedriver.exe') # 使用selenium中chrome的操作
    for url in url_lst:
        time_lst = [] # 各則新聞時間清單        
        title_lst = [] # 各則新聞標題清單
        href_lst = [] # 各則新聞連結清單
        popularity_lst = [] # 各則新聞人氣清單

        # 使用selenium模擬真實瀏覽器操作        
        r = driver.get(url)
        source = driver.page_source
        soup = bs4(source, 'html.parser') # 解析Html
        news = soup.find(class_ = 'forumgrid') # 抓取涵蓋所需內容範圍的Html Tag
        
        for tr in news.findAll('tr')[1:]:
            time_lst.append(str.strip(tr.findAll('td')[0].text))
            title_lst.append(tr.findAll('td')[1].text)
            popularity_lst.append(tr.findAll('td')[2].find('span').text) # selenium
            href = 'https://www.moneydj.com/' + tr.findAll('td')[1].find('a').get('href')
            href_lst.append(href)

        # 透過迴圈將資料存取起來
        for i in range(0, len(href_lst)-1): 
            csv_lst.append([time_lst[i], title_lst[i], popularity_lst[i], href_lst[i]])
    driver.close() # 關閉網頁
    
"""設定CSV的欄位標題"""
def writePandas(data_lst):
    df = pd.DataFrame(data=csv_lst, columns=['時間','主題','人氣','連結'])
    return df

"""將存取的資料轉成CSV格式輸出"""
def To_csv():
    global csv_lst
    fileName = 'moneydj' + t.strftime('%y%m%d', t.localtime())
    try:
        df = pd.read_csv('data/csv/' + fileName + '.csv')
        record = df['時間'].values.tolist()
        df = df.append(writePandas(csv_lst), ignore_index=False)
        df.to_csv('data/csv/'+fileName+'.csv', sep=',', encoding='utf_8_sig', index=False)
    except:
        with open('data/csv/'+fileName+'.csv', 'w') as new_csv:
            pass
        df = writePandas(csv_lst)
        df.to_csv(r'data/csv/'+fileName+'.csv', sep=',', encoding='utf_8_sig', index=False)

if __name__ == '__main__':
    # 設定全域變數
    url_lst = [] # 理財網-全頁網址
    csv_lst = [] # csv內容
    # 執行函式
    get_url() 
    get_content()
    To_csv()
