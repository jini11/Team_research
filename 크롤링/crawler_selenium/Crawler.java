package crawler_selenium;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;


//    1. selenium을 다운받은 후, 개발툴(eclipse, vsc 등)에 포함시켜 주기
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class Crawler {

	private static final char UTF_8_WITHOUT_BOM = '\ufeff';

	// WebDriver
	static private WebDriver driver;
	static private WebElement element;
	private String url;

	// Properties
	public static String WEB_DRIVER_ID = "webdriver.chrome.driver";
	public static String WEB_DRIVER_PATH = "C:/selenium/chromedriver.exe";   //  2. chromedriver를 다운받은 후 큰따옴표 사이의 위치를 바꿔주기

	// 총 리뷰 수
	static int review_total = 0;
	//음식점 넘버
	static int number = 279652;
	//230730, 289809, 245326, 485145, 406759, 396589, 522576, 249966, 513830, 508349, 246868, 486637, 279652
	public static HashMap<String, Object> map = new HashMap<>();

	public static ArrayList<String> id = new ArrayList<>();
	public static ArrayList<String> time = new ArrayList<>();
	public static ArrayList<String> score = new ArrayList<>();
	public static ArrayList<String> picture = new ArrayList<>();
	public static ArrayList<String> menu = new ArrayList<>();
	public static ArrayList<String> reviews = new ArrayList<>();

	public Crawler() {
		// System Property SetUp
		System.setProperty(WEB_DRIVER_ID, WEB_DRIVER_PATH);

		// Driver SetUp
		ChromeOptions options = new ChromeOptions();
		options.setCapability("ignoreProtectedModeSettings", true);
		driver = new ChromeDriver(options);

		// 음식점마다 url 바꿔주기
		url = "https://www.yogiyo.co.kr/mobile/#/"+(number++)+"/";  //      3. 요기요에서 본인이 크롤링하고 싶은 음식점 들어가서 주소 복붙하기

	}

	public void open() {
		try {
			// get방식으로 url 요청
			driver.get(url);

			// 홈페이지가 잘 열렸는지 확인
			check_open();
			
			// 클린리뷰 버튼 클릭
			new WebDriverWait(driver, 20).until(ExpectedConditions.elementToBeClickable(By.xpath("//*[@id=\"content\"]/div[2]/div[1]/ul/li[2]/a"))).click();

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	// 홈페이지 잘 열렸는지 확인
	public boolean check_open(){
		if(driver.getCurrentUrl().equals("https://www.yogiyo.co.kr/mobile/#/")){
			number++;
			return false;
		}
		else
			return true;
	}

	// 창 닫기
	public void close(){
		driver.close();
	}

	// scroll 내리기
	public void scroll_down() {
		JavascriptExecutor js = (JavascriptExecutor) driver;
		js.executeScript("window.scrollTo(0, document.body.scrollHeight);");
	}

	// 더보기 버튼 클릭하기
	public void click_more() throws InterruptedException {
		element = driver.findElement(By.className("btn-more"));
		element.click();

		Thread.sleep(2);

	}

	// 총 리뷰 개수 불러오기
	public int get_reviewnum() {
		element = driver.findElement(By.xpath("//*[@id=\"content\"]/div[2]/div[1]/ul/li[2]/a/span"));

		return Integer.parseInt(element.getText());
	}

	// 데이터 수집
	public void collect_data() throws IOException {

		List<WebElement> id_element = driver.findElements(By.cssSelector("#review li > div > span.review-id"));
		List<WebElement> time_element = driver.findElements(By.cssSelector("#review li > div > span.review-time"));
		List<WebElement> score_element = driver.findElements(By.cssSelector("#review li > div > div > span.total"));
		List<WebElement> picture_element = driver.findElements(By.cssSelector("#review li"));
		List<WebElement> menu_element = driver.findElements(By.cssSelector("#review li > div.order-items"));
		List<WebElement> reviews_element = driver.findElements(By.cssSelector("#review li > p"));

		//id
		for(int i=0;i<id_element.size();i++){
			String text = ((WebElement) id_element.get(i)).getText();

			if(text.contains("손님"))
				text = text.replaceAll("손님", "");
			else if(text.contains("님"))
				text = text.replaceAll("님", "");

			id.add(text);
		}

		//time
		for(int i=0;i<time_element.size();i++){
			String text = ((WebElement) time_element.get(i)).getText();
			Calendar cal = Calendar.getInstance();
			cal.setTime(new Date());
			DateFormat df = new SimpleDateFormat("yyyy년 MM월 dd일");

			if(text.contains("전")){
				if(text.contains("일")){
					if(text.contains("일주일")){
						cal.add(Calendar.DATE,-7);
						text = df.format(cal.getTime());
					}
					else {
						cal.add(Calendar.DATE,-Integer.parseInt(text.split("일")[0]));
						text = df.format(cal.getTime());
					}
				}
				else {
					text = df.format(cal.getTime());
				}
			}
			else if(text.contains("어제")){
				cal.add(Calendar.DATE,-1);
				text = df.format(cal.getTime());
			}

			time.add(text);
		}
		//시간 전처리
		//ex) 23시간 전, 2일 전, 일주일 전
		// "전" 들어간 text 가져와서 
		// 1. "일"이 포함되어 있으면 오늘 날짜-2 
		// 2. 1에서 "일주일"이 포함되어 있으면 오늘날짜-7일
		// 3. "시간"이 포함되어 있으면 오늘 날짜로 replaceAll
		// ++ "어제"

		// 별점 계산하고 별도로 score(Arraylist)에 add
		for (int i = 0; i < score_element.size(); i++) {
			int star = 0;
			String source = ((WebElement) score_element.get(i)).getAttribute("innerHTML");
			int len = 0;

			if (source.contains("full")) {
				for (int j = 0; j < source.length(); j++) {
					len = source.split("full").length;

				}
				star = len - 1;
			}
			score.add(Integer.toString(star));
		}

		// 사진 유무 판별, picture(ArrayList)에 저장
		for (int i = 1; i < picture_element.size(); i++) {
			String source = ((WebElement) picture_element.get(i)).getAttribute("innerHTML");

			if (source.contains("table"))
				source = "yes";
			else
				source = "no";

			picture.add(source);
			
		}

		// menu에서 , 기호를 +로 대체(,를 기준으로 셀이 분리되기 때문)
		for(int i=0;i<menu_element.size();i++){
			String text = ((WebElement) menu_element.get(i)).getText();
			
			if(text.contains(","))
				text = text.replaceAll(",","+");
			
			menu.add(text);
		}

		// reviews에서 , 기호 제거
		for(int i=1;i<reviews_element.size();i++){
			String text = ((WebElement) reviews_element.get(i)).getText();

			if(text.contains(","))
				text = text.replaceAll(",", "");

			reviews.add(text);
		}

				
		map.put("ID", id);
		map.put("TIME", time);
		map.put("SCORE", score);
		map.put("PICTURE", picture);
		map.put("MENU", menu);
		map.put("REVIEWS", reviews);

		System.out.println("데이터 수집 완료");
		
		save_data();

	}

	// 데이터 csv형태로 저장
	public void save_data() throws IOException {

		// 파일 경로 각자 설정하기

		String filepath = "C://Users//User//OneDrive - 공주대학교//바탕 화면//review//";       //   4. csv 파일 저장할 위치 설정해주기
		String title = "yogiyo_review";       //  5. csv 파일 이름 적는 곳(바꿔도 되고 안 바꿔도 됨)

		BufferedWriter fw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(filepath+title + ".csv",true)));
		// BufferedWriter로 이용해 파일 생성

		for (int i = 0; i < id.size(); i++) {
			fw.write(id.get(i) + ",");              //arraylist(id)에서 get으로 값을 가져와 write 메소드를 이용해 값을 파일에 입력, ","로 셀 분리
			fw.write(time.get(i) + ",");
			fw.write(score.get(i) + ",");
			fw.write(picture.get(i) + ",");
			fw.write(menu.get(i) + ",");
			fw.write(reviews.get(i));
			fw.newLine();  //엔터
		}

		fw.flush();   //출력 버퍼 비우기

 		fw.close();		//닫기
 		System.out.println("저장 완료");

		// apche poi를 사용한 파일 저장(작동 안됨..)
		/*
		 * File file=new File("yogiyo.xlsx"); FileOutputStream fileout=new
		 * FileOutputStream(file);
		 * 
		 * XSSFWorkbook xworkbook=new XSSFWorkbook();
		 * 
		 * XSSFSheet xsheet=xworkbook.createSheet("요기요"); XSSFRow curRow;
		 * 
		 * int row=element.size(); Cell cell=null;
		 * 
		 * //title curRow=xsheet.createRow(0); cell=curRow.createCell(0);
		 * cell.setCellValue("요기요 리뷰");
		 * 
		 * //head curRow=xsheet.createRow(1); cell=curRow.createCell(0);
		 * cell.setCellValue("유저ID");
		 * 
		 * cell=curRow.createCell(1); cell.setCellValue("시간");
		 * 
		 * cell=curRow.createCell(2); cell.setCellValue("신고");
		 * 
		 * cell=curRow.createCell(3); cell.setCellValue("별점");
		 * 
		 * cell=curRow.createCell(4); cell.setCellValue("리뷰");
		 * 
		 * cell=curRow.createCell(5); cell.setCellValue("신고");
		 * 
		 * //body for(int i=2;i<row;i++){ curRow=xsheet.createRow(1);
		 * 
		 * cell=curRow.createCell(0); cell.setCellValue(element.get(i).getText());
		 * 
		 * 
		 * 
		 * }
		 * 
		 * for(int i=0;i<3;i++){ xsheet.autoSizeColumn(i); xsheet.setColumnWidth(i,
		 * (xsheet.getColumnWidth(i))+256); }
		 */
	}
}
