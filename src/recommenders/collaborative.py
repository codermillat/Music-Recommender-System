from surprise import KNNWithMeans, Dataset, Reader
from surprise.model_selection import train_test_split

class CollaborativeRecommender:
    def __init__(self, k=50):
        self.k = k
        self.algo = KNNWithMeans(
            k=k,
            sim_options={'name': 'cosine', 'user_based': True}
        )
        
    def prepare_data(self, df):
        try:
            reader = Reader()
            return Dataset.load_from_df(
                df[['user_id', 'song_id', 'freq']],
                reader
            )
        except Exception as e:
            raise Exception(f"Error preparing data: {str(e)}")
        
    def train(self, data):
        try:
            trainset, testset = train_test_split(data, test_size=0.25)
            self.algo.fit(trainset)
            return self.algo.test(testset)
        except Exception as e:
            raise Exception(f"Error training model: {str(e)}")
    
    def recommend_songs(self, user_id, df, n_recommendations=5):
        try:
            user_songs = set(df[df['user_id'] == user_id]['song_id'])
            all_songs = set(df['song_id'])
            songs_to_predict = list(all_songs - user_songs)
            
            predictions = [
                self.algo.predict(user_id, song_id)
                for song_id in songs_to_predict[:100]  # Limit for demo
            ]
            
            predictions.sort(key=lambda x: x.est, reverse=True)
            return predictions[:n_recommendations]
        except Exception as e:
            raise Exception(f"Error generating recommendations: {str(e)}")