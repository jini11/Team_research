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
	// ��� ���� �����͸� ����

	public StartNlp() {
		// TODO Auto-generated constructor stub

		ReadReview();
	}

	@SuppressWarnings("resource")
	private void ReadReview() {
		// TODO Auto-generated method stub

		// ���� ������ �ҷ�����

		try {

			FileInputStream fileStream = null;

			fileStream = new FileInputStream("./data/Review_Data.txt");

			byte readBuffer[] = new byte[fileStream.available()];

			while (fileStream.read(readBuffer) != -1) {
				FullReview += new String(readBuffer, "UTF-8");
				// ���ڵ� ������ �����ϱ� ���Ͽ� UTF-8 ���
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
		// ���� ����� ���� ���並 '/'�� �����ϰ� �������Ƿ�, �ٽ� �и�

		int countindex = 1; // ���� ���� ������

		for (String i : splitReview) {
			NLP(i.replace("\\s+", ""), countindex);
			// ����ǥ������ ����Ͽ� ���� �������� ������ ������ ��, ���� ���� �������� �Բ� NLP �� ����
			countindex++;
		}
	}

	private void NLP(String str, int countindex) {
		// Komoran �� Ȱ���� ���¼� �м�
		Komoran komoran = new Komoran(DEFAULT_MODEL.LIGHT);
		// Default_Model �����Ͽ� ���¼� �м�

		// System.out.println(countindex+" "+str);

		KomoranResult analyzeResultList = komoran.analyze(str);
		// doToken �Լ��� ���е� ���� ���並 ���¼� �м��� ���̺귯���� �Է�

		resultWrite(analyzeResultList, countindex, str);
	}

	private void resultWrite(KomoranResult analyzeResultList, int countindex, String str) {
		// TODO Auto-generated method stub

		BufferedWriter output = null;

		try {
			output = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("./data/result.csv", true)));

			//output.write((countindex + ",").replace("\n", ""));// ���� ������ �Է� (1�� �÷�)
			output.write((str + ",").replace("\n", ""));// ���� ���� �Է� (2�� �÷�)
			output.write((analyzeResultList.getPlainText() + ",").replace("\n", ""));// ���¼� �м� �Է�(3�� �÷�)
			output.newLine();// �ٹٲ�

			System.out.println(countindex); // �����Ȳ ���

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
