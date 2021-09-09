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

            #1차 분류: 텍스트 유사도 계산해서 0.3 이상이면 어뷰징 리뷰 판단 종료
            score = similarity.get_result(review)
            if score>=0.3:
                print('이 리뷰는 {0:2f}%로 어뷰징 리뷰로 의심됩니다.'.format(score*100))
            else:
                #2차 분류: 1차 분류에서 어뷰징 리뷰가 아닐 경우 감성분석 실시해 세부적으로 어뷰징 리뷰 분류
                result = sentiment.start_test(review)
            
                #별점 테러, 별점과 리뷰의 불일치
                if (result == '긍정 리뷰') and (star == '1' or star == '2'):
                    result = '어뷰징 리뷰'
                elif (result =='부정 리뷰') and (star == '4' or star == '5'):
                    result = '어뷰징 리뷰'
                elif (result == '부정 리뷰' or result == '악성 리뷰') and review.find('배달'):
                    result = '어뷰징 리뷰'
                elif result == '악성 리뷰':
                    result = '어뷰징 리뷰'
                else:
                    result = '정상 리뷰'

                print('이 리뷰는 '+result+"입니다.")

    if __name__=="__main__": 
        main()


    
    