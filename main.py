import argparse
import json
import sys
from src.data_loader import DataLoader
from src.recommenders.popularity_based import PopularityRecommender
from src.recommenders.collaborative import CollaborativeRecommender
from src.recommenders.content_based import ContentBasedRecommender

def get_chart_data(df):
    # Get top artists data
    top_artists = df.groupby('artist_name')['freq'].sum().sort_values(ascending=False).head(10)
    artists_data = {
        'artists': [
            {'name': name, 'count': int(count)}
            for name, count in top_artists.items()
        ],
        'patterns': {
            'plays': df['freq'].tolist()
        }
    }
    return artists_data

def main():
    parser = argparse.ArgumentParser(description='Music Recommender System')
    parser.add_argument('--type', required=True, 
                      choices=['charts', 'popular', 'collaborative', 'content'])
    parser.add_argument('--user', help='User ID for collaborative filtering')
    parser.add_argument('--song', help='Song ID for content-based filtering')
    args = parser.parse_args()

    try:
        # Initialize data loader
        data_loader = DataLoader(
            'data/kaggle_visible_evaluation_triplets.txt',
            'data/unique_tracks.txt'
        )
        df = data_loader.merge_data()

        if args.type == 'charts':
            result = get_chart_data(df)
        
        elif args.type == 'popular':
            pop_rec = PopularityRecommender()
            pop_rec.create(df, 'user_id', 'song_id')
            result = pop_rec.recommend(df['user_id'].iloc[0])
            
        elif args.type == 'collaborative':
            if not args.user:
                raise ValueError("User ID is required for collaborative filtering")
            collab_rec = CollaborativeRecommender()
            data = collab_rec.prepare_data(df)
            result = collab_rec.train(data)
            
        elif args.type == 'content':
            if not args.song:
                raise ValueError("Song ID is required for content-based filtering")
            content_rec = ContentBasedRecommender()
            content_rec.fit(df)
            result = content_rec.recommend(args.song)
        
        print(json.dumps(result))
        
    except Exception as e:
        print(json.dumps({
            'error': str(e),
            'status': 500
        }), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()