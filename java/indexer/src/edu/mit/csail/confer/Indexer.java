package edu.mit.csail.confer;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queries.mlt.MoreLikeThis;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

import com.google.gson.Gson;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Scanner;

/** 
 * Index papers.json
 * 
 * @author anantb
 * @date 06/13/2013
 * 
 */
public class Indexer {
	String docsPath = "/Users/anantb/Downloads/papers.json";
	String similarDocsPath = "/Users/anantb/Downloads/similar_docs.json";
	String indexPath = "index";
	boolean create = true;
  
  public Indexer() {
  }
  
  public Indexer(String docsPath, String indexPath, String similarDocsPath, boolean create) {
	  this.docsPath = docsPath;
	  this.indexPath = indexPath;
	  this.similarDocsPath = similarDocsPath;
	  this.create = create;
	  
  }

  public static void main(String[] args) {
    
    try {
    	Indexer indexer = null;
    	if(args.length == 3){
    		indexer = new Indexer(args[0], args[1], args[2], true);
    	}else{
    		indexer = new Indexer();
    	}
    	indexer.index();
    	indexer.getSimilarity();
    } catch (IOException e) {
      System.out.println(" caught a " + e.getClass() +
       "\n with message: " + e.getMessage());
    }
  }

 



  void index() throws IOException{	 
      Directory indexDir = FSDirectory.open(new File(this.indexPath));
      Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_40);
      IndexWriterConfig iwc = new IndexWriterConfig(Version.LUCENE_40, analyzer);
      if (create) {
        iwc.setOpenMode(OpenMode.CREATE);
      } else {
        iwc.setOpenMode(OpenMode.CREATE_OR_APPEND);
      }
      IndexWriter writer = new IndexWriter(indexDir, iwc);
      
      StringBuilder text = new StringBuilder();
      Scanner scanner = new Scanner(new FileInputStream(this.docsPath));
      try {
        while (scanner.hasNextLine()){
          text.append(scanner.nextLine());
        }
      }
      finally{
        scanner.close();
      }
      //System.out.println(text);
      Map<String,Object> map = new HashMap<String,Object>();
      Gson gson = new Gson();
      map=(Map<String,Object>)gson.fromJson(text.toString(), map.getClass());
      Iterator<String> iterator = map.keySet().iterator();
      while (iterator.hasNext()) {  
          String key = iterator.next().toString();  
          String value = map.get(key).toString(); 
          Document doc = new Document();          
          doc.add(new StringField("docId", key, Field.Store.YES));
          doc.add(new TextField("docText", value, Field.Store.YES));
          if (writer.getConfig().getOpenMode() == OpenMode.CREATE) {
            writer.addDocument(doc);
          } else {
            writer.updateDocument(new Term("docId", key), doc);
          }
       }  
      writer.close();	  
  }
  
 void getSimilarity() throws IOException {	    
	IndexReader reader = DirectoryReader.open(FSDirectory.open(new File("index")));
	IndexSearcher searcher = new IndexSearcher(reader);
	Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_40);
	MoreLikeThis mlt = new MoreLikeThis(reader); // Pass the index reader
	mlt.setAnalyzer(analyzer);
	mlt.setFieldNames(new String[] {"docText"}); // specify the fields for similiarity
	HashMap<String, ArrayList<HashMap<String, Float>>> similar_docs = new HashMap<String, ArrayList<HashMap<String,Float>>>();
	for (int i=0; i<reader.maxDoc(); i++) { 
		ArrayList<HashMap<String, Float>> t = new ArrayList<HashMap<String,Float>>();
	    Query query = mlt.like(i);
	    TopDocs similarDocs = searcher.search(query, 10); // Use the searcher
		ScoreDoc[] docs = similarDocs.scoreDocs;
		for(int k=0; k<docs.length; k++){
			HashMap<String, Float> m = new HashMap<String, Float>();
			m.put(reader.document(docs[k].doc).getField("docId").stringValue(), docs[k].score);
			t.add(m);
		}
		similar_docs.put(reader.document(i).getField("docId").stringValue(), t);
	}
    Gson gson = new Gson(); 
    String json = gson.toJson(similar_docs); 
    PrintWriter out = new PrintWriter(this.similarDocsPath);
    out.println(json);
    out.close();
  } 

}
