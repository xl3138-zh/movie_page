"""
UTILS 
- Helper functions to use for your recommender funcions, etc
- Data: import files/models here e.g.
    - movies: list of movie titles and assigned cluster
    - ratings
    - user_item_matrix
    - item-item matrix 
- Models:
    - nmf_model: trained sklearn NMF model
"""
import pandas as pd
import numpy as np
import pickle

movies = pd.read_csv('data/movies.csv') 
ratings = pd.read_csv('data/ratings.csv')
model_file = 'models/nmf_recommender.pkl'
with open(model_file, 'rb') as file:
    nmf_model = pickle.load(file)

def movie_to_id(string_titles):
    '''
    converts movie title to id for use in algorithms'''
    
    movieID = movies.set_index('title').loc[string_titles]['movieId']
    movieID = movieID.tolist()
    
    return movieID

def id_to_movie(movieID):
    '''
    converts movie Id to title
    '''
    rec_title = movies.set_index('movieId').loc[movieID]['title']
    
    return rec_title


def test():
    m_titles = ['Tom and Huck (1995)', 'Chungking Express (Chung Hing sam lam) (1994)', 'Serendipity (2001)']
    print([movie_to_id(mt) for mt in m_titles])
    print([id_to_movie(movie_to_id(mt)) for mt in m_titles])


if __name__ == "__main__":
    test()
