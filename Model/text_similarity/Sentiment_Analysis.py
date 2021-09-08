#%%
#konlpy를 이용한 감성분석(로지스틱 회귀0) 책 참조
from os import name, sep
from nltk import tokenize
from nltk.corpus.reader import twitter
import pandas as pd
import numpy as np


from konlpy.tag import Okt
from konlpy.tag import Twitter
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.utils import shuffle
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from hanspell import spell_checker

from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import SGDClassifier
from sklearn.utils.fixes import loguniform

class Sentiment_Analysis:
    def __init__(self):
        self.data_x, self.data_y = self.load_data()   
        self.sgd = SGDClassifier(loss='log', random_state=1)
        self.param_dist = {'alpha': loguniform(0.0001, 100.0)}
        self.rsv_okt = self.get_rsv()

    def start_train(self):
        self.data_x = self.data_x.values.astype('U')
        data_okt = self.vectorize(self.data_x)
        self.train_model(data_okt)
        self.get_score()

    def load_data(self):
        df = pd.read_csv("C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/lastlast.csv", encoding='cp949')

        train_x = df["리뷰"]
        train_y = df['레이블']

        return train_x, train_y

    def vectorize(self, data):
        okt = Okt()
        self.tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.9, tokenizer=okt.morphs, token_pattern=None)
        self.tfidf.fit(data)
        data_okt = self.tfidf.transform(data)
        
        return data_okt

    def train_model(self, data_okt):
        self.rsv_okt.fit(data_okt, self.data_y)

    def get_rsv(self):
        rsv_okt = RandomizedSearchCV(estimator=self.sgd, param_distributions=self.param_dist, n_iter=50, random_state=1, verbose=1)

        return rsv_okt

    def get_score(self):
        print('최상 점수')
        print(self.rsv_okt.best_score_)

        print('최상 매개변수 값')
        print(self.rsv_okt.best_params_)

    def start_test(self, test_review):
        self.review = [test_review]

        review_okt = self.tfidf.transform(self.review)
        score = self.rsv_okt.best_estimator_.predict(review_okt)

        if score >=0:
            result = '긍정 리뷰'
        elif score == -1:
            result = '부정 리뷰'
        elif score == -2:
            result = '악성 리뷰'

        return result
# %%
