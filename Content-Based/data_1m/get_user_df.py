import pandas as pd
import numpy as np

movies_df = pd.read_table('movies.csv', header=0, sep=',', names=['movie_id', 'movie_title', 'movie_genre'])
#movies_df = pd.read_table('data_100k/movies.csv', header=0, sep=',', names=['movie_id', 'movie_title', 'movie_genre'])
user_ratings_train = pd.read_table('ratings_train.csv', header=0, sep=',', index_col=0, names=['user_id', 'movie_id', 'rating', 'timestamp'])
user_ratings_test = pd.read_table('ratings_test.csv', header=0, sep=',', index_col=0, names=['user_id', 'movie_id', 'rating', 'timestamp'])
#user_ratings_train = pd.read_table('data_100k/ratings_train.csv', header=0, sep=',', index_col=0, names=['user_id', 'movie_id', 'rating', 'timestamp'])
#user_ratings_test = pd.read_table('data_100k/ratings_test.csv', header=0, sep=',', index_col=0, names=['user_id', 'movie_id', 'rating', 'timestamp'])
#print(movies_df[0:3].head())
#print(user_ratings_test[0:3].head())

movies_df = movies_df[movies_df['movie_genre']!='(no genres listed)']
# we convert the movie genres to a set of dummy variables
movies_df = pd.concat([movies_df, movies_df.movie_genre.str.get_dummies(sep='|')], axis=1)
#print(movies_df[0:3].head())

movie_genres = pd.concat([movies_df.iloc[:,0:2],movies_df.iloc[:,3:]], axis=1)

#print(movie_genres.head())
# join the movie table with the user rating table
ratings_train = pd.merge(user_ratings_train, movie_genres, on='movie_id', how='left', sort=False)
#ratings_train.groupby("user_id")

ratings_test = pd.merge(user_ratings_test, movie_genres, on='movie_id', how='left')
#print(users_df.head())
# ratings but with genre columns
ratings_train.to_csv('rating_genres_train.csv', index=False, sep=',', encoding='utf-8')
ratings_test.to_csv('rating_genres_test.csv', index=False, sep=',', encoding='utf-8')
movie_genres.to_csv('movie_genres.csv', index=False, sep=',', encoding='utf-8')
