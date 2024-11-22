# Music Recommender System

A comprehensive music recommendation system using collaborative filtering, content-based, and popularity-based approaches, designed for Google Colab and Kaggle environments.

## Features

1. **Popularity-Based Recommender**
   - Recommends most popular songs based on play counts
   - Simple but effective baseline system

2. **Collaborative Filtering**
   - User-based approach using KNN with Means
   - Cosine similarity metric
   - k=50 neighbors

3. **Content-Based Recommender**
   - Uses song metadata (artist, title)
   - TF-IDF vectorization
   - Cosine similarity for recommendations

## Dataset Structure

- `kaggle_visible_evaluation_triplets.txt`: User listening history
- `unique_tracks.txt`: Song metadata
- `taste_profile_song_to_tracks.txt`: Song to track mappings

## Usage

1. Upload the notebook to Google Colab or Kaggle
2. Upload the dataset files to the `/data` directory
3. Run all cells sequentially
4. Explore different recommendation approaches

## Requirements

See `requirements.txt` for detailed dependencies.