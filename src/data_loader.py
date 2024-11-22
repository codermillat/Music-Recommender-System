import pandas as pd

class DataLoader:
    def __init__(self, triplets_path, tracks_path):
        self.triplets_path = triplets_path
        self.tracks_path = tracks_path
    
    def load_triplets(self):
        return pd.read_csv(
            self.triplets_path,
            sep='\t',
            names=['user_id', 'song_id', 'freq']
        )
    
    def load_tracks(self):
        return pd.read_csv(
            self.tracks_path,
            sep='<SEP>',
            names=['track_id', 'song_id', 'artist_name', 'release']
        ).drop('track_id', axis=1)
    
    def merge_data(self):
        df = self.load_triplets()
        df1 = self.load_tracks()
        return pd.merge(
            df,
            df1.drop_duplicates(['song_id']),
            on='song_id',
            how='left'
        )