#%%

from os import name, sep
import matplotlib
from nltk import metrics, tokenize
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score


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

#elbow curve
#distortions = []
#vector = pd.DataFrame(vector)
#for k in range(20, 40):
#    kmeans = KMeans(n_clusters=k)
#    kmeans.fit(vector)
#    distortions.append(kmeans.inertia_)

#fig = plt.figure(figsize=(20, 10))
#plt.plot(range(20, 40), distortions)
#plt.grid(True)
#plt.title('Elbow curve')
#plt.show()

pca = PCA(n_components=2)
vector = pca.fit_transform(vector)
vector.shape


model = KMeans(n_clusters=5, init='k-means++')

vector = pd.DataFrame(vector)

cluster = model.fit(vector)

cluster_id = pd.DataFrame(cluster.labels_)


d1 = pd.DataFrame()
d1 = pd.concat([vector, cluster_id], axis=1)
d1.columns = [0,1,"cluster"]


#시각화
sns.scatterplot(d1[0], d1[1], hue=d1['cluster'], style=d1['cluster'], legend="full")
sns.scatterplot(model.cluster_centers_[:,0], model.cluster_centers_[:,1], label = 'Centroids')
plt.title('KMeans Clustering')
plt.legend()
plt.show()

print('Silhouette Coefficient: {:.4f}'.format(silhouette_score(d1.iloc[:,:-1], d1['cluster'])))
print('Davies Bouldin Index: {:.4f}'.format(davies_bouldin_score(d1.iloc[:,:-1], d1['cluster'])))

plt.clf()
plt.close()


df['result'] = cluster_id

cluster_id = np.array(cluster_id).flatten().tolist()


f = open('C:/Users/User/OneDrive - 공주대학교/바탕 화면/review/result_kmeans_ver1.txt',mode='w', encoding='utf-8' )

for cluster_num in set(cluster_id):
    f.write("cluster num : {} \n".format(cluster_num))
    temp_df = df[df['result'] == cluster_num]
    for review in temp_df['리뷰']:
        f.write("{}".format(review))
        f.write('\n')

f.close