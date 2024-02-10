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
stop_words = ['지난해', '올해', '시즌', '향후', '한국', 'kbo', '야구']

url = "https://t1.daumcdn.net/cfile/tistory/241D6F475873C2B101"
model_type = 'skt/kobert-base-v1'
text = """
최근 R&D 센터장으로 보직을 옮겼던 김성용(53) 전 SSG 랜더스 단장이 팀을 완전히 떠난다.
29일 스타뉴스 취재 결과, 김성용 전 단장은 최근 구단에 자진 사퇴 의사를 밝힌 것으로 알려졌다. 
프랜차이즈 스타 김강민(41)의 한화 이글스 이적을 비롯한 이번 오프시즌 일어난 일련의 사태에 책임을 지겠다는 의미다.
SSG는 올해 NC 다이노스와 준플레이오프에서 3전 전패로 탈락한 후 팀을 재편하는 과정에서 적지 않은 잡음이 일었다. 
세대교체의 필요성을 이유로 지난해 정규시즌 와이어 투 와이어(시즌 시작부터 종료까지 1위를 놓치지 않음) 우승과 한국시리즈 제패를 이끈 김원형(51) 감독을 재계약 1년 만에 교체했다.
당시 SSG는 "지속해서 발전하는 팀을 위해서는 변화와 혁신이 필요하다고 봤다. 늦는 것보다는 좀더 빠르게 결정하는 게 낫다고 판단해 단행했다. 
처음에는 선수단 구성, 세대교체, 팀 운영 및 경기 운영 전반에 선수 및 코칭스태프 구성으로 가닥을 잡았으나 감독 교체까지 진행하게 됐다"고 이유를 밝혔다.
새 사령탑 선임 과정에도 논란이 일었다. 
현장, 프런트, 해설위원 등 다양한 분야에서 차기 감독 후보를 추리는 도중에 이호준(47) LG 트윈스 코치를 비롯한 면접 대상자들이 포스트시즌 도중 노출됐다. 
더욱이 이 코치가 소속된 LG가 한국시리즈를 앞둔 상황이어서 논란은 커졌다. 결국 후보 중 하나였던 이숭용(52) 감독을 선임하며 일단락되는 듯했으나, 코칭스태프를 인선하는 과정에서 또 껄끄러운 상황이 벌어졌다.
보통 감독의 의중이 많이 반영되는 1군 코칭스태프와 달리 2군 코칭스태프는 구단이 원하는 방향에 따라 인선이 가능하다. 
김 전 단장은 미국에서 연수 중이던 손시헌(43) 전 NC 코치를 퓨처스팀 감독으로 낙점했다. 
문제는 손시헌 퓨처스팀 감독은 NC의 지원을 받아 미국 연수를 떠났고, 마치면 NC로 돌아갈 예정이었다는 점이다. 
하지만 연수가 끝나고 SSG로 팀을 옮기게 되면서 모양새가 이상하게 됐다. 
SSG 관계자에 따르면 결국 손 감독이 NC에 연수 지원금을 돌려주고 합류하면서 마무리됐으나, 애써 키운 지도자를 데려갔다는 비판은 피할 수 없었다.
결정타는 김강민의 KBO 2차 드래프트를 통한 한화 이적이었다. 
김강민은 2001년 신인드래프트 2차 2라운드 18순위로 SK 와이번스(현 SSG 랜더스)에 입단해 23년간 한 구단에서만 뛰어온 프랜차이즈 스타다. 
다섯 번의 한국시리즈 우승을 함께했고 가장 최근이던 지난해에는 결정적인 활약으로 한국시리즈 MVP에 오르기도 했다. 
하지만 올해는 70경기 타율 0.226, 2홈런 OPS 0.627로 성적이 저조했고 많은 나이까지 고려해 구단과 은퇴와 현역 연장을 두고 상의했다.
그러나 SSG는 2차 드래프트 보호 선수 35인 명단을 작성할 때까지 김강민과 은퇴와 관련해 결론을 내리지 못했다. 
은퇴 경기와 향후 진로에 대해 이야기를 나눈 것은 사실이었으나, 김강민은 현역 연장 의지가 더 강했다. 
확실하게 합의하지 못했다면 다른 구단에서 선택할 가능성을 염두에 두고 보호 선수 35인 명단을 짜야 했으나 어린 유망주를 한 명이라도 보호하는 것을 선택했다. 
그 과정에서 선수와 구단 내부의 소통이 충분하지 않았고 결국 김강민은 한화에 4라운드 지명을 받아 떠났다.
결국 SSG 구단은 지난 25일 "최근 감독 및 코치 인선과 2차 드래프트 과정에서 생긴 논란에 대한 책임을 물어 김성용 단장을 R&D센터(구 육성팀) 센터장으로 보직 변경한다"고 발표했다. 
SSG 내부 사정에 밝은 관계자에 따르면 김 전 단장은 팀에 부담을 준 것에 책임을 느끼고, 지난 28일 구단에 직접 사퇴 의사를 밝혔다.
김 전 단장은 24년간 야탑고등학교 야구부 감독을 역임한 현장 지도자 경험과 더불어 스포츠 과학에 대한 폭넓은 지식과 이해로 높은 평가를 받았다. 
2022시즌을 앞두고 R&D 센터장으로 부임해 지난해 12월 단장까지 올랐으나 2년 만에 SSG를 떠나게 됐다.
한편 SSG는 신임 단장은 내부가 아닌 외부 인사로 후보군을 물색하고 있는 것으로 알려졌다. 코치진 인선도 대부분 마쳐 조만간 공식 발표할 예정이다.
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
       keywords = keyBERT_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=stop_words, top_n=5)
       return keywords 

def textPreprocessing(text):
    kiwi = Kiwi()
    results = []
    result = kiwi.analyze(text)
    for token, pos, _, _ in result[0][0]:
        if len(token) != 1 and pos.startswith('NNP') or pos.startswith('SL'):
            results.append(token)
    results = ' '.join(results)
    return results



if __name__ == '__main__':
    kw_model = modelLoad(model_type)
    keywords = keywordExtract(kw_model, textPreprocessing(text))
    print(keywords)