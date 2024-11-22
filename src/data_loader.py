import pandas as pd

class DataLoader:
    def __init__(self, triplets_path='data/kaggle_visible_evaluation_triplets.txt',
                 tracks_path='data/unique_tracks.txt'):
        self.triplets_path = triplets_path
        self.tracks_path = tracks_path
        
    def load_triplets(self):
        try:
            return pd.read_csv(
                self.triplets_path,
                sep='\t',
                names=['user_id', 'song_id', 'freq']
            )
        except Exception as e:
            raise Exception(f"Error loading triplets data: {str(e)}")
    
    def load_tracks(self):
        try:
            return pd.read_csv(
                self.tracks_path,
                sep='<SEP>',
                names=['track_id', 'song_id', 'artist_name', 'release']
            ).drop('track_id', axis=1)
        except Exception as e:
            raise Exception(f"Error loading tracks data: {str(e)}")
    
    def merge_data(self):
        try:
            df = self.load_triplets()
            df1 = self.load_tracks()
            return pd.merge(
                df,
                df1.drop_duplicates(['song_id']),
                on='song_id',
                how='left'
            )
        except Exception as e:
            raise Exception(f"Error merging data: {str(e)}")