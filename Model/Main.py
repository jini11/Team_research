from Sentiment_Analysis import Sentiment_Analysis


class Main():
    def main():
        sentiment = Sentiment_Analysis()
        sentiment.start_train()

        print("어뷰징 리뷰를 판별하는 프로그램입니다.(종료시 0 입력)")
        while(1):
            review = input('리뷰를 입력하세요: ')
            
            if review == '0':
                break

            star = input('별점을 입력하세요: ')
            
            result = sentiment.start_test(review)
            
            #별점 테러, 별점과 리뷰의 불일치
            if (result == '긍정 리뷰') and (star == '1' or star == '2'):
                result = '허위 리뷰'
            elif (result =='부정 리뷰') and (star == '4' or star == '5'):
                result = '허위 리뷰'
            elif result == '부정 리뷰' and review.find('배달'):
                result = '허위 리뷰'
            else:
                result = '정상 리뷰'

            print(result)

    if __name__=="__main__": 
        main()


    
    