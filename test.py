import streamlit as st
import pandas as pd
import io
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def test():
    d_link = pd.read_csv('links.csv', index_col=0)
    d_movie = pd.read_csv('movies.csv', index_col=0)
    d_rating = pd.read_csv('ratings.csv', index_col=0)
    d_tag = pd.read_csv('tags.csv', index_col=0)
    
    movie_and_link = pd.merge(d_movie, d_link, on='movieId', how='inner')
    movie_and_rating = pd.merge(d_movie, d_rating, on='movieId', how='inner')
    movie_and_rating_and_tag = pd.merge(movie_and_rating, d_tag, on='movieId', how='inner')
    avg_ratings = movie_and_rating.groupby('title')['rating'].mean()
    
    with st.expander('All Data'):
        choose = st.selectbox('Choose a plot to view', ['Movies', 'Movies Links', 'Movies Ratings', 'Movies Tags'])
        if choose == 'Movies':
            st.subheader('Movies')
            st.dataframe(d_movie)
            st.dataframe(d_movie.describe())
        elif choose == 'Movies Links':
            st.subheader('Movies Links')
            st.dataframe(d_link)
            st.dataframe(d_link.describe())
        elif choose == 'Movies Ratings':
            st.subheader('Movies Ratings')
            st.dataframe(d_rating)
            st.dataframe(d_rating.describe())
        elif choose == 'Movies Tags':
            st.subheader('Movies Tags')
            st.dataframe(d_tag)
            st.dataframe(d_tag.describe())

    with st.expander('Combine'):
        choose = st.selectbox('Choose a plot to view', ['Movies and Links', 'Movie and Ratings and Tags'])
        if choose == 'Movies and Links':
            st.subheader('Movies and Links')
            st.dataframe(movie_and_link)
            st.dataframe(movie_and_link.describe())
        elif choose == 'Movie and Ratings and Tags':
            st.subheader('Movie and Ratings and Tags')
            st.dataframe(movie_and_rating_and_tag)
            st.dataframe(movie_and_rating_and_tag.describe())
