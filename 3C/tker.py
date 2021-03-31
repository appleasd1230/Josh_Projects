import tkinter as tk
from tkinter import ttk
from tkinter.constants import ANCHOR, CENTER, END
import tkinter.font as tkFont
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import traceback
import logging
import os
from pathlib import Path
import time as t
from typing import Text
from spider import *
from post import *
import re
# from lib.fbCrawler import start_crawl 

"""log紀錄"""
path = str(Path(os.getcwd()))
# 若路徑不存在則新增
if not os.path.exists(path + '\\' + 'log' + '\\' + 'tker'):
    os.makedirs(path + '\\' + 'log' + '\\' + 'tker')

log_path = os.path.join(path, "log/tker", t.strftime('%Y%m%d', t.localtime()) + ".log")


logging.basicConfig(level=logging.INFO,
					format='[%(asctime)-4s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers = [logging.FileHandler(log_path, 'a+', 'utf-8'),])

"""錯誤訊息追蹤"""
def exception_to_string(excp):
   stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__) 
   pretty = traceback.format_list(stack)
   return ''.join(pretty) + '\n  {} {}'.format(excp.__class__,excp)

class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.StatusMenu = [
        "開啟",
        "關閉"
        ] 
        self.page = 1 # 頁數
        self.index = 0 # index
        self.NewsList = [] # title/href/index/page
        self.NewsContent = '' # 新聞內容
        # take the data 
        self.AccountList = [] # 帳密管理清單
        self.SelectAccountRow = [] # AccountTable 選擇單行帳密
        self.CreateFrame()

    # 更換新聞網站
    def callback(self, *args):
        self.page = 1 # 頁數
        self.index = 0 # index
        self.NewsList = [] # title/href/index/page
        self.NewsContent = '' # 新聞內容
        self.text.delete('1.0', END)
        self.text2.delete('1.0', END)
        self.button2['state'] = tk.DISABLED # 關閉上一篇按鈕
        self.button3['state'] = tk.DISABLED # 關閉下一篇按鈕

    # 取得新聞
    def getNews(self):
        if self.entry.get() == '':
            messagebox.showwarning('提示', '請先輸入搜尋關鍵字!')
            return
        
        self.text.delete('1.0', END)
        self.text2.delete('1.0', END)
        # # 用關鍵字去查詢新聞網
        if self.variable.get() == '蘋果日報':
            newlist = getETtodayNewsList(self.entry.get())  # 取得新聞資訊(連結、標題、index、page)
            if newlist == '0':
                messagebox.showwarning('提示', '此關鍵字可能搜尋不到結果，或是程式異常!')
                return
            else:
                self.NewsList = newlist # 取得新聞資訊(連結、標題、index、page)
                newscontent = getETtodayNewContent(self.NewsList[1]) # 取得新聞內容
                if newscontent == '0':
                    messagebox.showwarning('提示', '此篇新聞內文' + self.NewsList[1] + '程式抓取不到!')
                    return
                else:
                    self.NewsContent = newscontent
        else:
            newlist = getLtnNewsList(self.entry.get(), self.page, self.index) # 取得新聞資訊(連結、標題、index、page)
            if newlist == '0':
                messagebox.showwarning('提示', '此關鍵字可能搜尋不到結果，或是程式異常!')
                return
            else:     
                self.NewsList = newlist # 取得新聞資訊(連結、標題、index、page)
                newscontent = getLtnNewContent(self.NewsList[1]) # 取得新聞內容
                if newscontent == '0':
                    messagebox.showwarning('提示', '此篇新聞內文' + self.NewsList[1] + '程式抓取不到!')
                    return
                else:               
                    self.NewsContent = newscontent
        
        self.page = self.NewsList[3] # 紀錄頁數
        self.index = self.NewsList[2] # 紀錄index
        self.text.insert(END, self.NewsList[0]) # 插入標題
        self.text2.insert(END, self.NewsContent) # 插入新聞內容
        self.button2['state'] = tk.NORMAL # 打開上一篇按鈕
        self.button3['state'] = tk.NORMAL # 打開下一篇按鈕

    # 下一篇新聞
    def getNextNews(self):
        self.index = self.index + 1
        self.getNews()

    # 上一篇新聞
    def getPreNews(self):
        if self.index >= 1:
            self.index = self.index - 1
            self.getNews()
        else:
            messagebox.showwarning('提示', '已經是第一筆新聞了!')
            return

    # 新增index到AccoountList
    def ExtendList(self, AccountList):
        new_lst = []
        index = 0
        for lst in AccountList:
            lst = re.split('/', lst.strip('\n'))
            lst.extend(str(index))
            new_lst.append(lst)
            index += 1
        return new_lst

    # 編輯所選帳密
    def SelectAccountTable(self, event):
        self.entry.delete(0, END) # 清空專案
        self.text.delete('1.0', END) # 清空搜尋用關鍵字
        self.text2.delete('1.0', END) # 清空專案
        self.variable.set('關閉') # 清空狀態
        curItem = self.tree.focus()
        index = self.tree.item(curItem).get('text')
        value = self.tree.item(curItem).get('values')
        value.extend(index)
        self.SelectAccountRow = value
        self.SetDetail() # 寫入明細
        self.button2['state'] = tk.NORMAL # 打開編輯按鈕
        self.button3['state'] = tk.NORMAL # 打開發文按鈕

    # 寫入明細
    def SetDetail(self):
        self.entry.insert(END, self.SelectAccountRow[0]) # 寫入專案
        self.text.insert(END, self.SelectAccountRow[4]) # 寫入搜尋用關鍵字
        self.text2.insert(END, self.SelectAccountRow[5]) # 寫入搜尋用關鍵字
        self.variable.set(self.SelectAccountRow[3]) # 寫入狀態
        return

    # 開啟新增帳密視窗
    def AddAccountFrame(self):
        labelStyle = tkFont.Font(family="Lucida Grande", size=20)
        self.root2 = tk.Tk()
        self.root2.geometry('630x400')
        # 帳密管理
        self.label5 = tk.Label(self.root2, font=labelStyle)
        self.label5["text"] = "專案"
        self.label5.grid(row=0, column=0, sticky=tk.W, padx=65, pady=20)
    
        self.label6 = tk.Label(self.root2, font=labelStyle)
        self.label6["text"] = "帳號"
        self.label6.grid(row=0, column=1, sticky=tk.W, padx=65, pady=20)

        self.label7 = tk.Label(self.root2, font=labelStyle)
        self.label7["text"] = "密碼"
        self.label7.grid(row=0, column=2, sticky=tk.W, padx=65, pady=20)

        self.entry2 = tk.Entry(self.root2, font=labelStyle, highlightthickness=1)
        self.entry2.config(highlightbackground = "gray", highlightcolor= "gray")
        self.entry2.grid(row=1, column=0, sticky=tk.W, ipadx=5, ipady=2, padx=5, pady=20)

        self.entry3 = tk.Entry(self.root2, font=labelStyle, highlightthickness=1)
        self.entry3.config(highlightbackground = "gray", highlightcolor= "gray")
        self.entry3.grid(row=1, column=1, sticky=tk.W, ipadx=5, ipady=2, padx=5, pady=20)

        self.entry4 = tk.Entry(self.root2, font=labelStyle, highlightthickness=1)
        self.entry4.config(highlightbackground = "gray", highlightcolor= "gray")
        self.entry4.grid(row=1, column=2, sticky=tk.W, ipadx=5, ipady=2, padx=5, pady=20)

        # 確認編輯
        self.button5 = tk.Button(self.root2, font=labelStyle, command=self.AddEdit)
        self.button5.config(fg='#613030', bg='#F0F0F0')
        self.button5["text"] = "新增帳密"
        self.button5.grid(row=2, column=0, columnspan=3, padx=30, pady=20, ipadx=30, ipady=10)

        self.root2.resizable(0, 0)
        # self.root2.attributes("-topmost", True)
        self.root2.mainloop()

    # 儲存編輯
    def SaveEdit(self):
        if self.entry.get() == '' or len(self.text.get("1.0", "end-1c")) == 0 or len(self.text2.get("1.0", "end-1c")) == 0:
            messagebox.showwarning('提示', '不可有任一欄為空值!')
            return
        print(self.AccountList[int(self.SelectAccountRow[-1])])
        self.AccountList[int(self.SelectAccountRow[-1])][0] = self.entry.get() # 更改專案內容
        self.AccountList[int(self.SelectAccountRow[-1])][3] = self.variable.get() # 更改狀態
        self.AccountList[int(self.SelectAccountRow[-1])][4] = str(self.text.get('1.0', 'end')).replace('\n', '') # 更改查詢關鍵字內容 
        self.AccountList[int(self.SelectAccountRow[-1])][5] = str(self.text2.get('1.0', 'end')).replace('\n', '') # 更改插入文字內容
        print(self.AccountList[int(self.SelectAccountRow[-1])])
        messagebox.showinfo('提示', '已儲存變更!')
        self.tree.delete(*self.tree.get_children())

        # 開啟帳密文件
        with open('account.txt', 'w+', encoding='utf-8') as f:
            for lst in self.AccountList:
                f.write('/'.join(lst[0:6]))
                f.write('\n')
            f.close()

        # 開啟帳密文件
        with open('account.txt', 'r', encoding='utf-8') as f:
            self.AccountList = f.readlines()
            f.close()

        self.AccountList = self.ExtendList(self.AccountList) # 將index加入AccountList
        # 將table組出來
        for lst in self.AccountList[::-1]:
            self.tree.insert('', int(lst[-1]), text=lst[-1], values=(lst[0], lst[1], lst[2], \
                                                                    lst[3], lst[4], lst[5])) # 插入資料

    # 新增帳密
    def AddEdit(self):
        self.root2.attributes("-topmost", False)
        if self.entry2.get() == '' or self.entry3.get() == '' or self.entry4.get() == '':
            messagebox.showwarning('提示', '不可有任一欄為空值!')
            self.root2.attributes("-topmost", True)
            return
        self.AccountList.append([self.entry2.get(), self.entry3.get(), self.entry4.get() \
                                ,'停止', '0', '0']) # 新增專案
        messagebox.showinfo('提示', '已新增專案!')
        self.root2.quit() # 關閉編輯視窗
        self.root2.destroy() # 關閉編輯視窗
        self.tree.delete(*self.tree.get_children())
        self.button2['state'] = tk.DISABLED # 關閉編輯按鈕
        self.button3['state'] = tk.DISABLED # 關閉刪除按鈕

        # 開啟帳密文件
        with open('account.txt', 'w+', encoding='utf-8') as f:
            for lst in self.AccountList:
                f.write('/'.join(lst[0:6]))
                f.write('\n')
            f.close()

        # 開啟帳密文件
        with open('account.txt', 'r', encoding='utf-8') as f:
            self.AccountList = f.readlines()
            f.close()

        self.AccountList = self.ExtendList(self.AccountList) # 將index加入AccountList
        # 將table組出來
        for lst in self.AccountList[::-1]:
            self.tree.insert('', int(lst[-1]), text=lst[-1], values=(lst[0], lst[1], lst[2], \
                                                                    lst[3], lst[4], lst[5])) # 插入資料


    # 刪除選擇帳密
    def DeleteAccountFrame(self):
        MsgBox = tk.messagebox.askquestion('提示', '請確認是否刪除這筆資料?', icon = 'warning')
        if MsgBox == 'yes':
            del self.AccountList[int(self.SelectAccountRow[-1])] # 刪除這組帳密
            messagebox.showinfo('提示', '已刪除所選帳密!')
        else:
            return
        self.tree.delete(*self.tree.get_children())
        self.button4['state'] = tk.DISABLED # 關閉編輯按鈕
        self.button6['state'] = tk.DISABLED # 關閉發文按鈕
        self.button8['state'] = tk.DISABLED # 關閉刪除按鈕

        # 開啟帳密文件
        with open('account.txt', 'w+', encoding='utf-8') as f:
            for lst in self.AccountList:
                f.write('/'.join(lst[0:3]))
                f.write('\n')
            f.close()

        # 開啟帳密文件
        with open('account.txt', 'r', encoding='utf-8') as f:
            self.AccountList = f.readlines()
            f.close()

        self.AccountList = self.ExtendList(self.AccountList) # 將index加入AccountList
        # 將table組出來
        for lst in self.AccountList[::-1]:
            self.tree.insert('', int(lst[-1]), text=lst[-1], values=(lst[0], lst[1], lst[2])) # 插入資料    

    # 發文
    def PostNews(self):
        if len(self.text.get("1.0", "end-1c")) == 0 or len(self.text2.get("1.0", "end-1c")) == 0:
            messagebox.showwarning('提示', '新聞標題或新聞內容不可為空!')
            return
        try:
            if self.SelectAccountRow[2] == 1: # 如果是版型一
                post_type_one(self.SelectAccountRow[0], self.SelectAccountRow[1], \
                                self.text.get('1.0', 'end'), self.text2.get('1.0', 'end'))
            elif self.SelectAccountRow[2] == 2: # 如果是版型二
                # post_type_two(self.SelectAccountRow[0], self.SelectAccountRow[1], \
                #                 self.text.get('1.0', 'end'), self.text2.get('1.0', 'end'))
                messagebox.showwarning('提示', '版型二還在開發中!')
                return
            else:
                messagebox.showwarning('提示', '尚未有版型三，請確認帳密清單沒有設定錯誤!')
                return
            messagebox.showinfo('提示', '發文完成!')
            return
        except Exception as err:
            logging.info('發文時發生錯誤，原因為 : ' + exception_to_string(err))
            messagebox.showwarning('提示', '發文時發生錯誤，請聯繫系統開發人員!')
            return

    # 初始化界面
    def CreateFrame(self):
        labelStyle = tkFont.Font(family="Lucida Grande", size=20)
        ButtonStyle = tkFont.Font(family="Lucida Grande", size=10)

        # ----------------表格--------------------
        self.tree=ttk.Treeview(self, show='headings', selectmode = 'browse') # 表格
        self.tree['columns']=('專案', '帳號', '密碼', '狀態')
        # 表示列,不顯示
        self.tree.column('專案', width=125, anchor=tk.CENTER)
        self.tree.column('帳號', width=125, anchor=tk.CENTER)   
        self.tree.column('密碼', width=125, anchor=tk.CENTER)
        self.tree.column('狀態', width=125, anchor=tk.CENTER)
        # 顯示表頭
        self.tree.heading('專案', text='專案')  
        self.tree.heading('帳號', text='帳號')
        self.tree.heading('密碼', text='密碼')
        self.tree.heading('狀態', text='狀態')

        # 開啟帳密文件
        with open('account.txt', 'r', encoding='utf-8') as f:
            self.AccountList = f.readlines()
            f.close()

        self.AccountList = self.ExtendList(self.AccountList) # 將index加入AccountList
        # 將table組出來
        for lst in self.AccountList[::-1]:
            self.tree.insert('', int(lst[-1]), values=(lst[0], lst[1], lst[2], lst[3], \
                                                        lst[4], lst[5], lst[6])) # 插入資料
        self.tree.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10, ipady=150)
        self.tree.bind('<<TreeviewSelect>>', self.SelectAccountTable)

        # 新增按鈕
        self.button = tk.Button(self, font=ButtonStyle, bg="#FFD2D2", command=self.AddAccountFrame)
        self.button["text"] = "新增專案"
        self.button.grid(row=1, column=0, ipadx=20, ipady=15)

        # ----------------明細&修改--------------------
        self.LabelFrame = tk.LabelFrame(self, text='內容修改', font=ButtonStyle)
        self.LabelFrame.config(font=labelStyle)
        self.LabelFrame.grid(row=0, column=3, columnspan=5, rowspan=5, padx=20, pady=0, ipadx=5, ipady=50)

        # 專案
        self.label = tk.Label(self.LabelFrame, font=labelStyle, bg="#66B3FF")
        self.label["text"] = "專案(title)"
        self.label.grid(row=0, column=0,  padx=10, pady=5)

        self.entry = tk.Entry(self.LabelFrame, font=labelStyle)
        self.entry.grid(row=0, column=1,  padx=10, pady=5, ipadx=100)

        # 搜尋用關鍵字
        self.label2 = tk.Label(self.LabelFrame, font=labelStyle, bg="#66B3FF")
        self.label2["text"] = "搜尋用關鍵字"
        self.label2.grid(row=1, column=0,  padx=10)

        self.text=tk.Text(self.LabelFrame, font=ButtonStyle, height=3, width=35)
        self.text.config(font=labelStyle)
        self.text.grid(row=1, column=1, rowspan=2, pady=20, ipadx=5, ipady=10)

        # 插入文字
        self.label3 = tk.Label(self.LabelFrame, font=labelStyle, bg="#66B3FF")
        self.label3["text"] = "插入文字"
        self.label3.grid(row=3, column=0, padx=10)

        self.text2=tk.Text(self.LabelFrame, font=ButtonStyle, height=3, width=35)
        self.text2.config(font=labelStyle)
        self.text2.grid(row=3, column=1, rowspan=2, pady=5, ipadx=5, ipady=5)

        # 狀態
        self.label4 = tk.Label(self.LabelFrame, font=labelStyle, bg="#66B3FF")
        self.label4["text"] = "狀態"
        self.label4.grid(row=5, column=0, padx=10)

        self.variable = tk.StringVar(self.LabelFrame)
        self.variable.set(self.StatusMenu[0])
        NewsOpt = tk.OptionMenu(self.LabelFrame, self.variable, *self.StatusMenu)
        NewsOpt.config(font=labelStyle)
        NewsOpt.grid(row=5, column=1, pady=5, ipadx=20)

        # 儲存按鈕
        self.button2 = tk.Button(self.LabelFrame, font=ButtonStyle, bg="#E6E6F2", command=self.SaveEdit)
        self.button2["text"] = "儲存"
        self.button2['state'] = tk.DISABLED # 關閉編輯按鈕      
        self.button2.grid(row=7, column=0, columnspan=2, pady=70, ipadx=50, ipady=10)

        # 刪除按鈕
        self.button3 = tk.Button(self.LabelFrame, font=ButtonStyle, bg="#BEBEBE", command=self.getNews)
        self.button3["text"] = "刪除"
        self.button3['state'] = tk.DISABLED # 關閉刪除按鈕
        self.button3.grid(row=8, column=0, columnspan=2, pady=10, ipadx=50, ipady=10)

        # # description
        # self.label3 = tk.Label(self.LabelFrame, font=labelStyle, bg="#66B3FF")
        # self.label3["text"] = "description"
        # self.label3.grid(row=3, column=0, padx=10)

        # self.text2=tk.Text(self.LabelFrame, font=ButtonStyle, height=5, width=35)
        # self.text2.config(font=labelStyle)
        # self.text2.grid(row=3, column=1, rowspan=2, pady=5, ipadx=5, ipady=10)

        # # keywords
        # self.label4 = tk.Label(self.LabelFrame, font=labelStyle, bg="#66B3FF")
        # self.label4["text"] = "keywords"
        # self.label4.grid(row=5, column=0, padx=10)

        # self.text3=tk.Text(self.LabelFrame, font=ButtonStyle, height=3, width=35)
        # self.text3.config(font=labelStyle)
        # self.text3.grid(row=5, column=1, rowspan=2, pady=5, ipadx=5, ipady=5)

        # # 插入文字
        # self.label4 = tk.Label(self.LabelFrame, font=labelStyle, bg="#66B3FF")
        # self.label4["text"] = "插入文字"
        # self.label4.grid(row=7, column=0, padx=10)

        # self.text3=tk.Text(self.LabelFrame, font=ButtonStyle, height=3, width=35)
        # self.text3.config(font=labelStyle)
        # self.text3.grid(row=7, column=1, rowspan=2, pady=5, ipadx=5, ipady=5)

        # # 狀態
        # self.label4 = tk.Label(self.LabelFrame, font=labelStyle, bg="#66B3FF")
        # self.label4["text"] = "狀態"
        # self.label4.grid(row=9, column=0, padx=10)

        # self.variable = tk.StringVar(self.LabelFrame)
        # self.variable.set(self.StatusMenu[0])
        # NewsOpt = tk.OptionMenu(self.LabelFrame, self.variable, *self.StatusMenu)
        # NewsOpt.config(font=labelStyle)
        # NewsOpt.grid(row=9, column=1, pady=5, ipadx=20)
 



root = tk.Tk()
root.geometry('1300x800')
app = Application(root)
root.resizable(0, 0)
root.mainloop()
