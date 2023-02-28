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



def main():
    home_page()

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
            ("Random", "Highest rating", "Based on your taste")
        )
        # Using "with" notation
        rate_range = st.select_slider(
            'Rating', 
            options=[i*0.5 for i in range(2,11)],
            value = (1, 5))
 #       rate_range_c = st.slider('Rating', 1, 5, value=(1,5))
        movie_titles = movies.title.to_list()
        
        movies_select = st.multiselect("Mark movies you have seen", movie_titles)
        col1, col2 = st.columns([3, 1])
        movies_rated_title = []
        movies_rated_rate = []
        for i in range(5):
            movie_in = col1.selectbox("Choose a movie", movie_titles)
            rate_in = col2.select_slider('', options=[i*0.5 for i in range(2,11)], value=3)
            movies_rated_title.append(movie_in)
            movies_rated_rate.append(rate_in)

    algorithm
    rate_range
#    rate_range_c
    movies_select
    movies_rated_title
    movies_rated_rate

    

    import streamlit.components.v1 as components  # Import Streamlit

    # Render the h1 block, contained in a frame of size 200x200.
    components.html("<html><body><h1>Hello, World</h1></body></html>", width=200, height=200)

    #background-image: url("https://yourimageurl.com");
    #background-image: "static/timothy-eberly-small.jpg";

    background_image = '''
    <style>
    body {
        background-image: url("timothy-eberly-small.jpg");    
        background-size: cover;
    }
    </style>
    '''

    st.markdown(background_image, unsafe_allow_html=True)
    return

    st.markdown(background_image)

    # your Streamlit code here...

    price_range = st.slider('Select price range', 20, 100, (20, 100))
    st.write('Price range:', price_range)

    countries = [
        "United States", "China", "Japan", "Germany", "United Kingdom", 
        "India", "France", "Italy", "Canada", "South Korea",
        "Russia", "Australia", "Spain", "Mexico", "Indonesia", 
        "Netherlands", "Turkey", "Switzerland", "Saudi Arabia", "Taiwan"
    ]

    selected_country = st.select_slider('Select a country', options=countries)
    st.write('Selected country:', selected_country)

    ## Data exploration 
    # Let's give a title
    st.title("Binomials Awesome Pingu 🐧 EDA ")

    # first section Penguins Dataset
    st.header("Penguins data")
    st.image("penguins.png")
    st.write("The ```palmerpenguins``` dataset contains measurements about penguins")



    # ### Task1:
    # ### Load the 'penguins_pimped.csv' file into a data frame df
    # ### Print out 5 random sample from df 
    # ### (Hint: apply the function sample() on df)

    df = pd.read_csv('./data/penguins_pimped.csv')
    df_sample = df.sample(5)

    # Let's show a dataframe in the app
    st.markdown('**Hey here a 🐧 dataframe**')
    st.dataframe(data=df_sample)

    #print(df_sample)

    ### Task2:
    ### 2.1 Determine which islands are present in the data
    island = df.island.unique()
    #print(island)

    ### 2.2 Display the data for an island you choose from the dataframe 

    my_island = 'Biscoe'

    my_island_df = df[df['island'] == my_island]

    print(my_island_df.head())

    # Adding a selectbox in combination with checkbox
    st.markdown("**Hey here you can select stuff**")

    island = st.selectbox("Select an Island", df.island.unique())
    if st.checkbox("Do you want filter the dataframe??"):
        st.dataframe(df[df['island'] == island])

    ### Task3
    ### Plotting
    ### Display a scatterplot: bill_length_mm vs bill_depth



    st.header("Some plotting")
    st.subheader("Plotting with matplotlib and seaborn")

    fig, ax = plt.subplots()
    ax = sns.scatterplot(
        data=df,
        x='bill_length_mm',
        y='bill_depth_mm',
        hue='sex'
        )
    #plt.show()
    #plt.close(fig)
    st.pyplot(fig)

    # Add a checkbox for showing the code
    if st.checkbox("Do you wanna see the code 🚴🏽‍♀️?"):
        st.markdown("""```python 
        fig, ax = plt.subplots()
        ax = sns.scatterplot(
        data=df,
        x='bill_length_mm',
        y='bill_depth_mm',
        hue='sex'
        )
        """)


    ### Click on X in the figure-window that pop up



    ### Task4
    ### Determine the average of the bill_length_mm by species
    ### Add Barchart

    st.markdown("**Hey here descriptive statistics 😎**")
    bill_length_mean = df.groupby(by='species')[['bill_length_mm']].mean()

    #print(bill_length_mean)
    st.bar_chart(bill_length_mean)


    # plotly chart

    fig = px.scatter(
        data_frame=df,
        x='bill_length_mm',
        y='bill_depth_mm',
        color="sex",
        animation_frame="species"
    )

    st.plotly_chart(fig)


    # Plotting on map 

    st.map(df)

if __name__ == '__main__':
    main()
