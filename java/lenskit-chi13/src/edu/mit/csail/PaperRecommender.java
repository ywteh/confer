package edu.mit.csail;

import java.io.File;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

import org.grouplens.lenskit.GlobalItemRecommender;
import org.grouplens.lenskit.GlobalItemScorer;
import org.grouplens.lenskit.Recommender;
import org.grouplens.lenskit.RecommenderBuildException;
import org.grouplens.lenskit.RecommenderEngine;
import org.grouplens.lenskit.baseline.BaselinePredictor;
import org.grouplens.lenskit.baseline.ItemMeanPredictor;
import org.grouplens.lenskit.collections.ScoredLongList;
import org.grouplens.lenskit.core.LenskitRecommenderEngineFactory;
import org.grouplens.lenskit.data.dao.SimpleFileRatingDAO;
import org.grouplens.lenskit.knn.item.ItemItemGlobalRecommender;
import org.grouplens.lenskit.knn.item.ItemItemGlobalScorer;

import org.grouplens.lenskit.transform.normalize.BaselineSubtractingUserVectorNormalizer;
import org.grouplens.lenskit.transform.normalize.UserVectorNormalizer;
import py4j.GatewayServer;

public class PaperRecommender {
	GlobalItemRecommender grec;
	UserRecommender u;
	
	public PaperRecommender(String fileName, String fileName2) throws RecommenderBuildException{
		u = new UserRecommender(fileName2);
		
		LenskitRecommenderEngineFactory factory = new LenskitRecommenderEngineFactory();
		File f = new File(fileName);
		factory.setDAOFactory(new SimpleFileRatingDAO.Factory(f, "\t"));
		/* configure a normalizer and baseline predictor */
		factory.bind(UserVectorNormalizer.class)
	       .to(BaselineSubtractingUserVectorNormalizer.class);
		factory.bind(BaselinePredictor.class)
		       .to(ItemMeanPredictor.class);
		factory.bind(GlobalItemScorer.class).to(ItemItemGlobalScorer.class);
		factory.bind(GlobalItemRecommender.class).to(ItemItemGlobalRecommender.class);
		RecommenderEngine engine = factory.create();
		/* get the and use the recommender */
		Recommender rec = engine.open();
		grec = rec.getGlobalItemRecommender();
	}
	
	public ArrayList<String> recommend(ArrayList<String> i_items){
		Set<Long> input_items = new HashSet<Long>();
		for (String i : i_items){ 
          input_items.add(Long.valueOf(i)); 
        }
		ArrayList<String> ret = new ArrayList<String>();
		ScoredLongList recommendations = this.grec.globalRecommend(input_items, 20);
		int len = recommendations.size();
		long items[] = new long[len];
		double scores[] = new double[len];
		if(len > 0)
			recommendations.getElements(0, items, scores, 0, len);
		for(int i=0; i< len; i++){
			ret.add(items[i] + "," + scores[i]);
		}
		return ret;
	}
	
	public ArrayList<String> recommend_users(ArrayList<String> i_items){
		return u.recommend(i_items);
	}
	
	

	public static void main(String[] args){
		
		try{
			PaperRecommender p = new PaperRecommender(args[0], args[1]);
			GatewayServer gatewayServer = new GatewayServer(p);
	        gatewayServer.start();
	        System.out.println("Gateway Server Started");
		}catch(RecommenderBuildException rbe){
			rbe.printStackTrace();
		}		
		
		
	}

}
