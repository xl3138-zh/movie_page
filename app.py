""" main file for application """
import random
from flask import Flask
from flask import render_template
from flask import request

#import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.decomposition import NMF
from utils import movie_to_id, id_to_movie
from utils import movies, ratings, nmf_model
from recommender import recommend_random, recommend_popular, recommend_nmf
#from recommender import recommend_nmf_test

app = Flask(__name__)

@app.route('/')
def index():
#    return render_template('index.html', title='Hello, World!')
    return render_template('index.html', name='Xiaoling', movies = movies.title.to_list())


@app.route('/recommender/')
def recommender():
    choice = request.args['algo']
    #print(request.args)
    if True:       
        m_titles = request.args.getlist('title')
        m_ratings = request.args.getlist('Ratings')
       
        #print(m_titles)
        #print(m_ratings)
        movie_ids = [movie_to_id(title) for title in m_titles]
        movie_ratings = [int(mr) for mr in m_ratings]
        query = dict(zip(movie_ids, movie_ratings))

        #print(user_input)
        print('query: ', query)
        print('choice: ', choice)
    if choice =='random':
        recomm = recommend_random(query, ratings)
        reason = 'randomly'
    elif choice =='rating':
        recomm = recommend_popular(query, ratings)
        reason = 'based on highest viewer rating'
    else:
        recomm = recommend_nmf(query, nmf_model, k=10)
        reason = 'based on your taste'

    movies_watched = movies.set_index('movieId').loc[movie_ids].title
    movies_recomm = movies.set_index('movieId').loc[recomm].title


    print(movies_watched)
    print('Recommended movies:')
    print(movies_recomm)
    print('reason: ', reason)

    return render_template(
        'recommendations.html',
        movies_done = movies_watched,
        movies = movies_recomm,
        reason = reason
        )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
