import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

def chart():
    d_link = pd.read_csv('links.csv')
    d_link.drop(['imdbId', 'tmdbId'], axis=1, inplace=True)
    
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
    
    d_rating = pd.read_csv('ratings.csv')
    d_rating.drop(['timestamp'], axis=1, inplace=True)
    
    d_tag = pd.read_csv('tags.csv')
    d_tag.drop(['userId', 'timestamp'], axis=1, inplace=True)
    
    merged_df = pd.merge(d_rating, d_movie, on='movieId', how='inner')
    merged_df = pd.merge(merged_df, d_tag, on='movieId', how='inner')
    merged_df = pd.merge(merged_df, d_link, on='movieId', how='inner')
    with st.expander('All Chart'):
        choose = st.selectbox('Choose a plot to view', ['Movies', 'Ratings', 'Model'])
        
        if choose == 'Movies':
            st.subheader('Movies')
            genres_count = d_movie['genres'].str.split(',').explode().str.strip().value_counts()
            a = px.bar(
                x=genres_count.index,
                y=genres_count.values,
                labels={'x': 'Genre', 'y': 'Count'},
                title='Distribution of Movie Genres',
                template='plotly',
                color=genres_count.values,
                color_continuous_scale='viridis',
            )
            
            st.plotly_chart(a)
            
            all_genres = ",".join(d_movie['genres'].head(10)).split(',')
            genre_counts = pd.Series(all_genres).value_counts()
            b = px.pie(
                genre_counts,
                names=genre_counts.index,
                values=genre_counts.values,
                title='Distribution of Movie Genres',
                template='plotly',
                hole=0.3,
            )
        
            st.plotly_chart(b)
        
        elif choose == 'Ratings':
            st.subheader('Ratings')
            c = sns.countplot(x='rating', data=merged_df)
            plt.title('Distribution of Ratings')
            st.pyplot(c.figure)
            
            
            top_20_movies = merged_df.groupby('title')['rating'].mean().sort_values(ascending=False).head(20)
            st.subheader('Top 20 Movies with Highest Ratings')
            sns.set(style="whitegrid", font_scale=1.2)
            plt.figure(figsize=(14, 8))
            bar_plot = sns.barplot(x=top_20_movies.values, y=top_20_movies.index, palette='viridis')
            plt.title('Top 20 Movies with Highest Ratings', fontsize=18)
            plt.xlabel('Average Rating', fontsize=14)
            plt.ylabel('Movie Title', fontsize=14)
            plt.xlim(0, 5)
            for index, value in enumerate(top_20_movies.values):
                bar_plot.text(value + 0.1, index, f'{value:.2f}', va='center', fontsize=12)

            st.pyplot(plt.gcf())
            
        elif choose == 'Model':
            st.subheader('Descriptive Statistics')
            img = Image.open('Descriptive Statistics.png')
            st.image(img)
        