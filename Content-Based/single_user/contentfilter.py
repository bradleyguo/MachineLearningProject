import pandas as pd
import numpy as np
movies_df = pd.read_table('data_1m/movies.dat', header=0, sep='::', names=['movie_id', 'movie_title', 'movie_genre'])
#user_columns = ['user_id','movie_id','rating','timestamp','movie_title','Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','IMAX','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']
users_df = pd.read_table('data_1m/users_df.csv', header=0, sep='::')

for i in range(len(users_df.rating)):
	users_df.iloc[i, 5:] = users_df.rating[i] * users_df.iloc[i, 5:]

print(users_df.head())
#print(users_df.columns)
genres_col = ['Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','IMAX','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']
user_preference = pd.DataFrame(columns=['user_id']+genres_col)
for idx, user_id in enumerate(users_df.user_id.unique()):
	user_preference.set_value(idx, 'user_id', user_id)
	for col in genres_col:
		user_preference.set_value(idx, col, users_df.loc[users_df['user_id'] == user_id][col].mean(axis=0))

print(user_preference.head())
user_preference.to_csv('user_preference.csv', index=False, sep=',', encoding='utf-8')

#predict