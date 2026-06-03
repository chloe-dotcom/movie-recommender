import streamlit as st
import pickle
import requests
import pandas as pd

API_KEY = '826d2071a61ce1a7fb11b57c036ddc53'

movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url, timeout=5).json()
        poster = data.get('poster_path')
        if poster:
            return f"https://image.tmdb.org/t/p/w500{poster}"
    except Exception as e:
        print("poster fetch failed:", e)
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    idx = movies_df[movies_df['title'] == movie].index[0]
    movie_list = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])[1:6]
    names, posters = [], []
    for i, _ in movie_list:
        names.append(movies_df.iloc[i].title)
        posters.append(fetch_poster(movies_df.iloc[i].movie_id))
    return names, posters

st.title('🎬 Movie Recommender System')

selected = st.selectbox('Pick a movie:', movies_df['title'].values)

if st.button('Recommend'):
    # print("CLICKED")
    names, posters = recommend(selected)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.image(poster)
            st.caption(name)