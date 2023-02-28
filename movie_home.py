"""
Streamlit version of the Movie Recommender!
To run:
$ streamlit run movie_home.py

Streamlit script can run remotely (useful to run scripts from github):
$ streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py
However, this particular one is out of date!
In fact, none of the examples works!

Ref:
https://surendraredd.github.io/Books/
"""

### Import libraries
import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import urllib.request
from PIL import Image
import time

from scipy.sparse import csr_matrix
from sklearn.decomposition import NMF
from utils import movie_to_id, id_to_movie
from utils import movies, ratings, nmf_model
from recommender import recommend_random, recommend_popular, recommend_nmf


def home_page():
    st.title("Movie Recommender")
    st.header("Welcome to the movie page by Xiaoling")
#    st.write("Welcome to my app!")
#    img = "https://storage.googleapis.com/afs-prod/media/e53811360eed4b8ba26b5f635d703a7c/3000.jpeg"
#    st.image(img, width=200)
    "Welcome to my app!"



def about_page():
    st.title("About Page")
    st.write("This app was created by Jane Doe.")


def contact_page():
    st.title("Contact Page")
    st.write("You can reach me at janedoe@example.com.")


# Navigation menu
pages_notshown = {
    "Home": home_page,
    "About": about_page,
    "Contact": contact_page
}
#page = st.sidebar.selectbox("Select a page", tuple(pages.keys()))

# Display the selected page
#pages[page]()

def left_sidebar():
    img_url = "https://storage.googleapis.com/afs-prod/media/e53811360eed4b8ba26b5f635d703a7c/3000.jpeg"
    img = Image.open(urllib.request.urlopen(img_url)) # Opens the image from the url
    with st.sidebar:
        #st.image(img, width=200, caption="")
        left_co, cent_co,last_co = st.columns(3)
        cent_co.image(img, width=150)
#        with st.echo():
#            st.write("This code will be printed to the sidebar.")
#        with st.spinner("Loading..."):
#            time.sleep(2)
#        st.success("Done!")
    # Using object notation
        st.markdown("")
        #algorithm = st.selectbox(
        algorithm = st.radio(
            "How would you like to get movie recommendations?",
            ("Random", "Highest rating", "Based on your taste"),
            key='k_radio_algo'
        )
        # Using "with" notation
        rate_range = st.select_slider(
            'Rating', 
            options=[i*0.5 for i in range(2,11)],
            value = (1, 5),
            key='k_sslider_raterange')
        movie_titles = movies.title.to_list()

        st.write('How flexible are you? (0: rigid, 2: fluid)')
        flex = st.slider('flexibility', 0, 2, value=1, key='k_flex')


        movies_select = st.multiselect(
            "Mark movies you have seen", 
            movie_titles, key='k_mselect_movies')
        col1, col2 = st.columns([3, 1])
        for i in range(5):
            movie_in = col1.selectbox(
                "", movie_titles, 
                key=f'k_sbox_movie_in{i}')
            rate_in = col2.select_slider(
                '', options=[i*0.5 for i in range(2,11)],
                value=3,
                key=f'k_sslider_rate_in{i}')



def main():
    home_page()
    left_sidebar()

    movies_rated_title = []
    movies_rated_rate = []
    for i in range(5):
        movies_rated_title.append(st.session_state[f'k_sbox_movie_in{i}'])
        movies_rated_rate.append(st.session_state[f'k_sslider_rate_in{i}'])


    algorithm = st.session_state.k_radio_algo
    rate_range = st.session_state.k_sslider_raterange
    movies_select = st.session_state.k_mselect_movies

    st.write(f'Way to give recommendation: {algorithm}')
    st.write(f'Recommended movies will have user rating between: {rate_range}')
    
    movies_select

    st.write('User rated movies and ratings:')
    movies_rated_title
    movies_rated_rate


    #background-image: url("https://yourimageurl.com");
    #background-image: "static/timothy-eberly-small.jpg";
    #    background-image: url("timothy-eberly-small.jpg");    

    background_image = '''
    <style>
    body {
        background-image: url("static/timothy-eberly-small.jpg");    
        background-size: cover;
    }
    </style>
    '''
    st.markdown(background_image, unsafe_allow_html=True)
  

if __name__ == '__main__':
    main()
