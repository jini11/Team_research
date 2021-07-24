package crawler_selenium;

public class Main {
    static int review_total=50;
    public static void main(String[] args) throws Exception {
 
		Crawler crawl = new Crawler();
		crawl.open();
		
		
		//element = driver.findElement(By.xpath("//*[@id=\"content\"]/div[2]/div[1]/ul/li[2]/a/span"));
		//review_total= Integer.parseInt(element.getText());
		int review_count = review_total/10;
		System.out.println(review_count); //더보기 버튼 클릭할 횟수
		
		for(int i=0;i<review_count;i++) {		
			crawl.scroll_down();
			crawl.click_more();
		}

        //정보 수집
		crawl.collect_data();
        
		crawl.close();
    }
}
