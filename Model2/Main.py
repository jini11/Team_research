from typing import final
from Text_Similarity import Text_Similarity
from Sentiment_Analysis import Sentiment_Analysis
from Preprocess import Preporcess
from Part_of_Speech import pscCounter
class Main():
    def main():
        sentiment = Sentiment_Analysis()
        sentiment.start_train()

        speech = pscCounter()

        preprocess = Preporcess()
        similarity = Text_Similarity()
        print("어뷰징 리뷰를 판별하는 프로그램입니다.(종료시 0 입력)")
        while(1):
            review = input('리뷰를 입력하세요: ')
            
            if review == '0':
                break

            star = input('별점을 입력하세요: ')
            
            #데이터 전처리(띄어쓰기, 맞춤법, 자모음 삭제)
            review = preprocess.spacing(review)
            review = preprocess.dele(review)

            
            #감성분석 실시해 세부적으로 어뷰징 리뷰 분류
            sen_score, result = sentiment.start_test(review)
        
            speech_score, speech_result = speech.counter(review)

            #감성분석, 품사 결과 비교
            if(sen_score == speech_score):
                final_score = 80.0 + speech_result
            else:
                final_score = 80.0 - speech_result

            #별점 테러, 별점과 리뷰의 불일치
            if (result == '정상 리뷰') and (star == '1' or star == '2'):
                result = '어뷰징 리뷰'
            elif (result =='악성 리뷰') and (star == '4' or star == '5'):
                result = '어뷰징 리뷰'
            elif result == '악성 리뷰':
                result = '어뷰징 리뷰'
            #else:
            #    result = '정상 리뷰'

            print('이 리뷰는 약 {0:.2f}%로 {1}로 예상됩니다.'.format(final_score, result))
            

    if __name__=="__main__": 
        main()


    
    