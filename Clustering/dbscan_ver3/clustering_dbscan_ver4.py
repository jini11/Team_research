#umap으로 차원 축소

#%%

from inspect import EndOfBlock
from os import name, sep
import matplotlib
from nltk import tokenize
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from umap import UMAP
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.manifold import TSNE




df = pd.read_csv("C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/맞춤법 정리(리뷰, 레이블).csv", encoding='cp949')

train_x = df['리뷰']


okt = Okt()
print(train_x[4])
print(okt.morphs(train_x[4]))

#tf-idf
tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=5, max_df=0.9, tokenizer=okt.morphs, token_pattern=None)
tfidf.fit(train_x.values.astype('U'))
train_x_okt = tfidf.transform(train_x.values.astype('U'))
vector = tfidf.transform(train_x.values.astype('U')).toarray()


#차원 축소(UMAP)

plt.figure(figsize=(20,15))
model = UMAP(n_neighbors=10, min_dist= 0.25, n_components= 2, verbose= True)
umap = model.fit_transform(vector)
plt.scatter(umap[:,0], umap[:,1], cmap = 'tab10', s=50)
plt.show()

#tsne_df = pd.DataFrame({'x': tsne[:,0], 'y': tsne[:,1], 'classes':df['긍/부정']})

#plt.figure(figsize=(16,10))
#sns.scatterplot(
#    x='x', y='y',
#    hue= 'classes',
#    data = tsne_df,
#    legend= "full",
#    alpha =0.4
#)

#plt.title("tSNE")
#plt.show()

vector = umap
vector.shape


#DBSCAN
model = DBSCAN(eps=0.5, min_samples=4)

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


plt.clf()
plt.close()

print('Silhouette Coefficient: {:.4f}'.format(silhouette_score(d2.iloc[:,:-1], d2['cluster'])))
print('Davies Bouldin Index: {:.4f}'.format(davies_bouldin_score(d2.iloc[:,:-1], d2['cluster'])))

df['result'] = result_id

result_id = np.array(result_id).flatten().tolist()


f = open('C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/result_dbscan_ver3.txt',mode='w', encoding='utf-8' )

for cluster_num in set(result_id):
    f.write("cluster num : {} \n".format(cluster_num))
    temp_df = df[df['result'] == cluster_num]
    for review in temp_df['리뷰']:
        f.write("{}".format(review))
        f.write('\n')

f.close
# %%
