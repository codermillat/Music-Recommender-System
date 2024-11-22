# Music Recommender System

A comprehensive music recommendation system using collaborative filtering, content-based, and popularity-based approaches, optimized for Google Colab.

## Features

1. **Popularity-Based Recommender**
   - Recommends most popular songs based on play counts
   - Simple but effective baseline system

2. **Collaborative Filtering**
   - User-based approach using KNN with Means
   - Cosine similarity metric
   - Optimized for sparse matrices

3. **Content-Based Recommender**
   - Uses song metadata (artist, title)
   - TF-IDF vectorization
   - Efficient similarity computation

## Usage in Google Colab

1. Clone the repository:
```python
!git clone https://github.com/your-username/music-recommender.git
```

2. Install dependencies:
```python
!pip install -r requirements.txt
```

3. Run the Streamlit app:
```python
!streamlit run app.py
```

## Dataset Structure

The dataset should be placed in the `/data` directory:
- `kaggle_visible_evaluation_triplets.txt`: User listening history
- `unique_tracks.txt`: Song metadata

## Requirements

See `requirements.txt` for detailed dependencies.