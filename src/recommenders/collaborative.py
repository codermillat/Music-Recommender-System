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
        reader = Reader()
        return Dataset.load_from_df(
            df[['user_id', 'song_id', 'freq']],
            reader
        )
        
    def train(self, data, test_size=0.25):
        trainset, testset = train_test_split(data, test_size=test_size)
        self.algo.fit(trainset)
        return self.algo.test(testset)
        
    def get_predictions(self, predictions):
        return pd.DataFrame(
            predictions,
            columns=['uid', 'iid', 'rui', 'est', 'details']
        )