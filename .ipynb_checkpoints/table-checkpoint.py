import streamlit as st
import pandas as pd
import io
import plotly.express as px

def table():
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

    mean_rating = merged_df['rating'].mean()
    median_rating = merged_df['rating'].median()
    std_dev_rating = merged_df['rating'].std()
    top_tags = merged_df['tag'].value_counts().head(10)

    with st.expander('All Data'):
        choose = st.selectbox('Choose a plot to view', ['Movies', 'Movies Links', 'Movies Ratings', 'Movies Tags'])
        if choose == 'Movies':
            st.subheader('Movies')
            st.dataframe(d_movie)
            
            col1, col2 = st.columns(2)

            with col1:
                st.subheader('Movie Describe')
                st.dataframe(d_movie.describe())
            with col2:
                st.subheader('Movie Dtypes')
                st.dataframe(d_movie.dtypes)
            
            col1, col2 = st.columns(2)

            with col1:
                st.subheader('All Genres')
                st.dataframe(m_genre)
            with col2:
                st.subheader('Movie Shape')
                st.dataframe(d_movie.shape)
            
        elif choose == 'Movies Links':
            st.subheader('Movies Links')
            st.dataframe(d_link)
            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader('Link Describe')
                st.dataframe(d_link.describe())
            with col2:
                st.subheader('Link Dtypes')
                st.dataframe(d_link.dtypes)
            with col3:
                st.subheader('Link Shape')
                st.dataframe(d_link.shape)
                
                
        elif choose == 'Movies Ratings':
            st.subheader('Movies Ratings')
            st.dataframe(d_rating)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader('Ratings Describe')
                st.dataframe(d_rating.describe())
            with col2:
                st.subheader('Ratings Dtypes')
                st.dataframe(d_rating.dtypes)
            with col3:
                st.subheader('Ratings Shape')
                st.dataframe(d_rating.shape)
                
        elif choose == 'Movies Tags':
            st.subheader('Movies Tags')
            st.dataframe(d_tag)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader('Tags Describe')
                st.dataframe(d_tag.describe())
            with col2:
                st.subheader('Tags Dtypes')
                st.dataframe(d_tag.dtypes)
            with col3:
                st.subheader('Tags Shape')
                st.dataframe(d_tag.shape)
                
    with st.expander('Combine'):
        choose = st.selectbox('Choose a plot to view', ['All Data', 'Model'])
        if choose == 'All Data':
            st.subheader('All Data')
            st.dataframe(merged_df)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader('All Describe')
                st.dataframe(merged_df.describe())
            with col2:
                st.subheader('All Dtypes')
                st.dataframe(merged_df.dtypes)
            with col3:
                st.subheader('All Shape')
                st.dataframe(merged_df.shape)
        if choose == 'Model':
                st.subheader('Descriptive Statistics')
                st.text("Mean")
                st.text(mean_rating)
                st.text("Median")
                st.text(median_rating)
                st.text("Std")
                st.text(std_dev_rating)
                st.text("Top tags")
                st.text(top_tags)
                


            
        