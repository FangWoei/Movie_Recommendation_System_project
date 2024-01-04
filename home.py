import streamlit as st
from PIL import Image
# from eda import eda
# from ml import ml
from test import test


def main():
    st.title('Movie Recommendation System')
    menu = ['Home','Test' ]
    choice = st.sidebar.selectbox('Menu', menu)
    if choice == 'Home':
        st.image('https://tse3.mm.bing.net/th?id=OIP.U-R58ahr5dtAvtSLGK2wXgHaEK&pid=Api&P=0&h=180')
        st.text("Hello World")

    # elif choice == 'EDA':
    #     eda()
    else:
        test()

main()