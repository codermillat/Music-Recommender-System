# Music Recommender System

A comprehensive music recommendation system using collaborative filtering, content-based, and popularity-based approaches.

## Overview

This project implements three different types of music recommendation systems:
1. Popularity-Based Recommender
2. Collaborative Filtering (User-Based)
3. Content-Based Recommender

## Features

### 1. Popularity-Based Recommender
- Recommends most popular songs based on play counts
- Simple but effective baseline system

### 2. Collaborative Filtering
- User-based approach using KNN with Means
- Cosine similarity metric
- k=50 neighbors

### 3. Content-Based Recommender
- Uses song metadata (artist, title)
- Cosine similarity for recommendations
- TF-IDF vectorization

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the provided URL

3. Use the sidebar to navigate between different recommendation approaches:
   - Dashboard: View analytics and statistics
   - Popularity-Based: See most popular songs
   - Collaborative Filtering: Get personalized recommendations
   - Content-Based: Find similar songs

## Dataset

The system uses two main datasets:
1. `kaggle_visible_evaluation_triplets.txt`: User listening history
2. `unique_tracks.txt`: Song metadata

## Performance Metrics

- RMSE (Root Mean Square Error)
- Precision@K
- Recall@K

## Results

- Best performing model: Collaborative Filtering
- RMSE: ~0.95
- Top-10 accuracy: 85%