import tkinter as tk
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import messagebox
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import requests
import time as t
import re
import os, sys, io
import logging
from pathlib import Path
import configparser
import traceback

"""log紀錄"""
path = str(Path(os.getcwd()))
Info_Log_path = os.path.join(path, "log", t.strftime('%Y%m%d', t.localtime()) + ".log")

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)-4s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers = [logging.FileHandler(Info_Log_path, 'a+', 'utf-8'),])

"""使用headless模式"""
chrome_options = Options() # 啟動無頭模式
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
"""使用chrome driver"""
driver = webdriver.Chrome('./chromedriver.exe', chrome_options=chrome_options) # 使用selenium中chrome的操作

"""錯誤訊息追蹤"""
def exception_to_string(excp):
   stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__) 
   pretty = traceback.format_list(stack)
   return ''.join(pretty) + '\n  {} {}'.format(excp.__class__,excp)

class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.CreateFrame()

    def CreateFrame(self):
        TitleStyle = tkFont.Font(family="微軟正黑體", size=30)
        ContentStyle = tkFont.Font(family="微軟正黑體", size=15)
        lst = ["3", "4", "5"]

        self.label = tk.Label(self, font=TitleStyle)
        self.label["text"] = "座標抓取程式"
        self.label.grid(row=1, column=0, sticky=tk.N+tk.W, padx=140, pady=20)

        self.entry = tk.Entry(self, width=30)
        self.entry.grid(row=2, column=0, sticky=tk.E, padx=200, pady=3)

        self.label2 = tk.Label(self, font=ContentStyle)
        self.label2["text"] = "店家名稱"
        self.label2.grid(row=2, column=0, sticky=tk.N+tk.W, padx=110, pady=10)

        self.var = tk.StringVar()
        self.var.set("5")
        self.OptLst = tk.OptionMenu(self, self.var, *lst)
        self.OptLst.grid(row=3, column=0, sticky=tk.W, padx=240, pady=3)

        self.label3 = tk.Label(self, font=ContentStyle)
        self.label3["text"] = "等待秒數"
        self.label3.grid(row=3, column=0, sticky=tk.N+tk.W, padx=110, pady=10)

        self.button = tk.Button(self, width=15, command=self.search_google_map)
        self.button["text"] = "取得座標"
        self.button.grid(row=4, column=0, sticky=tk.N+tk.W, padx=190, pady=10)

    """至Google Map搜尋餐廳"""
    def search_google_map(self):
        if self.entry.get() == '':
            messagebox.showwarning("提醒", "請輸入完整地址或店家名稱(含分店名))")
        
        try:
            url = 'https://www.google.com.tw/maps/place/'
            driver.get(url)
            driver.find_element(By.XPATH, '//input[@autofocus="autofocus"]').send_keys(self.entry.get())
            driver.find_element(By.XPATH, '//input[@autofocus="autofocus"]').send_keys(Keys.ENTER)
        except:
            logging.info("階段 : 可能是輸入地址因此不需搜尋")
            pass

        try:
            t.sleep(int(self.var.get())) # 等待X秒網頁跑完
            url_info = driver.current_url
            lat_long_info = url_info[url_info.index('!3d')+3:] # 解析網址中的經緯度
            latitude = lat_long_info.split('!4d')[1] # 經度
            longitude = lat_long_info.split('!4d')[0] # 緯度
            messagebox.showwarning("結果", "經度 : " + str(latitude) + '\n' + "緯度 : " + str(longitude))
        except:
            try:
                t.sleep(int(self.var.get())) # 等待X秒網頁跑完
                url_info = driver.current_url
                lat_long_info = url_info[url_info.index('!3d')+3:] # 解析網址中的經緯度
                latitude = lat_long_info.split('!4d')[1] # 經度
                longitude = lat_long_info.split('!4d')[0] # 緯度
                messagebox.showwarning("結果", "經度 : " + str(latitude) + '\n' + "緯度 : " + str(longitude))            
            except Exception as err:
                logging.info("錯誤階段 : 解析經緯度失敗，可能是時間延長後還是不夠 : ")
                logging.info(exception_to_string(err))
                return False
        driver.quit()

        # try:
        #     url = 'https://www.google.com.tw/maps/place/' + self.entry.get()
        #     driver.get(url)
        #     t.sleep(1)
        #     driver.find_element_by_id('searchbox-searchbutton').click() # 點擊搜尋
        #     t.sleep(int(self.var.get())) # 等待X秒網頁跑完
        # except Exception as err:
        #     logging.info("錯誤階段 : 搜尋該地址異常 : ")
        #     logging.info(exception_to_string(err))
        #     messagebox.showwarning("錯誤", "請確認地址完整或店家名稱正確，或是將等待秒數延長")
        #     return False

        # try:
        #     driver.find_element_by_class_name('section-hero-header-title-description-container') # 如果有明確位置就抓
        # except Exception as err:
        #     logging.info("錯誤階段 : 抓不到完整得地址 : ")
        #     logging.info(exception_to_string(err))
        #     messagebox.showwarning("錯誤", "請確認地址完整或店家名稱正確，或是將等待秒數延長")
        #     return False

        # try:
        #     url_info = driver.current_url
        #     lat_long_info = url_info[url_info.index('!3d')+3:] # 解析網址中的經緯度
        #     latitude = lat_long_info.split('!4d')[1] # 經度
        #     longitude = lat_long_info.split('!4d')[0] # 緯度
        #     messagebox.showwarning("結果", "經度 : " + str(latitude) + '\n' + "緯度 : " + str(longitude))
        # except Exception as err:
        #     logging.info("錯誤階段 : 解析經緯度失敗 : ")
        #     logging.info(exception_to_string(err))
        #     messagebox.showwarning("錯誤", "請確認地址完整或店家名稱正確，或是將等待秒數延長")
        #     return False

root = tk.Tk()
root.geometry('500x300')
app = Application(root)
root.mainloop()
