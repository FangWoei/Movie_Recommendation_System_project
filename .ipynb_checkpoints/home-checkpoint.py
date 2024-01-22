import streamlit as st
from PIL import Image
from table import table
from chart import chart
from my_wordcloud import my_wordcloud
from test import test


def main():
    st.title('Movie Recommendation System')
    menu = ['Home','Table','chart','WordCloud' ]
    choice = st.sidebar.selectbox('Menu', menu)
    if choice == 'Home':
        st.title('Foo Fang Woei')
        st.text(18)
        st.text('Movie Recommendation System')
        st.text('Why I want do this project')
        st.info('Creating a personalized movie recommendation system excites me as a movie enthusiast. It promises to deliver films tailored to my preferences, enhancing my entertainment experience.')
        img = Image.open('minions-shh.gif')
        st.image(img)
    elif choice == 'Table':
        table()
    elif choice == 'chart':
        chart()
    else :
        my_wordcloud()

main()