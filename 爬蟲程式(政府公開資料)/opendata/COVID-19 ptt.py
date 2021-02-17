source activate MyProfileName
conda install basemap

import requests
from datetime import datetime
# import sqlite3 # fot sqlute database support
from bs4 import BeautifulSoup
from mpl_toolkits.basemap import Basemap

class Crawler:
    pttUrl = "https://www.ptt.cc"

    def __init__(self, board):
        self.board = board
        self.Articles = []
        self.boardUrl = "/bbs/{}".format(board)
        self.contents = []

    def getToday(self, date=None, pageNext=None, keyword=None, num_posts=100):
        if pageNext == None:
            pageNext = self.boardUrl
        request = requests.get(Crawler.pttUrl + pageNext, cookies = {"over18": "1"})
        if request.status_code == 404:
            print("No such board")
            return
        self.pageText = request.text
        soup = BeautifulSoup(self.pageText, "lxml")
        pageNext = soup.find("div", "btn-group btn-group-paging").find_all("a")[1].attrs["href"]
        if date == None:
            date = datetime(2020, 2, 12) 
        pageText = self.pageText.split("r-list-sep")[0]
        soup = BeautifulSoup(pageText, "lxml")
        for post in soup.select("div.r-ent"):
            url = post.find("div", "title").a
            if url == None:
                continue
            else:
                url = post.find("div", "title").a.attrs["href"]
            articleTxt = requests.get(Crawler.pttUrl + url, cookies = {"over18": "1"}).text
            articleSoup = BeautifulSoup(articleTxt, "lxml")
            title = articleSoup.find("title").text  # 標題
            content = articleSoup.find("meta", property="og:description").get("content")  # 文章內容
            if title == None or content == None:
                continue
            if keyword != None:
                if title.find(keyword) < 0 and content.find(keyword) < 0:
                    continue
            # print(Crawler.pttUrl + url)
#             print(type(title))
            self.contents.append(title + ":" + content)
#             self.contents.append(content)
            push_list = []
            for push in articleSoup.find_all("span", class_="push-content"):
                if len(push.text[2:]) <= 0:
                    continue
                push_list.append(push.text[2:])  # 推文
            self.contents.append(push_list)  
            time_str = post.find("div", "date").text.strip()
            time_obj = datetime.strptime(time_str+"/2020", '%m/%d/%Y')
            #if True:  # 一篇文章
            if time_obj < date:  # 不是今天的文章
                return
        else:
            if len(self.contents)/2 > num_posts:
                return
            # print(pageNext)
            self.getToday(date, pageNext, keyword, num_posts)

"""
board = "nCoV2019"
crawler = Crawler(board)
crawler.getToday(date=datetime(2019, 12, 31), num_posts=50)
"""
"""修改參數區"""
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
board = "nCoV2019" # Ptt專版名稱
crawler = Crawler(board) # 呼叫Class，請別動這段!
num_posts = 50 # 要爬幾篇(一個日期幾篇)
lst = [] # 定義新的lst，誤動!

# 看你要幾個日期，就加幾個datetime進去...最後一個的後面不用逗點
lst.append([
    datetime(2015, 4, 5),
    datetime(2016, 4, 5),
    datetime(2017, 4, 5),
    datetime(2018, 4, 5),
    datetime(2019, 4, 5),
    datetime(2020, 4, 5),
    datetime(2021, 4, 5)
    ])

# 以下迴圈誤動!
for datetime_lst in lst: # 解析lst
    for datetime_infor in datetime_lst: # 抓出每個日期
        crawler.getToday(date=datetime_infor, num_posts) # 日期
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# crawler.getToday(date=datetime(2020, 1, 3), num_posts=50)
# crawler.getToday(date=datetime(2020, 1, 5), num_posts=50)
# crawler.getToday(date=datetime(2020, 1, 6), num_posts=50)
# crawler.getToday(date=datetime(2020, 1, 7), num_posts=50)

print(len(crawler.contents))

import tensorflow as tf
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

import os
import sys

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
ws = WS("./data", disable_cuda=False)
pos = POS("./data", disable_cuda=False)
ner = NER("./data", disable_cuda=False)

word_sentence_list = ws(
    crawler.contents,
    sentence_segmentation=True, # To consider delimiters
    segment_delimiter_set = {",", "。", ":", "?", "!", ";", ".", "（", "）", "", "()", " [",
        "] ", ":", "", "》"}, # This is the defualt set of delimiters
#     recommend_dictionary = dictionary1, # words in this dictionary are encouraged
#     coerce_dictionary = dictionary2, # words in this dictionary are forced
)

pos_sentence_list = pos(word_sentence_list)

entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

del ws
del pos
del ner

import pandas as pd

count_list = []
# count_dict = {}
for e in entity_sentence_list:
    for i in e:
# count_dict[i[3]] = count_dict.get(i[3], 0) + 1
# df = pd.concat([df, pd.DataFrame(i[3])])
        count_list.append(i[3])


from collections import Counter

entity = Counter(count_list)
entity.most_common(10)

df = pd.DataFrame(count_list, columns=["entity"])
text = df.entity.value_counts()
text.head(30)


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt


text = " ".join(review for review in count_list)
font_path = 'C:\\Users\\admin\AppData\\Local\\Microsoft\\Windows\\Fonts\\NotoSansCJK-Regular.ttc'
# back_color = imageio.imread("./taiwan.png")
wordcloud = WordCloud(width=1200, height=600, max_font_size=200, max_words=200, background_color="black", 
                      font_path=font_path, colormap="Dark2").generate(text)

map = Basemap(llcrnrlon = 119.3, llcrnrlat = 20.7, urcrnrlon = 124.6, urcrnrlat = 26,
resolution = 'h', epsg = 3415)
map.drawcoastlines()
plt.figure(dpi=600)
plt.imshow(wordcloud)
plt.axis("off")
plt.show()            #   須為字串且每個分詞以空白相隔

