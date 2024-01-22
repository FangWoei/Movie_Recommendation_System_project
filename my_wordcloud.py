import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def my_wordcloud():
    d_movie = pd.read_csv('movies.csv')
    def process_genres(genres):
        if genres == '(no genres listed)':
            return genres
        else:
            return genres.replace('|', ' ').replace(' ', ', ')
    d_movie['genres']= d_movie['genres'].apply(process_genres)
    d_movie['date'] = d_movie['title'].str.extract(r'\((\d{4})\)', expand=False)
    d_movie['title'] = d_movie['title'].str.replace(r'\s*\(\d{4}\)', '', regex=True)
    d_movie = d_movie[['movieId', 'title', 'date', 'genres']]
    median_date = d_movie['date'].median()
    d_movie['date'].fillna(median_date, inplace=True)
    m_genre = set(d_movie['genres'].str.split(',').explode().str.strip())
    
    d_tag = pd.read_csv('tags.csv')
    d_tag.drop(['userId', 'timestamp'], axis=1, inplace=True)
    
    title_wordcloud = WordCloud(width=800, height=400, background_color='black').generate(' '.join(d_movie['title']))
    genres_wordcloud = WordCloud(width=800, height=400, background_color='black').generate(','.join(d_movie['genres']))
    tag_wordcloud = WordCloud(width=800, height=400, background_color='black').generate(' '.join(d_tag['tag']))
    
    with st.expander('All WordCloud'):
        choose = st.selectbox('Choose a plot to view', ['Movies', 'Tags'])
        
        if choose == 'Movies':
            st.subheader('Movies')
            st.subheader('Title')
            a, ax_title = plt.subplots(figsize=(6, 6))
            ax_title.imshow(title_wordcloud, interpolation='bilinear')
            ax_title.set_title('Word Cloud for Titles')
            ax_title.axis('off')
            st.pyplot(a)
            st.subheader('Genres')
            b,ax_genres = plt.subplots(figsize=(6, 6))
            ax_genres.imshow(genres_wordcloud, interpolation='bilinear')
            ax_genres.set_title('Word Cloud for Genres')
            ax_genres.axis('off')
            st.pyplot(b)
        elif choose == 'Tags':
            st.subheader('Tags')
            c,ax_tag = plt.subplots(figsize=(6, 6))
            ax_tag.imshow(tag_wordcloud, interpolation='bilinear')
            ax_tag.set_title('Word Cloud for Genres')
            ax_tag.axis('off')
            st.pyplot(c)
            
            
        
