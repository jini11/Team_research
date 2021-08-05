package CRAWLER;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.util.Iterator;
import java.util.*;


import java.io.IOException;

import org.jsoup.Jsoup;

public class crawler {
    
    public crawler(){
        start();
    }

    public static void start(){
        String url="https://www.yogiyo.co.kr/mobile/#/359890/";
        Document doc=null;

        try {
            doc=Jsoup.connect(url).get();
        } catch (IOException e) {
            e.printStackTrace();
        }

        

        Elements element = doc.select("li.list-group");

        Iterator<Element> ie1=element.select("span.review-id").iterator();
        
        while(ie1.hasNext()){
            System.out.println(ie1.next().text());
        }

    }
    
}

