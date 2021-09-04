from Sentiment_Analysis import Sentiment_Analysis


class Main():
    def main():
        sentiment = Sentiment_Analysis()
        sentiment.start_train()

        print("어뷰징 리뷰를 판별하는 프로그램입니다.")
        review = input('리뷰를 입력하세요: ')
        star = input('별점을 입력하세요: ')

        result = sentiment.start_test(review)

        print(result)

    if __name__=="__main__": 
        main()


    
    