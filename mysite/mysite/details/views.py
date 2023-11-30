from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import requests
from bs4 import BeautifulSoup as bs
from .models import newsData
from .functions.GetContentFromUrl import *
from .functions.Keyword import *
from .functions.TextRank import *
from django.conf import settings
def index(request):
    return render(request, 'details/index.html')

def extractNoun(text):
    result = settings.kiwi.tokenize(text)
    for token in result:
        if token.tag in ['NNG', 'NNP']:
            yield token.form

def showDetails(request, url):
    # db에서 정보 조회
    data = newsData.objects.filter(Url = url)

    if not data: #db에 없으면
        # 웹 페이지 크롤링
        soup = get_soup(url)
        if soup:
            # 크롤링 정보 추출
            title = soup.find('title').get_text()
            reporter = soup.select_one(
                '#newsEndContents > div.reporter_area div.reporter_profile > div > div.profile_info > a > div.name').get_text()
            company = soup.select_one(
                '#content > div > div.content > div > div.link_news > div > h3 > span.logo').get_text()
            news_datetime = soup.select_one(
                '#content > div > div.content > div > div.news_headline > div > span:nth-child(1)').get_text()
            news_datetime = get_datetime_from_news(news_datetime)
            article = soup.find('div', attrs={"id": "newsEndContents"})
            article = delete_child(article).get_text()
            keyword = keywordExtract(settings.keyword_model, textPreprocessing(article))
            article = summarizeText(article)
            #크롤링한 정보 db에 저장
            new_data = newsData(url = url, title = title, reporter = reporter, company = company, created_datetime = news_datetime, article = article, keywords = keyword )
            new_data.save()

            return render(request, 'index.html', {'data': new_data})
    else:  # 데이터베이스에 이미 있는 경우
        return render(request, 'index.html', {'data': data})
# Create your views here.
