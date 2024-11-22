import pandas as pd

class PopularityRecommender:
    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.item_id = None
        self.popularity_recommendations = None

    def create(self, train_data, user_id, item_id):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id

        train_data_grouped = train_data.groupby([self.item_id]).agg({
            self.user_id: 'count'
        }).reset_index()
        
        train_data_grouped.rename(columns={'user_id': 'score'}, inplace=True)
        train_data_sort = train_data_grouped.sort_values(
            ['score', self.item_id],
            ascending=[0, 1]
        )
        
        train_data_sort['Rank'] = train_data_sort['score'].rank(
            ascending=0,
            method='first'
        )
        
        self.popularity_recommendations = train_data_sort.head(10)

    def recommend(self, user_id):
        user_recommendations = self.popularity_recommendations.copy()
        user_recommendations['user_id'] = user_id
        cols = user_recommendations.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        return user_recommendations[cols]