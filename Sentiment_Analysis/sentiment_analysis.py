from os import sep
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

dataset = pd.read_csv('C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/dataset.csv')

#리뷰와 레이블만 불러와 review_dataset에 저장
review_dataset = dataset.iloc[:,[5]]




#리뷰만 따로 불러와서 형태소 추출, tf-idf 적용
#tf-idf와 레이블을 같은 리스트에 넣고 train_test_split 해서 로지스틱에 넣고 학습

