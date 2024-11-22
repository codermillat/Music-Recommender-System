import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

class MusicRecommender:
    def __init__(self):
        self.df = None
        self.user_song_matrix = None
        self.similarity_matrix = None
        
    def load_data(self):
        # Load triplets data
        triplets = pd.read_csv('data/kaggle_visible_evaluation_triplets.txt', 
                             sep='\t', names=['user_id', 'song_id', 'freq'])
        
        # Load song metadata
        tracks = pd.read_csv('data/unique_tracks.txt', 
                           sep='<SEP>', names=['track_id', 'song_id', 'artist_name', 'release'])
        
        # Merge data
        self.df = pd.merge(triplets, tracks[['song_id', 'artist_name', 'release']], 
                          on='song_id', how='left')
        return self.df
    
    def get_popular_songs(self, n=10):
        """Get most popular songs based on play frequency"""
        return (self.df.groupby(['song_id', 'artist_name', 'release'])['freq']
                .sum()
                .sort_values(ascending=False)
                .head(n)
                .reset_index())
    
    def create_user_song_matrix(self):
        """Create user-song interaction matrix"""
        self.user_song_matrix = pd.pivot_table(
            self.df, 
            values='freq',
            index='user_id',
            columns='song_id',
            fill_value=0
        )
        return self.user_song_matrix
    
    def compute_similarity(self):
        """Compute user similarity matrix"""
        if self.user_song_matrix is None:
            self.create_user_song_matrix()
        self.similarity_matrix = cosine_similarity(self.user_song_matrix)
        return self.similarity_matrix
    
    def get_similar_users(self, user_id, n=5):
        """Find similar users"""
        if self.similarity_matrix is None:
            self.compute_similarity()
        
        user_idx = self.user_song_matrix.index.get_loc(user_id)
        similar_scores = self.similarity_matrix[user_idx]
        similar_users = self.user_song_matrix.index[np.argsort(similar_scores)[-n-1:-1]]
        return similar_users
    
    def get_user_recommendations(self, user_id, n=5):
        """Get song recommendations for a user"""
        similar_users = self.get_similar_users(user_id)
        
        # Get songs listened to by similar users
        similar_user_songs = (self.df[self.df['user_id'].isin(similar_users)]
                            .groupby(['song_id', 'artist_name', 'release'])['freq']
                            .sum()
                            .sort_values(ascending=False))
        
        # Remove songs the user has already listened to
        user_songs = set(self.df[self.df['user_id'] == user_id]['song_id'])
        recommendations = similar_user_songs[~similar_user_songs.index.get_level_values('song_id').isin(user_songs)]
        
        return recommendations.head(n).reset_index()
    
    def get_content_based_recommendations(self, song_id, n=5):
        """Get content-based song recommendations"""
        # Create song features using artist and title
        song_features = self.df.drop_duplicates('song_id').apply(
            lambda x: f"{x['artist_name']} {x['release']}", axis=1
        )
        
        # Calculate TF-IDF
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(song_features)
        
        # Calculate similarity
        song_idx = self.df[self.df['song_id'] == song_id].index[0]
        sim_scores = cosine_similarity(tfidf_matrix[song_idx], tfidf_matrix).flatten()
        
        # Get similar song indices
        similar_indices = sim_scores.argsort()[-n-1:-1][::-1]
        
        return self.df.iloc[similar_indices][['song_id', 'artist_name', 'release']].drop_duplicates()
    
    def plot_top_artists(self, n=10):
        """Plot top artists by play count"""
        plt.figure(figsize=(12, 6))
        top_artists = self.df.groupby('artist_name')['freq'].sum().sort_values(ascending=False).head(n)
        sns.barplot(x=top_artists.values, y=top_artists.index)
        plt.title('Most Popular Artists')
        plt.xlabel('Total Play Count')
        plt.tight_layout()
        return plt.gcf()
    
    def plot_listening_distribution(self):
        """Plot distribution of listening frequencies"""
        plt.figure(figsize=(10, 6))
        sns.histplot(data=self.df, x='freq', bins=50)
        plt.title('Distribution of Play Counts')
        plt.xlabel('Play Count')
        plt.ylabel('Number of Songs')
        plt.tight_layout()
        return plt.gcf()

# Example usage
if __name__ == "__main__":
    recommender = MusicRecommender()
    df = recommender.load_data()
    
    print("\nDataset Statistics:")
    print(f"Total Users: {df['user_id'].nunique():,}")
    print(f"Total Songs: {df['song_id'].nunique():,}")
    print(f"Total Artists: {df['artist_name'].nunique():,}")
    
    # Get popular songs
    print("\nTop 5 Popular Songs:")
    print(recommender.get_popular_songs(5))
    
    # Get recommendations for a sample user
    sample_user = df['user_id'].iloc[0]
    print(f"\nRecommendations for user {sample_user}:")
    print(recommender.get_user_recommendations(sample_user, 5))
    
    # Get content-based recommendations for a sample song
    sample_song = df['song_id'].iloc[0]
    print(f"\nSimilar songs to {sample_song}:")
    print(recommender.get_content_based_recommendations(sample_song, 5))