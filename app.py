import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import DataLoader
from src.recommenders.popularity_based import PopularityRecommender
from src.recommenders.collaborative import CollaborativeRecommender
from src.recommenders.content_based import ContentBasedRecommender

st.set_page_config(
    page_title="Music Recommender System",
    page_icon="🎵",
    layout="wide"
)

# Initialize data and models
@st.cache_data
def load_data():
    data_loader = DataLoader(
        'data/kaggle_visible_evaluation_triplets.txt',
        'data/unique_tracks.txt'
    )
    return data_loader.merge_data()

def initialize_models(df):
    pop_rec = PopularityRecommender()
    pop_rec.create(df, 'user_id', 'song_id')
    
    collab_rec = CollaborativeRecommender()
    collab_data = collab_rec.prepare_data(df)
    collab_rec.train(collab_data)
    
    content_rec = ContentBasedRecommender()
    content_rec.fit(df)
    
    return pop_rec, collab_rec, content_rec

# Main UI
st.title("🎵 Music Recommender System")
st.markdown("""
This system provides music recommendations using three different approaches:
- 🔥 **Popularity-Based**: Recommends the most popular songs
- 👥 **Collaborative Filtering**: Recommends based on similar users' preferences
- 📝 **Content-Based**: Recommends based on song characteristics
""")

# Load data
with st.spinner("Loading data..."):
    df = load_data()
    pop_rec, collab_rec, content_rec = initialize_models(df)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a Page", [
    "Dashboard",
    "Popularity-Based Recommendations",
    "Collaborative Filtering",
    "Content-Based Recommendations"
])

if page == "Dashboard":
    # Analytics Dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Artists")
        top_artists = df.groupby('artist_name')['freq'].sum().sort_values(ascending=False).head(10)
        fig = px.bar(
            top_artists,
            orientation='h',
            title="Most Popular Artists",
            labels={'artist_name': 'Artist', 'freq': 'Play Count'}
        )
        st.plotly_chart(fig)
    
    with col2:
        st.subheader("Listening Patterns")
        listen_dist = px.histogram(
            df,
            x='freq',
            nbins=50,
            title="Distribution of Play Counts",
            labels={'freq': 'Play Count', 'count': 'Number of Songs'}
        )
        st.plotly_chart(listen_dist)
    
    # Dataset Statistics
    st.subheader("Dataset Statistics")
    col3, col4, col5 = st.columns(3)
    col3.metric("Total Users", len(df['user_id'].unique()))
    col4.metric("Total Songs", len(df['song_id'].unique()))
    col5.metric("Total Artists", len(df['artist_name'].unique()))

elif page == "Popularity-Based Recommendations":
    st.header("Popular Songs")
    
    recommendations = pop_rec.recommend(df['user_id'].iloc[0])
    
    st.dataframe(
        recommendations[['song_id', 'score', 'Rank']]
        .merge(df[['song_id', 'artist_name', 'release']], on='song_id')
        .drop_duplicates()
    )

elif page == "Collaborative Filtering":
    st.header("User-Based Recommendations")
    
    user_id = st.selectbox(
        "Select a User ID",
        options=df['user_id'].unique()[:100]  # Limit for demo
    )
    
    if st.button("Get Recommendations"):
        with st.spinner("Generating recommendations..."):
            user_data = df[df['user_id'] == user_id]
            st.subheader("User's Listening History")
            st.dataframe(
                user_data[['artist_name', 'release', 'freq']]
                .sort_values('freq', ascending=False)
            )

elif page == "Content-Based Recommendations":
    st.header("Similar Songs")
    
    song_id = st.selectbox(
        "Select a Song ID",
        options=df['song_id'].unique()[:100]  # Limit for demo
    )
    
    if st.button("Find Similar Songs"):
        with st.spinner("Finding similar songs..."):
            similar_songs = content_rec.recommend(song_id)
            song_details = df[df['song_id'].isin(similar_songs)][
                ['song_id', 'artist_name', 'release']
            ].drop_duplicates()
            
            st.subheader("Selected Song")
            selected_song = df[df['song_id'] == song_id][
                ['artist_name', 'release']
            ].iloc[0]
            st.write(f"Artist: {selected_song['artist_name']}")
            st.write(f"Title: {selected_song['release']}")
            
            st.subheader("Similar Songs")
            st.dataframe(song_details)