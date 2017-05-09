import pandas as pd
import numpy as np

movies_df = pd.read_table('movies.csv', header=0, sep=',', names=['movie_id', 'movie_title', 'movie_genre'])
users_df = pd.read_table('singleuserrating.csv', header=0, sep=',', names=['user_id', 'movie_id', 'rating', 'timestamp'])

#print(movies_df[0:3].head())
group = users_df.groupby(["user_id"])
print(group.get_group(1))
'''
movies_df = movies_df[movies_df['movie_genre']!='(no genres listed)']
# we convert the movie genres to a set of dummy variables
movies_df = pd.concat([movies_df, movies_df.movie_genre.str.get_dummies(sep='|')], axis=1)
#print(movies_df[0:3].head())

movie_genres = pd.concat([movies_df.iloc[:,0:2],movies_df.iloc[:,3:]], axis=1)

#print(movie_genres.head())
users_df = pd.merge(users_df, movie_genres, on='movie_id', how='inner')
#print(users_df.head())
users_df.to_csv('users_df.csv', index=False, sep=',', encoding='utf-8')
movie_genres.to_csv('movie_genres.csv', index=False, sep=',', encoding='utf-8')
'''
