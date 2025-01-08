import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f0099d3c8a0a1c63dcbf8cdf110a65f4&language=en-US')
    data = response.json()
    # Check if 'poster_path' exists in the API response
    if 'poster_path' in data and data['poster_path']:
        return "http://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        # Return a placeholder image if 'poster_path' is missing
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies['movie_id'].iloc[i[0]]  # Replace 'movie_id' with the actual column name
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters



movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

# Initialize names and posters
names = []
posters = []

selected_movie_name = st.selectbox(
    "Select a Movie:",
    movies['title'].values,
    index=None,
    placeholder='Select Movies',
)

st.write("You selected:", selected_movie_name)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f"<h3 style='font-size:16px;'>{names[0] if names else 'Movie 1'}</h3>",
        unsafe_allow_html=True,
    )
    st.image(posters[0] if posters else "https://via.placeholder.com/500x750?text=No+Image")

with col2:
    st.markdown(
        f"<h3 style='font-size:16px;'>{names[1] if names else 'Movie 2'}</h3>",
        unsafe_allow_html=True,
    )
    st.image(posters[1] if posters else "https://via.placeholder.com/500x750?text=No+Image")

with col3:
    st.markdown(
        f"<h3 style='font-size:16px;'>{names[2] if names else 'Movie 3'}</h3>",
        unsafe_allow_html=True,
    )
    st.image(posters[2] if posters else "https://via.placeholder.com/500x750?text=No+Image")

with col4:
    st.markdown(
        f"<h3 style='font-size:16px;'>{names[3] if names else 'Movie 4'}</h3>",
        unsafe_allow_html=True,
    )
    st.image(posters[3] if posters else "https://via.placeholder.com/500x750?text=No+Image")

with col5:
    st.markdown(
        f"<h3 style='font-size:16px;'>{names[4] if names else 'Movie 5'}</h3>",
        unsafe_allow_html=True,
    )
    st.image(posters[4] if posters else "https://via.placeholder.com/500x750?text=No+Image")
