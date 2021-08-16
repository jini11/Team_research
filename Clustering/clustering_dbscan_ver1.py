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

from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import SGDClassifier
from sklearn.utils.fixes import loguniform



df = pd.read_csv("C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/맞춤법 정리(리뷰, 레이블).csv", encoding='cp949')

train_x = df['리뷰']
#train_x, test_x, train_y, test_y = train_test_split(df["리뷰"],df["긍/부정"], test_size=0.3, random_state=10)

#print(len(train_x), len(train_y))

#print(len(test_x), len(test_y))


okt = Okt()
print(train_x[4])
print(okt.morphs(train_x[4]))

tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=10, max_df=0.9, tokenizer=okt.morphs, token_pattern=None)
tfidf.fit(train_x.values.astype('U'))
train_x_okt = tfidf.transform(train_x.values.astype('U'))
#test_x_okt = tfidf.transform(test_x.values.astype('U'))
vector = tfidf.transform(train_x.values.astype('U')).toarray()

vector = np.array(vector)
model = DBSCAN(eps=0.5, min_samples=3, metric="cosine")

result = model.fit_predict(vector)
#result = pd.DataFrame(model.fit_predict(vector))
#vector = pd.DataFrame(vector)
print(len(vector))
print(len(result))
#vector.columns = ['vector']
#result.columns = ['result']
print(result)

print(vector)

df['result'] = result


f = open('C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/result_dbscan.txt',mode='w', encoding='utf-8' )

for cluster_num in set(result):
    f.write("cluster num : {} \n".format(cluster_num))
    temp_df = df[df['result'] == cluster_num]
    for review in temp_df['리뷰']:
        f.write("{}".format(review))
        f.write('\n')

f.close

result = pd.DataFrame(model.fit_predict(vector))
vector = pd.DataFrame(vector)


#vector.columns = ['vector']
result.columns = ['result']

r = pd.concat([vector, result],axis=1)


#pairplot with Seaborn

sns.pairplot(r, hue = 'result')
plt.show()
plt.show(sns)

plt.clf()
plt.close()


# %%
