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

@st.cache_data
def load_data():
    data_loader = DataLoader()
    return data_loader.merge_data()

def main():
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

    # Initialize recommenders
    pop_rec = PopularityRecommender()
    collab_rec = CollaborativeRecommender()
    content_rec = ContentBasedRecommender()

    # Sidebar navigation
    page = st.sidebar.radio("Select a Page", [
        "Dashboard",
        "Popularity-Based",
        "Collaborative Filtering",
        "Content-Based"
    ])

    if page == "Dashboard":
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Artists")
            top_artists = df.groupby('artist_name')['freq'].sum().sort_values(ascending=False).head(10)
            fig = px.bar(
                top_artists,
                orientation='h',
                title="Most Popular Artists"
            )
            st.plotly_chart(fig)
        
        with col2:
            st.subheader("Listening Patterns")
            fig = px.histogram(
                df,
                x='freq',
                nbins=50,
                title="Distribution of Play Counts"
            )
            st.plotly_chart(fig)

        col3, col4, col5 = st.columns(3)
        col3.metric("Total Users", f"{df['user_id'].nunique():,}")
        col4.metric("Total Songs", f"{df['song_id'].nunique():,}")
        col5.metric("Total Artists", f"{df['artist_name'].nunique():,}")

    elif page == "Popularity-Based":
        st.header("Popular Songs")
        pop_rec.fit(df)
        recommendations = pop_rec.recommend()
        st.dataframe(recommendations)

    elif page == "Collaborative Filtering":
        st.header("User-Based Recommendations")
        user_id = st.selectbox("Select a User ID", df['user_id'].unique()[:100])
        
        if st.button("Get Recommendations"):
            with st.spinner("Generating recommendations..."):
                data = collab_rec.prepare_data(df)
                collab_rec.train(data)
                recommendations = collab_rec.recommend_songs(user_id, df)
                
                results = []
                for pred in recommendations:
                    song_info = df[df['song_id'] == pred.iid].iloc[0]
                    results.append({
                        'Artist': song_info['artist_name'],
                        'Song': song_info['release'],
                        'Score': f"{pred.est:.2f}"
                    })
                st.dataframe(pd.DataFrame(results))

    elif page == "Content-Based":
        st.header("Similar Songs")
        song_id = st.selectbox("Select a Song ID", df['song_id'].unique()[:100])
        
        if st.button("Find Similar Songs"):
            with st.spinner("Finding similar songs..."):
                content_rec.fit(df)
                similar_songs = content_rec.recommend(song_id)
                st.dataframe(similar_songs[['artist_name', 'release']])

if __name__ == "__main__":
    main()