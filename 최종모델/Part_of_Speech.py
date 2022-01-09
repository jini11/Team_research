from konlpy.tag import Komoran
import pandas as pd
from pandas import DataFrame

class pscCounter:
    def counter(self, review_text):
        
        komoran = Komoran()
        
        print(review_text)
        
        nlpData = komoran.pos(review_text)

        rawData = pd.DataFrame(nlpData)

        rawData.columns = ["words", "PSC"]

        counterList = rawData['PSC']

        targetA = ['NNG', 'NNP', 'NNB', 'VA','JKS', 'JKC', 'JKG','JKO','JKB','JKV','JKQ','JX','JC','MM']
        targetB = ['VV', 'MAG', 'MAJ', 'NP', 'NR']

        a, b = (0, 0)

        for index in counterList:
            if index in targetA:
                a+=1
            elif index in targetB:
                b+=1
        
        total = len(rawData)

        targetApercent = (a/total)*100
        targetBpercent = (b/total)*100

        if(targetApercent < targetBpercent):
            return 1, float(targetBpercent * 0.2)
        elif(targetBpercent < targetApercent):
            return 0, float(targetApercent * 0.2)
        else:
            return -1, 10.0