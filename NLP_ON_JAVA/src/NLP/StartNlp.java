package NLP;

import kr.co.shineware.nlp.komoran.constant.DEFAULT_MODEL;
import kr.co.shineware.nlp.komoran.core.Komoran;
import kr.co.shineware.nlp.komoran.model.KomoranResult;

import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;

public class StartNlp {

	String FullReview;
	// 모든 리뷰 데이터를 저장

	public StartNlp() {
		// TODO Auto-generated constructor stub

		ReadReview();
	}

	@SuppressWarnings("resource")
	private void ReadReview() {
		// TODO Auto-generated method stub

		// 리뷰 데이터 불러오기

		try {

			FileInputStream fileStream = null;

			fileStream = new FileInputStream("./data/Review_Data.txt");

			byte readBuffer[] = new byte[fileStream.available()];

			while (fileStream.read(readBuffer) != -1) {
				FullReview += new String(readBuffer, "UTF-8");
				// 인코딩 에러를 방지하기 위하여 UTF-8 사용
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		doToken();

	}

	private void doToken() {
		// TODO Auto-generated method stub
		String[] splitReview = FullReview.split("/");
		// 이전 리뷰와 다음 리뷰를 '/'로 구분하고 합쳤으므로, 다시 분리

		int countindex = 1; // 리뷰 구분 시퀸서

		for (String i : splitReview) {
			NLP(i.replace("\\s+", ""), countindex);
			// 정규표현식을 사용하여 리뷰 데이터의 공백을 제거한 뒤, 리뷰 구분 시퀸서와 함께 NLP 에 전달
			countindex++;
		}
	}

	private void NLP(String str, int countindex) {
		// Komoran 을 활용한 형태소 분석
		Komoran komoran = new Komoran(DEFAULT_MODEL.LIGHT);
		// Default_Model 지정하여 형태소 분석

		// System.out.println(countindex+" "+str);

		KomoranResult analyzeResultList = komoran.analyze(str);
		// doToken 함수로 구분된 개별 리뷰를 형태소 분석기 라이브러리에 입력

		resultWrite(analyzeResultList, countindex, str);
	}

	private void resultWrite(KomoranResult analyzeResultList, int countindex, String str) {
		// TODO Auto-generated method stub

		BufferedWriter output = null;

		try {
			output = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("./data/result.csv", true)));

			//output.write((countindex + ",").replace("\n", ""));// 리뷰 시퀸서 입력 (1번 컬럼)
			output.write((str + ",").replace("\n", ""));// 리뷰 원문 입력 (2번 컬럼)
			output.write((analyzeResultList.getPlainText() + ",").replace("\n", ""));// 형태소 분석 입력(3번 컬럼)
			output.newLine();// 줄바꿈

			System.out.println(countindex); // 진행상황 출력

		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			System.out.println("output Fail");
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		try {
			output.flush();
			output.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
}

//	private void Bufferdout(String plainText, int countindex) throws FileNotFoundException {
//		// TODO Auto-generated method stub
//		
//		BufferedOutputStream bout = null;
//		
//		try {
//			bout = new BufferedOutputStream(new FileOutputStream("./data/result.txt"));
//			
//			bout.write(plainText.getBytes());
//			
//		} catch (IOException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
//		
//	}
//
//}
