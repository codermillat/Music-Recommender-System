import pandas as pd

class PopularityRecommender:
    def __init__(self):
        self.recommendations = None

    def fit(self, df):
        try:
            song_stats = df.groupby('song_id').agg({
                'freq': 'sum',
                'artist_name': 'first',
                'release': 'first'
            }).reset_index()
            
            self.recommendations = song_stats.sort_values(
                'freq',
                ascending=False
            ).head(10)
            
        except Exception as e:
            raise Exception(f"Error fitting popularity recommender: {str(e)}")
        
    def recommend(self):
        if self.recommendations is None:
            raise Exception("Model not fitted. Call fit() first.")
        return self.recommendations