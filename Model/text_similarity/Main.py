from Text_Similarity import Text_Similarity
from Sentiment_Analysis import Sentiment_Analysis
from Preprocess import Preporcess

class Main():
    def main():
        sentiment = Sentiment_Analysis()
        sentiment.start_train()

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

            print(review)

            result = sentiment.start_test(review)
            
            #별점 테러, 별점과 리뷰의 불일치
            if (result == '긍정 리뷰') and (star == '1' or star == '2'):
                result = '악성 리뷰'
            elif (result =='부정 리뷰') and (star == '4' or star == '5'):
                result = '악성 리뷰'
            elif (result == '부정 리뷰' or result == '악성 리뷰') and review.find('배달'):
                result = '악성 리뷰'
            elif result == '악성 리뷰':
                result = '악성 리뷰'
            else:
                result = '정상 리뷰'

            score = similarity.get_result(review)
            print("최종 유사도: {0:.3f}".format(score))
            print(result)

    if __name__=="__main__": 
        main()


    
    