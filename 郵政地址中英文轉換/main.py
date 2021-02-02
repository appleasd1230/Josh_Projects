#coding:utf-8
from bs4 import BeautifulSoup as bs4
from string import digits
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import requests
import time as t
import re
import pandas as pd
import os, sys, io
import logging
from pathlib import Path

"""參數設置"""
record_err = False # 是否記錄錯誤資訊，建議不用
select_wait = 1 # 取得縣市鄉鎮街道選單選完等待時間
search_wait = 2 # 查詢完後等待結果時間


"""log紀錄"""
path = str(Path(os.getcwd()))
Err_Log_path = os.path.join(path,"log","error.log")
Info_Log_path = os.path.join(path,"log","info.log")

logging.basicConfig(level=logging.INFO,
					format='[%(asctime)-4s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers = [logging.FileHandler(Info_Log_path, 'w+', 'utf-8'),])

# logging.basicConfig(level=logging.ERROR,
# 					format='[%(asctime)-4s] %(message)s',
# 					datefmt='%Y-%m-%d %H:%M:%S',
# 					handlers = [logging.FileHandler(Err_Log_path, 'w+', 'utf-8'),])


"""使用headless模式"""
chrome_options = Options() # 啟動無頭模式
chrome_options.add_argument('--headless')  #規避google bug
chrome_options.add_argument('--disable-gpu')

"""取得縣市鄉鎮街道"""
def get_search_fators():
    url = 'https://www.post.gov.tw/post/internet/Postal/index.jsp?ID=207' # 郵政英譯網址
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=chrome_options) # 使用selenium中chrome的操作
    driver.get(url)
    source = driver.page_source # 網頁資訊
    soup = bs4(source, 'html.parser') # 解析Html

    city_list = Select(driver.find_element_by_id('city')) # 縣市選單

    """ 縣市下拉清單迴圈 """
    for city in city_list.options[1:]:
        city_list.select_by_visible_text(city.text) # 選擇某縣市
        t.sleep(select_wait)
        try:
            cityarea_list = Select(driver.find_element_by_id('cityarea')) # 鄉鎮選單
        except:
            # logging.info('以下縣市可能有漏抓 : ' + city.text)
            # logging.error(city.text + " Catch an exception.", exc_info=True)
            continue       

        """ 鄉鎮市區下拉清單迴圈 """
        for cityarea in cityarea_list.options:
            cityarea_list.select_by_visible_text(cityarea.text) # 選擇某縣市
            t.sleep(select_wait)
            try:
                # print('-------------------------------------------')
                # print(city.text + cityarea.text + '開始...........')
                # print('-------------------------------------------')
                street_list = Select(driver.find_element_by_id('street')) # 道路選單
            except Exception as e:
                # print(city.text + cityarea.text + '失敗 : ' + str(e))
                # logging.info('以下縣市鄉鎮可能有漏抓 : ' + city.text + cityarea.text)
                # logging.error(city.text + cityarea.text + " Catch an exception.", exc_info=True)
                continue
                
            """ 鄉鎮市區下拉清單迴圈 """
            for street in street_list.options:
                t.sleep(select_wait)                
                try:
                    street_list.select_by_visible_text(street.text) # 選擇道路
                    get_content(city.text, cityarea.text, street.text)
                except:
                    logging.info('以下地址可能有漏抓 : ' + city.text + cityarea.text + street.text) 
                    if record_err:
                        logging.error("抓資料失敗 錯誤訊息為 : ", exc_info=True)    
                    continue

        To_csv(city.text)

    driver.close() # 關閉網頁



"""主要查詢"""
def get_content(city, cityarea, street):
    global csv_lst

    url = 'https://www.post.gov.tw/post/internet/Postal/index.jsp?ID=207' # 郵政英譯網址
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=chrome_options) # 使用selenium中chrome的操作
    driver.get(url)
    source = driver.page_source # 網頁資訊
    soup = bs4(source, 'html.parser') # 解析Html

    """選擇縣市"""
    city_list = Select(driver.find_element_by_id('city')) # 縣市選單
    city_list.select_by_visible_text(city) # 選擇某縣市
    t.sleep(select_wait)

    """選擇鄉鎮"""
    cityarea_list = Select(driver.find_element_by_id('cityarea')) # 鄉鎮選單
    cityarea_list.select_by_visible_text(cityarea) # 選擇某縣市
    t.sleep(select_wait)

    """選擇街道"""
    street_list = Select(driver.find_element_by_id('street')) # 道路選單
    street_list.select_by_visible_text(street) # 選擇道路
    t.sleep(select_wait)

    """驗證碼處理"""
    code_area = soup.find(class_ = 'identify-pic') # 驗證碼區塊
    code_url = code_area.find('a').get('href') # 取得驗證碼連結

    code = get_security_num(code_url) # 取得驗證碼
    driver.find_element_by_id('checkImange').send_keys(code) # 點擊查詢
    
    driver.find_element_by_id('Submit1').click() # 點擊查詢
    t.sleep(search_wait)
    source_result = driver.page_source # 網頁資訊
    soup_result = bs4(source_result, 'html.parser') # 解析Html
    
    result = soup_result.find(id = 'tb1').find('td').text # 輸出結果
    result_lst = re.split(', ', result) # 輸出結果透過,區隔
    city_eng = result_lst[2][:-4] # 取得縣市英文
    cityarea_eng = result_lst[1] # 取得鄉鎮英文
    street_eng = result_lst[0] # 取得街道英文
    csv_lst.append([city, city_eng, cityarea, cityarea_eng, street, street_eng, city+cityarea+street, result]) # 將資料存入CSV
    # print(city + cityarea + street + ' : ' + city_eng + cityarea_eng + street_eng)

    driver.close() # 關閉網頁


"""取得驗證碼"""
def get_security_num(url):
    host = 'https://www.post.gov.tw'
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=chrome_options) # 使用selenium中chrome的操作
    driver.get(host + url) 
    source = driver.page_source # 網頁資訊
    soup = bs4(source, 'html.parser') # 解析Html
    code = soup.find('body').text # 取得驗證碼
    driver.close() # 關閉網頁
    return code.strip()


"""設定CSV的欄位標題"""
def writePandas(data_lst):
    df = pd.DataFrame(data=csv_lst, columns=['縣市中文', '縣市英文', '鄉鎮中文', '鄉鎮英文', '街道中文', '街道英文', '中文完整地址', '英文完整地址'])
    return df

"""將存取的資料轉成CSV格式輸出"""
def To_csv(city):
    global csv_lst
    fileName = city + '_' + t.strftime('%Y%m%d', t.localtime())
    try:
        df = pd.read_csv('data/csv/' + fileName + '.csv')
        record = df['縣市中文'].values.tolist()
        df = df.append(writePandas(csv_lst), ignore_index=False)
        df.to_csv('data/csv/'+fileName+'.csv', sep=',', encoding='utf_8_sig', index=False)
    except:
        with open('data/csv/'+fileName+'.csv', 'w') as new_csv:
            pass
        df = writePandas(csv_lst)
        df.to_csv(r'data/csv/'+fileName+'.csv', sep=',', encoding='utf_8_sig', index=False)
    csv_lst = []

if __name__ == '__main__':
    csv_lst = []
    get_search_fators()
