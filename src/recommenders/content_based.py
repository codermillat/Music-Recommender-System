from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class ContentBasedRecommender:
    def __init__(self):
        self.cv = CountVectorizer()
        self.cosine_sim = None
        self.indices = None
        self.df = None
        
    def prepare_features(self, df):
        df['combined_features'] = df.apply(
            lambda row: f"{row['user_id']} {row['song_id']} {row['artist_name']} {row['release']}",
            axis=1
        )
        return df
        
    def fit(self, df):
        self.df = self.prepare_features(df)
        count_matrix = self.cv.fit_transform(self.df['combined_features'])
        self.cosine_sim = cosine_similarity(count_matrix)
        self.indices = pd.Series(self.df.index)
        
    def recommend(self, song_id, n_recommendations=10):
        idx = self.indices[self.indices == song_id].index[0]
        score_series = pd.Series(self.cosine_sim[idx]).sort_values(ascending=False)
        top_indices = list(score_series.iloc[1:n_recommendations + 1].index)
        
        return [list(self.df.index)[i] for i in top_indices]