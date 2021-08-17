#%%

from os import name, sep
import matplotlib
from nltk import tokenize
from nltk.corpus.reader import twitter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from konlpy.tag import Okt
from konlpy.tag import Twitter
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.utils import shuffle
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.cluster import DBSCAN
from hanspell import spell_checker
from sklearn.decomposition import PCA

from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import SGDClassifier
from sklearn.utils.fixes import loguniform



df = pd.read_csv("C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/맞춤법 정리(리뷰, 레이블).csv", encoding='cp949')

train_x = df['리뷰']


okt = Okt()
print(train_x[4])
print(okt.morphs(train_x[4]))

#tf-idf
tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=10, max_df=0.9, tokenizer=okt.morphs, token_pattern=None)
tfidf.fit(train_x.values.astype('U'))
train_x_okt = tfidf.transform(train_x.values.astype('U'))
vector = tfidf.transform(train_x.values.astype('U')).toarray()


#차원 축소
pca = PCA(n_components=2)
vector = pca.fit_transform(vector)
vector.shape

#DBSCAN
model = DBSCAN(eps=0.03, min_samples=4)

vector = pd.DataFrame(vector)

result = model.fit(vector)

result_id = pd.DataFrame(result.labels_)

d2 = pd.DataFrame()
d2 = pd.concat([vector, result_id], axis=1)
d2.columns = [0,1,"cluster"]

#시각화
sns.scatterplot(d2[0], d2[1], hue=d2['cluster'], style=d2['cluster'], legend="full")
plt.title('DBSCAN')
plt.show()


result = pd.DataFrame(model.fit_predict(vector))
vector = pd.DataFrame(vector)



plt.clf()
plt.close()


# %%
