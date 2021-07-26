package crawler_selenium;

public class Main {
    static int review_total=0; //초기화
	static int count=0; //실제 크롤링한 음식점 개수
	static int store=4; //크롤링할 음식점 개수
	static int review_sum=0;
    public static void main(String[] args) throws Exception {
		
		for(int k=0;k<store;k++){
		Crawler crawl = new Crawler();
		crawl.open();
		
		boolean correct=crawl.check_open();

		if(correct){
		review_total= crawl.get_reviewnum();
		review_sum+=(review_total-review_total%10);
		int review_count = review_total/10;
		
		
		for(int i=0;i<review_count;i++) {		
			crawl.scroll_down();
			crawl.click_more();
		}

        //정보 수집
		crawl.collect_data();
		count++;
		}

		crawl.close();
		
		}
	System.out.println("총 "+count+"개 음식점, 약 "+review_sum+"개 리뷰");
	}
}
