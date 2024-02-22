import json
import bs4.element
import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import math
import numpy as np
from sklearn.preprocessing import normalize
from _datetime import datetime
from keybert import KeyBERT
from kiwipiepy import Kiwi
from transformers import BertModel

# 참조 : https://bab2min.tistory.com/544, 한국어 불용어 사전 100
stop_words = ['지난해', '올해', '시즌', '향후', '한국', 'kbo', '야구','bbc']

url = "https://t1.daumcdn.net/cfile/tistory/241D6F475873C2B101"
model_type = 'skt/kobert-base-v1'
text = """
전 맨체스터 유나이티드 선수이자 잉글랜드 대표팀에서도 뛰었던 유망주 출신 제시 린가드(31)가 FC서울 유니폼을 입을 가능성이 점점 커지고 있다. 
지난 2일(한국시간) 영국 현지 매체들은 린가드가 K리그1 FC서울과 이적 협상 중이며, 이는 단순한 영입 의사 타진 수준이 아니라 계약서 싸인이 임박한 구체적인 협상이 이뤄지고 있다고 보도했다. 
린가드의 이적설은 이적 시장에 떠도는 각종 루머를 그대로 받아 쓰는 가십 매체가 아닌 BBC와 스카이스포츠 같은 유력 매체가 보도한 내용이라 더 놀라움을 줬다. 
스카이스포츠는 “린가드가 서울과 기본 2년, 1년 연장을 옵션으로 하는 구두 계약이 합의했다”고 전했다. 
FC서울 구단 역시 린가드와 이적 협상 중이라고 인정했다. 현지 매체들은 린가드의 서울행에 대해 '비현실적인 이적설'이라고 표현하며 놀라워하고 있다. 
린가드는 맨체스터 유나이티드(맨유) 유스 출신으로 본격적으로 맨유 1군에 데뷔하기 전 레스터 시티, 버밍엄 시티 등에 임대돼 실전 경험을 쌓은 뒤 2015~16시즌부터 맨체스터 유나이티드에서 본격적으로 뛰었다. 
맨유에 2021~22시즌까지 소속되었던 그는 맨유에서만 리그 149경기 20골, 컵대회 등 모든 대회를 통틀어 232경기 35골을 기록하며 활약했다. 2018 러시아 월드컵을 포함해 잉글랜드 대표팀에서도 뛰었다. 
그러나 린가드는 맨유 후반부 기량이 눈에 띄게 떨어져 결국 2022~23시즌 노팅엄 포레스트로 팀을 옮겼고, 현재는 팀을 찾지 못한 무적 상태다.   
한때 촉망받는 유망주였고, 특히 빅클럽인 맨유의 성골 스타로 이름을 떨쳤던 린가드가 K리그행을 선택한 건 전세계 축구팬에게 모두 파격적인 선택으로 받아들여지고 있다. 
특히 린가드가 선수들에게 파격적인 연봉을 제시하는 것으로 유명한 사우디아라비아 리그의 러브콜도 받았다는 점에서 이번 K리그 이적 협상이 더 놀라움을 주고 있다. 
사우디아라비아의 알샤밥이 린가드에게 구체적인 이적 제안을 한 것으로 알려졌다. 
스포츠 매체 스포츠바이블은 이런 결과에 대해 “사우디아라비아 리그에는 크리스티아누 호날두(알힐랄) 등 세계적인 스타들이 많이 있지만, 리그 자체의 흥행과 관중 규모가 매우 작은 것으로 악명이 높다. 
만일 린가드가 사우디 리그 대신 한국행을 선택한다면, 그는 사우디 보다 2배 더 많은 관중 앞에서 뛰게 된다”고 전했다. 
이 매체는 공식 기록을 근거로 사우디 리그는 보유하고 있는 스타 선수에 비해 관중과 흥행 규모가 작다면서 이는 K리그의 관중 기록에 훨씬 못 미친다고 짚었다. 
K리그는 만일 린가드가 서울 유니폼을 입게 될 경우 지난해 흥행 호조(단일 시즌 최초 홈관중 40만 명 돌파)에 더 탄력을 받을 것으로 기대하고 있다. 
"""

def get_soup(url): # soup 객체를 가져옴
    res = requests.get(url)
    if res.status_code == 200:
        return bs(res.text, 'html.parser')
    else:
        print(f"Super big fail! with {res.status_code}")

def modelLoad(model_type):
    model = BertModel.from_pretrained(f'{model_type}')
    kw_model = KeyBERT(model)
    return kw_model

def keywordExtract(keyBERT_model, text):
       keywords = keyBERT_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=stop_words, top_n=20, use_mmr=True)
       return keywords

def textPreprocessing(text):
    kiwi = Kiwi()
    results = []
    result = kiwi.analyze(text)
    for token, pos, _, _ in result[0][0]:
        if len(token) != 1 and pos.startswith('NNP') or pos.startswith('SL'):
            if token not in results:
                results.append(token)
    results = ' '.join(results)
    return results



if __name__ == '__main__':
    print(textPreprocessing(text))
    # kw_model = modelLoad(model_type)
    # keywords = keywordExtract(kw_model, textPreprocessing(text))
    # print(keywords)