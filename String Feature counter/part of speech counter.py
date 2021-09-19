#!/usr/bin/env python
# coding: utf-8

# In[1]:


from konlpy.tag import Komoran
import pandas as pd
from pandas import DataFrame


# In[2]:


reviewText = input("리뷰를 입력하시오 : ")


# In[3]:


Komoran = Komoran()

nlpData = Komoran.pos(reviewText)


# In[4]:


rawData = pd.DataFrame(nlpData)

rawData.columns = ["words", "PSC"]

counterList = rawData['PSC']

# print(counterList)


# In[5]:


a, b = (0, 0)

targetA = ['NNG', 'NNP', 'NNB', 'VA','JKS', 'JKC', 'JKG','JKO','JKB','JKV','JKQ','JX','JC','MM']
targetB = ['VV', 'MAG', 'MAJ', 'NP', 'NR']

for index in counterList:
    if index in targetA:
        a+=1
    elif index in targetB:
        b+=1


# In[12]:


total = len(rawData)

targetApercent = (a/total)*100
targetBpercent = (b/total)*100

# print(targetApercent)
# print(targetBpercent)

