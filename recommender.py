"""
Movie Recommender

Three recommending algorithms are implemented:
1. random
2. best rating
3. NMF
"""

import random
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.decomposition import NMF


def recommend_random(query, ratings, k=10):
   """
   Filters and recommends k random movies for any given input query.
   Returns a list of k movie ids    
   """
   # 1. candidate generation    
   # filter out movies that the user has allready seen
   movies_seen = list(query.keys())
   ratings = ratings[~ratings.movieId.isin(movies_seen)]

   # calculate a random sample of movies: 
   movies = list(set(ratings.movieId))
   recommendation = random.sample(movies, k)

   return recommendation  


def recommend_popular(query, ratings, k=10):
    """
    Filters and recommends the top k movies for any given input query. 
    Returns a list of k movie ids.
    """
    
    # filter out movies that the user has allready seen
    movies_seen = list(query.keys())
    ratings = ratings[~ratings.movieId.isin(movies_seen)]

    # filter out movies that have been watched by less than 20/50/100... users
    seen = ratings.movieId.value_counts().loc[lambda x: x > 50]
    ratings = ratings.loc[ratings.movieId.isin(seen)]
   
    # rank by the average rating for each movie
    score = ratings.groupby('movieId').rating.mean()
    ranking = score.sort_values(ascending=False)

    # return the top-k highst rated movie ids or titles
    recommendation = list(ranking.index[list(range(k))])

    return recommendation


def recommend_nmf(query, model, k=10):
   """
   Filters and recommends the top k movies for any given input query based on a trained NMF model. 
   Returns a list of k movie ids.
   """

   # 1. candiate generation
   # construct a user vector, needs to have the same format as the training data
   data = list(query.values())      # the ratings of the new user
   row_ind = [0]*len(data)          # we use just a single row 0 for this user
   col_ind = list(query.keys())     # the columns (=movieId) of the ratings
   n_col = model.n_features_in_
   user_vec = csr_matrix((data, (row_ind, col_ind)), shape=(1, n_col))

   # calculate the score with the NMF model
   scores = model.inverse_transform(model.transform(user_vec))
   scores = pd.Series(scores[0])

   # filter out movies user has seen by setting their ratings to 0
   scores[col_ind] = 0
   scores = scores.sort_values(ascending=False)

   # return the top-k highst rated movie ids or titles
   recommendations = list(scores.head(k).index)

   return recommendations


def test():
   """ Test function """

   import pandas as pd
   import pickle

   # load modvies and model
   movies = pd.read_csv('data/movies.csv')
   ratings = pd.read_csv('data/ratings.csv')
   model_file = 'models/nmf_recommender.pkl'
   with open(model_file, 'rb') as file:
      model = pickle.load(file)

   # test query
   query = {
      50:5,
      47:5,
      111:5,
      150:5,
      191:5,
      364:5,
      523:3,
      608:5,
      6565:5,
      33004:4,
      155743:3
   }
   movies_rated = movies.set_index('movieId').loc[query.keys()]

   # call the recommender
   recomm = recommend_random(query, ratings)
   movies_recomm_ran = movies.set_index('movieId').loc[recomm]   
   recomm = recommend_popular(query, ratings, k=10)
   movies_recomm_pop = movies.set_index('movieId').loc[recomm]
   recomm = recommend_nmf(query, model, k=20)
   movies_recomm_nmf = movies.set_index('movieId').loc[recomm]
   
   print('\n\nUser has rated these movies:')
   print('----------------------------------------')
   print(movies_rated.reset_index()[['title', 'genres']])

   print('\n\nMovies recommended randomly:')
   print('----------------------------------------')
   print(movies_recomm_ran.reset_index()[['title', 'genres']])

   print('\n\nMost popular movies:')
   print('----------------------------------------')
   print(movies_recomm_pop.reset_index()[['title', 'genres']])

   print('\n\nMovies recommended based on user\'s taste:')
   print('----------------------------------------')
   print(movies_recomm_nmf.reset_index()[['title', 'genres']])
   print('')


if __name__ == ('__main__'):
   test()
