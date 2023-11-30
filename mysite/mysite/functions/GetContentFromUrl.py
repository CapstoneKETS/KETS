import requests
from bs4 import BeautifulSoup as bs
import re
import math
import numpy as np
from _datetime import datetime
import bs4

def get_soup(url): # soup 객체를 가져옴
    res = requests.get(url)
    if res.status_code == 200:
        return bs(res.text, 'html.parser')
    else:
        print(f"Super big fail! with {res.status_code}")

def get_newsdata(url): # 뉴스 본문 페이지에서 데이터들을 가져오는 함수
    soup = get_soup(url)
    title = soup.find('title').get_text()
    reporter = soup.select_one('#newsEndContents > div.reporter_area div.reporter_profile > div > div.profile_info > a > div.name').get_text()
    company = soup.select_one('#content > div > div.content > div > div.link_news > div > h3 > span.logo').get_text()
    datetime = soup.select_one('#content > div > div.content > div > div.news_headline > div > span:nth-child(1)').get_text()
    datetime = get_datetime_from_news(datetime)
    article = soup.find('div', attrs={"id": "newsEndContents"})
    article = delete_child(article).get_text()
    newsdata = {}
    newsdata['title'] = title
    newsdata['reporter'] = reporter
    newsdata['company'] = company
    newsdata['datetime'] = datetime
    newsdata['article'] = article
    return newsdata

def get_datetime_from_news(datetime):
    datetime = re.split("[ .:]", datetime)
    if datetime[5] == "오후":
        datetime[6] = str(int(datetime[6]) + 12)
    datetime = datetime[1] + '.' + datetime[2] + '.' + datetime[3] + ' ' + datetime[6] + ':' + datetime[7]
    return datetime

def delete_child(tag):
    for child in tag.children:
        if isinstance(child, bs4.element.Tag):
            child.decompose()
    return tag

def get_related_newslist(topic): # 토픽이 주어지면, 관련 기사 링크들의 리스트를 반환
    url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=' + topic
    soup = get_soup(url)
    taglist = soup.select('.bx > div > div > div.news_info > div.info_group > a:nth-child(3)')
    linklist = []
    for tag in taglist:
        link = tag['href']
        linklist.append(link)
    print(linklist)
    return linklist

def get_datetime_from_news(datetime):
    datetime = re.split("[ .:]", datetime)
    if datetime[5] == "오후":
        datetime[6] = str(int(datetime[6]) + 12)
    datetime = datetime[1] + '.' + datetime[2] + '.' + datetime[3] + ' ' + datetime[6] + ':' + datetime[7]
    return datetime

def get_related_newsdatalist(topic):
    list = get_related_newslist(topic)
    newsdatalist = []
    for link in list:
        newsdata = get_newsdata(link)
        newsdatalist.append(newsdata)
    return newsdatalist

if __name__ == '__main__':
    topic = '투헬'
    get_related_newsdatalist(topic)