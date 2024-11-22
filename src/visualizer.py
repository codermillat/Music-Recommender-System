import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class DataVisualizer:
    @staticmethod
    def plot_top_artists(df, n=10):
        """Plot top artists using matplotlib/seaborn for better notebook compatibility."""
        try:
            plt.figure(figsize=(12, 6))
            top_artists = df.groupby('artist_name')['freq'].sum().sort_values(ascending=False).head(n)
            sns.barplot(x=top_artists.values, y=top_artists.index)
            plt.title('Most Popular Artists')
            plt.xlabel('Play Count')
            plt.ylabel('Artist')
            plt.tight_layout()
            return plt.gcf()
        except Exception as e:
            raise Exception(f"Error creating top artists plot: {str(e)}")
    
    @staticmethod
    def plot_listening_patterns(df, bins=50):
        """Plot listening patterns using matplotlib/seaborn."""
        try:
            plt.figure(figsize=(10, 6))
            sns.histplot(data=df, x='freq', bins=bins)
            plt.title('Distribution of Play Counts')
            plt.xlabel('Play Count')
            plt.ylabel('Number of Songs')
            plt.tight_layout()
            return plt.gcf()
        except Exception as e:
            raise Exception(f"Error creating listening patterns plot: {str(e)}")
            
    @staticmethod
    def display_recommendations(recommendations, df=None):
        """Format recommendations for display in notebook."""
        try:
            if df is not None:
                result = recommendations.merge(
                    df[['song_id', 'artist_name', 'release']].drop_duplicates(),
                    on='song_id'
                )[['artist_name', 'release', 'freq']]
            else:
                result = recommendations[['artist_name', 'release', 'freq']]
            
            # Format for better notebook display
            return result.style.set_properties(**{
                'text-align': 'left',
                'white-space': 'pre-wrap'
            }).set_table_styles([
                {'selector': 'th', 'props': [('text-align', 'left')]},
                {'selector': '', 'props': [('border', '1px solid #ddd')]}
            ])
        except Exception as e:
            raise Exception(f"Error displaying recommendations: {str(e)}")

    @staticmethod
    def plot_evaluation_metrics(metrics_dict):
        """Plot evaluation metrics for the models."""
        try:
            plt.figure(figsize=(10, 6))
            metrics_df = pd.DataFrame(list(metrics_dict.items()), columns=['Metric', 'Value'])
            sns.barplot(data=metrics_df, x='Metric', y='Value')
            plt.title('Model Evaluation Metrics')
            plt.xticks(rotation=45)
            plt.tight_layout()
            return plt.gcf()
        except Exception as e:
            raise Exception(f"Error plotting evaluation metrics: {str(e)}")