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
        self.NewsDropDwonMenu = [
        "蘋果日報",
        "自由時報"
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
            newlist = getAppleNewsList(self.entry.get(), self.page, self.index)  # 取得新聞資訊(連結、標題、index、page)
            if newlist == '0':
                messagebox.showwarning('提示', '此關鍵字可能搜尋不到結果，或是程式異常!')
                return
            else:
                self.NewsList = newlist # 取得新聞資訊(連結、標題、index、page)
                newscontent = getAppleNewContent(self.NewsList[1]) # 取得新聞內容
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
        curItem = self.tree.focus()
        index = self.tree.item(curItem).get('text')
        value = self.tree.item(curItem).get('values')
        value.extend(index)
        self.SelectAccountRow = value
        self.button4['state'] = tk.NORMAL # 打開編輯按鈕
        self.button6['state'] = tk.NORMAL # 打開發文按鈕
        self.button8['state'] = tk.NORMAL # 打開刪除按鈕

    # 儲存編輯
    def SaveEdit(self):
        if self.entry2.get() == '' or self.entry3.get() == '' or self.entry4.get() == '':
            messagebox.showwarning('提示', '不可有任一欄為空值!')
            self.root2.attributes("-topmost", True)
            return
        self.AccountList[int(self.SelectAccountRow[-1])] = [self.entry2.get(), \
                                                        self.entry3.get(), self.entry4.get()] # 更改編輯內容
        messagebox.showinfo('提示', '已儲存變更!')                                           
        self.root2.quit() # 關閉編輯視窗
        self.root2.destroy() # 關閉編輯視窗
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


    # 新增帳密
    def AddEdit(self):
        if self.entry2.get() == '' or self.entry3.get() == '' or self.entry4.get() == '':
            messagebox.showwarning('提示', '不可有任一欄為空值!')
            self.root2.attributes("-topmost", True)
            return
        self.AccountList.append([self.entry2.get(), self.entry3.get(), self.entry4.get()]) # 新增帳密
        messagebox.showinfo('提示', '已新增帳密!')
        self.root2.quit() # 關閉編輯視窗
        self.root2.destroy() # 關閉編輯視窗
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

    # 開啟編輯帳密視窗
    def EditAccountFrame(self):
        labelStyle = tkFont.Font(family="Lucida Grande", size=20)
        self.root2 = tk.Tk()
        self.root2.geometry('630x400')
        # 帳密管理
        self.label5 = tk.Label(self.root2, font=labelStyle)
        self.label5["text"] = "帳號"
        self.label5.grid(row=0, column=0, sticky=tk.W, padx=65, pady=20)
    
        self.label6 = tk.Label(self.root2, font=labelStyle)
        self.label6["text"] = "密碼"
        self.label6.grid(row=0, column=1, sticky=tk.W, padx=65, pady=20)

        self.label7 = tk.Label(self.root2, font=labelStyle)
        self.label7["text"] = "版型"
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
        self.button5 = tk.Button(self.root2, font=labelStyle, command=self.SaveEdit)
        self.button5.config(fg='#613030', bg='#F0F0F0')
        self.button5["text"] = "儲存結果"
        self.button5.grid(row=2, column=0, columnspan=3, padx=30, pady=20, ipadx=30, ipady=10)

        self.entry2.insert(END, self.SelectAccountRow[0]) # 所選帳號
        self.entry3.insert(END, self.SelectAccountRow[1]) # 所選密碼
        self.entry4.insert(END, self.SelectAccountRow[2]) # 所選版型

        self.root2.resizable(0, 0)
        self.root2.attributes("-topmost", True)
        self.root2.mainloop()

    # 開啟新增帳密視窗
    def AddAccountFrame(self):
        labelStyle = tkFont.Font(family="Lucida Grande", size=20)
        self.root2 = tk.Tk()
        self.root2.geometry('630x400')
        # 帳密管理
        self.label5 = tk.Label(self.root2, font=labelStyle)
        self.label5["text"] = "帳號"
        self.label5.grid(row=0, column=0, sticky=tk.W, padx=65, pady=20)
    
        self.label6 = tk.Label(self.root2, font=labelStyle)
        self.label6["text"] = "密碼"
        self.label6.grid(row=0, column=1, sticky=tk.W, padx=65, pady=20)

        self.label7 = tk.Label(self.root2, font=labelStyle)
        self.label7["text"] = "版型"
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
        self.root2.attributes("-topmost", True)
        self.root2.mainloop()

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

        # 關鍵字欄位
        self.label = tk.Label(self, font=labelStyle)
        self.label["text"] = "搜尋關鍵字"
        self.label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=20)

        self.entry = tk.Entry(self, font=labelStyle, highlightthickness=1)
        self.entry.config(highlightbackground = "gray", highlightcolor= "gray")
        self.entry.grid(row=0, column=1, sticky=tk.W, ipadx=150, ipady=2, pady=20)
  
        # 新聞清單
        self.label = tk.Label(self, font=labelStyle)
        self.label["text"] = "選擇新聞網"
        self.label.grid(row=0, column=2, sticky=tk.W, padx=20, pady=20)

        self.variable = tk.StringVar(self)
        self.variable.set(self.NewsDropDwonMenu[0])
        self.variable.trace('w', self.callback)
        self.NewsOpt = tk.OptionMenu(self, self.variable, *self.NewsDropDwonMenu)
        self.NewsOpt.config(font=ButtonStyle, highlightthickness=1, highlightbackground='gray', highlightcolor='gray')
        self.NewsOpt.grid(row=0, column=3, sticky=tk.W, padx=0, pady=20, ipadx=15, ipady=10)

        # 爬文按鈕
        self.button = tk.Button(self, font=ButtonStyle, command=self.getNews)
        self.button.config(fg='#613030', bg='#F0F0F0')
        self.button["text"] = "抓取新聞"
        self.button.grid(row=0, column=4, sticky=tk.W, padx=30, pady=20, ipadx=30, ipady=10)

        # 新聞標題
        self.label2 = tk.Label(self, font=labelStyle)
        self.label2["text"] = "新聞標題"
        self.label2.grid(row=1, column=0, sticky=tk.E, pady=20)

        self.text=tk.Text(self, font=ButtonStyle, height=1, width=70, highlightthickness=1)
        self.text.config(font=labelStyle, highlightbackground = "gray", highlightcolor= "gray")
        self.text.grid(row=1, column=1, columnspan=4, ipadx=10, ipady=1)

        # 新聞內容
        self.label3 = tk.Label(self, font=labelStyle)
        self.label3["text"] = "新聞內容"
        self.label3.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=70, pady=100)

        self.text2=tk.Text(self, font=ButtonStyle, height=10, width=60, highlightthickness=1)
        self.text2.config(font=labelStyle, highlightbackground = "gray", highlightcolor= "gray")
        self.text2.grid(row=2, column=1, rowspan=2, columnspan=4, pady=20, ipadx=5, ipady=20)

        self.button2 = tk.Button(self, font=ButtonStyle, command=self.getPreNews)
        self.button2["text"] = "上一篇"
        self.button2['state'] = tk.DISABLED
        self.button2.grid(row=3, column=0, sticky=tk.W, padx=30, ipadx=15, ipady=10)

        self.button3 = tk.Button(self, font=ButtonStyle, command=self.getNextNews)
        self.button3["text"] = "下一篇"
        self.button3['state'] = tk.DISABLED
        self.button3.grid(row=3, column=1, sticky=tk.W, ipadx=15, ipady=10)

        # 帳密管理
        self.label4 = tk.Label(self, font=labelStyle)
        self.label4["text"] = "帳密管理"
        self.label4.grid(row=4, column=0, columnspan=2, rowspan=3, sticky=tk.W, padx=70, pady=100)

        self.tree=ttk.Treeview(self, show='headings', selectmode = 'browse') # 表格
        self.tree['columns']=('帳號', '密碼', '版型')
        self.tree.column('帳號', width=125, anchor=tk.CENTER)   # 表示列,不顯示
        self.tree.column('密碼', width=125, anchor=tk.CENTER)
        self.tree.column('版型', width=125, anchor=tk.CENTER)

        self.tree.heading('帳號', text='帳號')  # 顯示表頭
        self.tree.heading('密碼', text='密碼')
        self.tree.heading('版型', text='版型')

        # 開啟帳密文件
        with open('account.txt', 'r', encoding='utf-8') as f:
            self.AccountList = f.readlines()
            f.close()

        self.AccountList = self.ExtendList(self.AccountList) # 將index加入AccountList
        # 將table組出來
        for lst in self.AccountList[::-1]:
            self.tree.insert('', int(lst[-1]), text=lst[-1], values=(lst[0], lst[1], lst[2])) # 插入資料
        self.tree.grid(row=4, column=1, columnspan=2, rowspan=3, sticky=tk.W, padx=127)
        self.tree.bind('<<TreeviewSelect>>', self.SelectAccountTable)

        # 編輯按鈕
        self.button4 = tk.Button(self, font=ButtonStyle, command=self.EditAccountFrame)
        self.button4.config(fg='#613030', bg='#F0F0F0')
        self.button4["text"] = "編輯選擇帳密"
        self.button4['state'] = tk.DISABLED # 關閉按鈕
        self.button4.grid(row=4, column=2, sticky=tk.W, ipadx=30, ipady=10)

        # 新增按鈕
        self.button7 = tk.Button(self, font=ButtonStyle, command=self.AddAccountFrame)
        self.button7.config(fg='#613030', bg='#F0F0F0')
        self.button7["text"] = "新增帳號密碼"
        self.button7.grid(row=5, column=2, sticky=tk.W, ipadx=30, ipady=10, pady=0)

                # 新增按鈕
        self.button8 = tk.Button(self, font=ButtonStyle, command=self.DeleteAccountFrame)
        self.button8.config(fg='#613030', bg='#F0F0F0')
        self.button8["text"] = "刪除選擇帳密"
        self.button8['state'] = tk.DISABLED # 關閉按鈕
        self.button8.grid(row=6, column=2, sticky=tk.W, ipadx=30, ipady=10, pady=0)

        # 發文
        self.button6 = tk.Button(self, font=ButtonStyle, command=self.PostNews)
        self.button6.config(fg='#613030', bg='#F0F0F0')
        self.button6["text"] = "使用此帳密發文"
        self.button6['state'] = tk.DISABLED # 關閉按鈕
        self.button6.grid(row=4, column=3, rowspan=3, sticky=tk.W, ipadx=20, ipady=10)

root = tk.Tk()
root.geometry('1200x800')
app = Application(root)
root.resizable(0, 0)
root.mainloop()
