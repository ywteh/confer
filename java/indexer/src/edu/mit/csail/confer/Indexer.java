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
      Map<String, Map<String, Object>> papers = new HashMap<String,Map<String, Object>>();
      Gson gson = new Gson();
      papers=(Map<String,Map<String,Object>>)gson.fromJson(text.toString(), papers.getClass());
      Iterator<String> iterator = papers.keySet().iterator();
      while (iterator.hasNext()) {  
          String paper_id = iterator.next().toString();  
          Map<String, Object> paper_details = papers.get(paper_id);
          String title = paper_details.get("title").toString();
          String abstrct = paper_details.get("abstract").toString();
          String session = paper_details.get("session").toString();
          //System.out.println(title);
          //System.out.println(abstrct);
          System.out.println(session);
          Document doc = new Document();   
          Field f_paper_id = new StringField("paper_id", paper_id, Field.Store.YES);
          Field f_session = new TextField("session", session, Field.Store.YES);
          Field f_title = new TextField("title", title, Field.Store.YES);
          Field f_abstract = new TextField("abstract", abstrct, Field.Store.YES);
          f_session.setBoost((float) 5.11);
          doc.add(f_paper_id);
          doc.add(f_session);
          doc.add(f_title);
          doc.add(f_abstract);
          if (writer.getConfig().getOpenMode() == OpenMode.CREATE) {
            writer.addDocument(doc);
          } else {
            writer.updateDocument(new Term("docId", paper_id), doc);
          }
       }  
      writer.close();	  
  }
  
 void getSimilarity() throws IOException {	    
	IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(this.indexPath)));
	IndexSearcher searcher = new IndexSearcher(reader);
	Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_40);
	MoreLikeThis mlt = new MoreLikeThis(reader); // Pass the index reader
	mlt.setAnalyzer(analyzer);
	mlt.setFieldNames(new String[] {"session", "title", "abstract"}); // specify the fields for similiarity
	HashMap<String, ArrayList<HashMap<String, Float>>> similar_docs = new HashMap<String, ArrayList<HashMap<String,Float>>>();
	for (int i=0; i<reader.maxDoc(); i++) { 
		ArrayList<HashMap<String, Float>> t = new ArrayList<HashMap<String,Float>>();
	    Query query = mlt.like(i);
	    TopDocs similarDocs = searcher.search(query, 11); // Use the searcher
		ScoreDoc[] docs = similarDocs.scoreDocs;
		for(int k=0; k<docs.length; k++){
			if(docs[k].doc == i){
				continue;
			}
			HashMap<String, Float> m = new HashMap<String, Float>();
			m.put(reader.document(docs[k].doc).getField("paper_id").stringValue(), docs[k].score);
			t.add(m);
		}
		similar_docs.put(reader.document(i).getField("paper_id").stringValue(), t);
	}
    Gson gson = new Gson(); 
    String json = gson.toJson(similar_docs); 
    PrintWriter out = new PrintWriter(this.similarDocsPath);
    out.println(json);
    out.close();
  } 

}
