
from os import name, sep
import pandas as pd
import numpy as np


from konlpy.tag import Okt
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다', '요']

dataset = pd.read_csv('C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/dataset.csv')


#리뷰와 레이블만 불러와 review_dataset에 저장
review_dataset = dataset.iloc[:,[5,]]

print('전처리 전 리뷰 개수:',len(dataset))