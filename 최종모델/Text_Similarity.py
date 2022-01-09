from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from konlpy.tag import Okt

import pandas as pd
import numpy as np

class Text_Similarity:
    def __init__(self):
        self.ab_reviews = self.load_data()
        self.matrix = self.tfidf(self.ab_reviews)
    
    def load_data(self):
        df = pd.read_csv('C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/after_negative(-2).txt', sep='\n', encoding='utf-8')

        reviews = df['리뷰']
        reviews = np.array(reviews)
       
        return reviews

    def tfidf(self,reviews):
        twitter = Twitter()
        okt = Okt()
        
        for i, document in enumerate(reviews):
            clean_words = []
            for word in okt.pos(document, stem=True): #어간 추출
                if word[1] in ['Noun', 'Verb', 'Adjective']: #명사, 동사, 형용사
                    clean_words.append(word[0])
            document = ' '.join(clean_words)
            reviews[i] = document
       
        tfidf = TfidfVectorizer(min_df=1, tokenizer= okt.morphs, token_pattern=None)

        tfidf_matrix = tfidf.fit_transform(reviews)
      
        return tfidf_matrix
    
    def get_result(self, review):
       
        review = np.append(self.ab_reviews, np.array(review))
     
        review_tfidf = self.tfidf(review)
      
        similarity = cosine_similarity(review_tfidf, review_tfidf)
      
        max = -2

        for num in range(0,len(similarity)-1):
            if max < similarity[len(similarity)-1][num]:
                max = similarity[len(similarity)-1][num]  

        return max

# 어뷰징 리뷰들 가져오기
# 어뷰징 리뷰들 벡터화
# 입력받은 리뷰 벡터화해서 어뷰징 리뷰들과 텍스트 유사도 분석
# 텍스트 유사도 중 가장 큰 것이 최종 텍스트 유사도
# 텍스트 유사도가 0.3 넘으면 어뷰징 리뷰