from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

class Text_Similarity:
    def __init__(self):
        self.ab_reviews = self.load_data()
        self.matrix = self.tfidf(self.ab_reviews)
    
    #def load_data(self):
    def load_data(self):
        df = pd.read_csv('C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/after_negative(-2).txt', sep='\n', encoding='utf-8')

        reviews = df['리뷰']
        reviews = np.array(reviews)
        print(type(reviews))
        print(reviews)

        return reviews

    def tfidf(self,reviews):
        twitter = Twitter()

        tfidf = TfidfVectorizer(min_df=1, tokenizer=twitter.morphs, token_pattern=None)

        tfidf_matrix = tfidf.fit_transform(reviews)
        #print(tfidf_matrix)

        #document_distance = (tfidf_matrix * tfidf_matrix.T)

        #print('유사도 분석을 위한 '+str(document_distance.get_shape()[0])+' x '+str(document_distance.get_shape()[1]))

        #코사인 유사도?
        #print(document_distance.toarray())

        
        return tfidf_matrix
    
    def get_result(self, review):
       
        review = np.append(self.ab_reviews, np.array(review))
        print(review)
        print(type(self.tfidf(review)))
        print(type(self.matrix))
        #tfidf_matrix = [self.tfidf(review)].extend([self.matrix])
       # tfidf_matrix = np.array(self.tfidf(review),self.matrix)

        review_tfidf = self.tfidf(review)
       # sum_matrix = np.concatenate((review_tfidf, self.matrix))
        
        print(review_tfidf)
        #vect1 = np.array(tfidf_matrix).reshape(-1,)
        #print(vect1)
        #max = 0
        #print(self.matrix)
        #for vect in range(0,61):
        #    vect2 = np.array(self.matrix[vect]).reshape(-1,)
        #    print(vect2)
        #    similarity = self.cos_similarity(vect1, vect2)
        #    if max < similarity:
        #        max = similarity
        #document_distance = (tfidf_matrix * tfidf_matrix)
        print(type(review_tfidf))
        similarity = cosine_similarity(review_tfidf, review_tfidf)
        print(similarity)
        
        max = 0.0
        print(similarity.shape)
        print(len(similarity))
        for num in range(0,len(similarity)-1):
            if max < similarity[len(similarity)-1][num]:
                max = similarity[len(similarity)-1][num]  

        print('최대 유사도: {0:.3f}'.format(max))
        return max

    def cos_similarity(self, v1, v2):
        dot_product = np.dot(v1, v2)
        norm = (np.sqrt(sum(np.square(v1))) * np.sqrt(sum(np.square(v2))))
        similarity = dot_product / norm
        
        return similarity

# 어뷰징 리뷰들 가져오기
# 어뷰징 리뷰들 벡터화
# 입력받은 리뷰 벡터화해서 어뷰징 리뷰들과 텍스트 유사도 분석
# 텍스트 유사도 중 가장 큰 것이 최종 텍스트 유사도
# 텍스트 유사도가 0.5 넘으면 어뷰징 리뷰