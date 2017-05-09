# this module is to transform the dat dataset to a standard "," csv
# and split train test
import pandas as pd
import numpy as np

movies_df = pd.read_table('movies.dat', header=None, sep='::', names=['movie_id', 'movie_title', 'movie_genre'])
ratings_df = pd.read_table('ratings.dat', header=None, sep='::', names=['user_id', 'movie_id', 'rating', 'timestamp'])
users_df = pd.read_table('users.dat', header=None, sep='::', names=['user_id', 'gender', 'age', 'occupation', 'zipcode'])

movies_df.to_csv('movies.csv', index=False, sep=',', encoding='utf-8')
ratings_df.to_csv('ratings.csv', index=False, sep=',', encoding='utf-8')
users_df.to_csv('users.csv', index=False, sep=',', encoding='utf-8')
