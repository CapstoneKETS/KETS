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

stop_words = ['지난해', '올해', '시즌', '향후', '한국', 'kbo', '야구']
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
