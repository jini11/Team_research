#%%
from os import name, sep
from nltk import tokenize
import pandas as pd
import numpy as np


from konlpy.tag import Okt
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from hanspell import spell_checker

stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다', '요']

dataset = pd.read_csv('C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/dataset.csv')


#리뷰와 레이블만 불러와 review_dataset에 저장
review_dataset = dataset.iloc[:,[5]]

print('전처리 전 리뷰 개수:',len(dataset))

#데이터셋의 긍/부정 레이블 개수 출력 및 시각화
print(dataset['긍/부정'].value_counts().plot(kind='bar'))
print(dataset.groupby('긍/부정').size().reset_index(name='count'))

#리뷰 띄어쓰기, 맞춤법 보정
checked = []
for sentence in dataset[:1000]['리뷰']:
    spelled_sent = spell_checker.check(sentence)
    checked.append(spelled_sent.checked)


#dataset['리뷰'] = dataset['리뷰'].str.replace('^ +', "") # 공백은 empty 값으로 변경
#dataset['리뷰'].replace('', np.nan, inplace=True) # 공백은 Null 값으로 변경
#dataset = dataset.dropna(how='any') # Null 값 제거
print('전처리  완료')


#토큰화
okt = Okt()
X_data = []
for sentence in checked:
    temp_X = okt.morphs(sentence,stem=True)
    temp_X = [word for word in temp_X if not word in stopwords]
    X_data.append(temp_X)

print(X_data[:10])

vect = TfidfVectorizer()
tdm = vect.fit_transform(checked)
word_count = pd.DataFrame({
    '단어':vect.get_feature_names(),
    '빈도':tdm.sum(axis=0).flat
})

print(word_count)
#x_train = dataset.loc[:]
#y_train = dataset.loc[:15620,'긍/부정'].values
#x_test = X_data[6694:]
#y_test = dataset.loc[6694:'긍/부정'].values

for i in range(50):
    print("리뷰: ",checked," tfidf: ",tdm)

X = tdm
Y = dataset[:1000]['긍/부정']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)


tfidf = TfidfVectorizer(lowercase=False, tokenizer=tokenize)
lr_tfidf = Pipeline([('vect', tfidf),('clf', LogisticRegression(C=10.0, penalty='l2', random_state=0))])
lr = LogisticRegression()
print('start')
#lr_tfidf.fit(Y_train)
lr.fit(X_train,Y_train)

#y_pred = lr_tfidf.predict(X_test)
y_pred = lr.predict(X_test)

print(Y_test)
print(y_pred)

print('정확도: %.3f' %accuracy_score(Y_test,y_pred))
#리뷰만 따로 불러와서 형태소 추출, tf-idf 적용
#tf-idf와 레이블을 같은 리스트에 넣고 train_test_split 해서 로지스틱에 넣고 학습



#1 내 방식대로 형태소 추출 "사이킷런 tf-idf 검색"
#2 result_full 가져와서 명, 동, 형만 추출