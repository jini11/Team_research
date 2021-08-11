#%%
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


df = pd.read_csv("C://Users//User//OneDrive - 공주대학교//바탕 화면//review//only_review_score.csv")

train_x, test_x, train_y, test_y = train_test_split(df["리뷰"],df["긍/부정"], test_size=0.3, random_state=0)

print(len(train_x), len(train_y))

print(len(test_x), len(test_y))


twitter = Twitter()

tfv = TfidfVectorizer(tokenizer=twitter.morphs, ngram_range=(1,2), min_df=3, max_df=0.9)
tfv.fit(train_x)

tfv_train_x = tfv.transform(train_x)
print(tfv_train_x)


clf = LogisticRegression(random_state=0)
params = {"C":[1,3,5,7,9]}
grid_cv = GridSearchCV(clf, param_grid=params, cv= 4, scoring='accuracy', verbose=1)
grid_cv.fit(tfv_train_x, train_y)

GridSearchCV(cv=4, error_score=np.nan,
             estimator=LogisticRegression(C=1.0, class_weight=None, dual=False,
                                          fit_intercept=True,
                                          intercept_scaling=1, l1_ratio=None,
                                          max_iter=100, multi_class='auto',
                                          n_jobs=None, penalty='l2',
                                          random_state=0, solver='lbfgs',
                                          tol=0.0001, verbose=0,
                                          warm_start=False),
              n_jobs=None, param_grid={'C': [1, 3, 5, 7, 9]},
             pre_dispatch='2*n_jobs', refit=True, return_train_score=False,
             scoring='accuracy', verbose=1)

tfv_test_x = tfv.transform(test_x)

print(grid_cv.best_estimator_.score(tfv_test_x, test_y))
score = grid_cv.best_estimator_.predict(tfv_test_x)


f = open('C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/result(po,na).txt',mode='w', encoding='utf-8' )


for review, score in zip(test_x,score):
    f.write("{} {}\n".format(review,score))
    print(review, score, end='\n')





f.close