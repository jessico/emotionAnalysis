import os
import time
import json
import random
import csv
import re

import jieba
import requests
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 设置生成的词云形状图片
WC_MASK_IMG = 'wordCloudShape.jpg'
# 设置评论数据保存路径
COMMENT_FILE_PATH = 'goods.txt'
# 设置词云字体
WC_FONT_PATH = 'songti.ttf'
num=0

def spider_comment(page=0, key=0):
    """
    爬取指定页的评价数据
    :param page: 爬取第几，默认值为0
    """

    url ="https://club.jd.com/comment/productPageComments.action?callback=jQuery8086946" \
         "&productId=10027813820127&score=0&sortType=5&page=%s&pageSize=10&pin=jd_noxPSkIagzoZ&_=1625474372582" % page

    kv = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          'Referer': 'https://item.jd.com/'+ key + '.html',
          'cookies':'thor=2E42B544D5807751A88E99DF89791FD3ECECCF74A13EF63A676218176A9954F9908CEC7765E9D39A3819DC2AF7AB1914FB9957186782A20D185FAEE33D2652833077AE3795F2CEB18FF6CBB00A08C62F6F0F63C956EC5AB33F0D570D001343E956DEB8A274DCEF293B8A92F60CB7A091EDDE0253C3638D6D6955C6C76FF1AD7BE885014D9BA48121AA9D8C6E4208C8DB10EFEA9B0A002DDC75C012BA370C0009'
          }
    try:
        r = requests.get(url, headers=kv)
        r.raise_for_status()
    except:
        print('爬取失败')
    # 截取json数据字符串
    r_json_str =r.text[14:-2]
    # 字符串转json对象
    r_json_obj = json.loads(r_json_str)
    # 获取评价列表数据
    r_json_comments = r_json_obj['comments']
    # 遍历评论对象列表
    for r_json_comment in r_json_comments:
        # 以追加模式换行写入每条评价
        with open(COMMENT_FILE_PATH, 'a+') as file:
            file.write(r_json_comment['content'] + '\n')
        # 打印评论对象中的评论内容
        global num
        print(num,r_json_comment['content'])
        num=num+1


def batch_spider_comment():
    """
        批量爬取评价
        """

    #key = input("Please enter the address:")
    #key = re.sub("\D","",key)
    key='45947543572'
    #通过range来设定爬取的页面数
    for i in range(0,99):
        spider_comment(i,key)
        # 模拟用户浏览，设置一个爬虫间隔，防止ip被封
        time.sleep(random.random() * 5)


def cut_word():
    """
    对数据分词
    :return: 分词后的数据
    """
    with open(COMMENT_FILE_PATH) as file:
        comment_txt = file.read()
        wordlist = jieba.cut(comment_txt, cut_all=False)#精确模式
        wl = " ".join(wordlist)
        print(wl)
        return wl


def create_word_cloud():
    """44144127306
    生成词云
    :return:
    """
    # 设置词云形状图片
    wc_mask = np.array(Image.open(WC_MASK_IMG))
    # 设置词云的一些配置，如：字体，背景色，词云形状，大小
    wc = WordCloud(background_color="white", max_words=2000, mask=wc_mask, scale=4,
                   max_font_size=50, random_state=42,font_path =WC_FONT_PATH)
    # 生成词云
    wc.generate(cut_word())
    # 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.show()
    wc.to_file("jd_ysld.jpg")


def txt_change_to_csv():
    with open('goods.csv', 'w+', encoding="utf8", newline='')as c:
        writer_csv = csv.writer(c, dialect="excel")
        with open("goods.txt", 'r', encoding='utf8')as f:
            # print(f.readlines())
            for line in f.readlines():
                # 去掉str左右端的空格并以空格分割成list
                line_list = line.strip('\n').split(',')
                print(line_list)
                writer_csv.writerow(line_list)

if __name__ == '__main__':
    # 爬取数据
    #batch_spider_comment()
    cut_word()
    #转换数据
    #txt_change_to_csv()

    # 生成词云
    #create_word_cloud()
