import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=291d874a58936d19f133b0cf2e915566&language=en-US"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"API call failed with status code: {response.status_code}")
            return "https://via.placeholder.com/185x278?text=API+Error"
        
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
            return full_path
        else:
            print(f"No poster path found for movie_id: {movie_id}")
            return "https://via.placeholder.com/185x278?text=No+Image"
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/185x278?text=Error"

# Function to recommend movies
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:  # Top 5 recommendations
            movie_id = movies.iloc[i[0]].movie_id
            print(f"Fetching poster for movie: {movies.iloc[i[0]].title}, Movie ID: {movie_id}")
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return [], []

# Streamlit App
st.header('🎬 Movie Recommender System')

# Load data
try:
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# User input
selected_movie = st.selectbox("Type or select a movie from the dropdown", movies['title'].values)

# Recommendation button
if st.button('Recommend'):
    with st.spinner('Fetching recommendations...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        if recommended_movie_names:
            # Display recommendations
            col1, col2, col3, col4, col5 = st.columns(5)
            cols = [col1, col2, col3, col4, col5]
            for i in range(5):
                with cols[i]:
                    st.text(recommended_movie_names[i])
                    st.image(recommended_movie_posters[i])
