#coding:utf-8
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os, sys, io
import logging
from pathlib import Path
import time as t
import traceback
import configparser

"""config"""
config = configparser.ConfigParser()
config.read('Config.ini', encoding = 'utf-8')
years = config.get('Parameters', 'Year').split(',') # 取得年份
seasons = config.get('Parameters', 'Season').split(',') # 取得季
real_estate_citys = config.get('Parameters', 'RealEstateCity').split(',') # 取得不動產縣市
presale_house_citys = config.get('Parameters', 'PresaleHouseCity').split(',') # 取得預售屋縣市

"""log紀錄"""
path = str(Path(os.getcwd()))
Info_Log_path = os.path.join(path, "log", t.strftime('%Y%m%d', t.localtime()) + ".log")

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)-4s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers = [logging.FileHandler(Info_Log_path, 'a+', 'utf-8'),])


"""設定chrome option"""
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080") # 指定網頁視窗大小
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
"""使用chrome driver"""
driver = webdriver.Chrome('./chromedriver.exe', chrome_options=chrome_options) # 使用selenium中chrome的操作


"""錯誤訊息追蹤"""
def exception_to_string(excp):
   stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__) 
   pretty = traceback.format_list(stack)
   return ''.join(pretty) + '\n  {} {}'.format(excp.__class__,excp)

"""主流程"""
def main():
    url = 'http://plvr.land.moi.gov.tw/DownloadOpenData' # 內政部不動產時價登錄網
    driver.get(url)
    driver.execute_script("window.alert = function () { return true}") # 防止彈出視窗
    driver.find_element(By.XPATH, '//a[text()="非本期下載"]').click() # 點選非本期下載
    driver.find_element_by_id('downloadTypeId2').click() # 點選進階下載
    # 台北、新北、高雄 - 不動產買賣
    driver.find_elements_by_xpath("//tr[contains(text(), '臺北市')]//td")[1].click()
    driver.find_elements_by_xpath("//tr[contains(text(), '新北市')]//td")[1].click()
    driver.find_elements_by_xpath("//tr[contains(text(), '高雄市')]//td")[1].click()
    # 桃園、台中 - 預售屋買賣
    driver.find_elements_by_xpath("//tr[contains(text(), '桃園市')]//td")[2].click()
    driver.find_elements_by_xpath("//tr[contains(text(), '臺中市')]//td")[2].click()

    Select(driver.find_element_by_id('fileFormatId')).select_by_value('csv') # 下載檔案格式選擇CSV格式

    for year in years:
        for season in seasons:
            Select(driver.find_element_by_id('historySeason_id')).select_by_value(year + season) # 下載檔案格式選擇CSV格式
            driver.find_element_by_id('downloadBtnId').click() # 點選下載

if __name__ == '__main__':
    main()


