from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class ContentBasedRecommender:
    def __init__(self):
        self.cv = CountVectorizer()
        self.cosine_sim = None
        self.df = None
        
    def prepare_features(self, df):
        try:
            return df.apply(
                lambda x: f"{x['artist_name']} {x['release']}",
                axis=1
            )
        except Exception as e:
            raise Exception(f"Error preparing features: {str(e)}")
        
    def fit(self, df):
        try:
            self.df = df
            features = self.prepare_features(df)
            count_matrix = self.cv.fit_transform(features)
            self.cosine_sim = cosine_similarity(count_matrix)
        except Exception as e:
            raise Exception(f"Error fitting model: {str(e)}")
        
    def recommend(self, song_id, n_recommendations=5):
        try:
            if self.df is None or self.cosine_sim is None:
                raise Exception("Model not fitted. Call fit() first.")
                
            idx = self.df[self.df['song_id'] == song_id].index[0]
            sim_scores = list(enumerate(self.cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:n_recommendations+1]
            song_indices = [i[0] for i in sim_scores]
            
            return self.df.iloc[song_indices][['artist_name', 'release', 'song_id']]
        except Exception as e:
            raise Exception(f"Error generating recommendations: {str(e)}")