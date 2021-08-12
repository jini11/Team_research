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

df = pd.read_csv("C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/맞춤법 정리(리뷰, 레이블).csv", encoding='cp949')

train_x, test_x, train_y, test_y = train_test_split(df["리뷰"],df["긍/부정"], test_size=0.3, random_state=0)

print(len(train_x), len(train_y))

print(len(test_x), len(test_y))


okt = Okt()
print(train_x[4])
print(okt.morphs(train_x[4]))

tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.9, tokenizer=okt.morphs, token_pattern=None)
tfidf.fit(train_x)
train_x_okt = tfidf.transform(train_x)
test_x_okt = tfidf.transform(test_x.values.astype('U'))

#svm
#sgd = SGDClassifier(loss='hinge', random_state=1)

#logistic
sgd = SGDClassifier(loss='log', random_state=1)
param_dist = {'alpha': loguniform(0.0001, 100.0)}

rsv_okt = RandomizedSearchCV(estimator=sgd, param_distributions=param_dist, n_iter=50, random_state=1, verbose=1)
rsv_okt.fit(train_x_okt, train_y)

print('최상 점수')
print(rsv_okt.best_score_)

print('최상 매개변수 값')
print(rsv_okt.best_params_)

print('test 점수')
print(rsv_okt.score(test_x_okt,test_y))
score = rsv_okt.best_estimator_.predict(test_x_okt)

#f = open('C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/result_svm.txt',mode='w', encoding='utf-8' )


#for review, score in zip(test_x,score):
#    f.write("{} {}\n".format(review,score))
#    print(review, score, end='\n')

#f.close
# %%
