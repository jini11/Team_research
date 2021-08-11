from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
import re

corpus = [
    '푸짐하게 잘 먹었습니다.'
    '콩국수 꼽빼기 2개는 양도 맛도 별로임 꽁국수 메뉴추가는 패착인듯'
    '김밥이 맛있습니다요'
]

vect = CountVectorizer();

document_term_matrix = vect.fit_transform(corpus)

tf = pd.DataFrame(document_term_matrix.toarray(), colums = vect.get_feature_names())

D = len(tf)

df = tf.astype(bool).sum(axis = 0)
idf = np.log(D+1 / (df+1) + 1)

tfidf = tf * idf

tfidf = tfidf / np.linalg.norm(tfidf, axis = 1, keepdims = True)

count = CountVectorizer()
docs = np.array([
        'The sun is shining',
        'The weather is sweet',
        'The sun is shining, the weather is sweet, and one and one is two'])
bag = count.fit_transform(corpus)

def preprocessor(corpus):
    text = re.sub('<[^>]*>', '', corpust)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',
                           corpus)
   corpus = (re.sub('[\W]+', ' ', corpus.lower()) +
            ' '.join(emoticons).replace('-', ''))
    return corpus