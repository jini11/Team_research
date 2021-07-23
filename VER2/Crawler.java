package VER2;

import java.util.ArrayList;
import java.util.List;

import org.jsoup.select.Elements;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

 
public class Crawler {
 
	//WebDriver
	static private WebDriver driver;
	static private WebElement element;
	private String url;
	
	//Properties
	public static String WEB_DRIVER_ID = "webdriver.chrome.driver";
	public static String WEB_DRIVER_PATH = "C:/selenium/chromedriver.exe";
	
	static int review_total=50;
	
	public static class Info {
		private static String userID;
		private static String date;
		private static String score;
		private static boolean picture;
		private static String menu;
		private static String review;
	}
	
	
	public Crawler() {
		//System Property SetUp
		System.setProperty(WEB_DRIVER_ID, WEB_DRIVER_PATH);
		
		//Driver SetUp
		ChromeOptions options = new ChromeOptions();
		options.setCapability("ignoreProtectedModeSettings", true);
		driver = new ChromeDriver(options);
		
		url = "https://www.yogiyo.co.kr/mobile/#/359890/";
		//url = "https://www.yogiyo.co.kr/mobile/#/%EC%B6%A9%EC%B2%AD%EB%82%A8%EB%8F%84/336850/";
		
		
	}
 
	public void open() {
		try {
			//get방식으로 url 요청
			driver.get(url);
			
			//로그인 버튼 클릭
			//element = driver.findElement(By.className("item clearfix"));
			//element.click();
			
			//클린리뷰 버튼 클릭
			new WebDriverWait(driver,20).until(ExpectedConditions.elementToBeClickable(By.xpath("//*[@id=\"content\"]/div[2]/div[1]/ul/li[2]/a"))).click();
			
			
			Thread.sleep(10000);
	
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			//driver.close();
		}
 
	}
	
	public void scroll_down() { //scroll 내리기
		JavascriptExecutor js=(JavascriptExecutor) driver;
		js.executeScript("window.scrollBy(0,3050)", "");
	}
	
	public void click_more() throws InterruptedException {
		element = driver.findElement(By.className("btn-more"));
		element.click();
		
		Thread.sleep(2);
		
	}
 
}
