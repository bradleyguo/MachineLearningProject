import pandas as pd
import numpy as np
from tqdm import tqdm
from numpy import linalg as LA

genres_col = ['Action','Adventure','Animation',"Children",'Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','IMAX','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']
#movies_df = pd.read_table('data_1m/movies.dat', header=0, sep=',', names=['movie_id', 'movie_title', 'movie_genre'])
#user_columns = ['user_id','movie_id','rating','timestamp','movie_title','Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','IMAX','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']
users_df = pd.read_table('rating_genres_train.csv', header=0, sep=',')
# multiply the rating score to the genre vector to generate
# this users preference vector:
#for i in tqdm(range(len(users_df.rating))):
#	users_df.iloc[i, 5:] = users_df.rating[i] * users_df.iloc[i, 5:]
users_df.iloc[:,5:] = users_df.iloc[:,5:].apply(lambda x: users_df["rating"]*x)
#print(users_df.head())
#print(users_df.columns)

preference_res = []
weight_res = []
rating_global = [0.0 for _ in range(len(genres_col))] # compute the global average for each genre
user_count = [0 for _ in range(len(genres_col))] # record the valid user count for each genre
for user_id in tqdm(users_df.user_id.unique()):
	this_user_preference = (user_id,)
	this_user_weight = (user_id,)
	preference_nonweight = np.zeros(len(genres_col))
	#preference_weight = np.zeros(len(genres_col))
	weight = np.zeros(len(genres_col))
	#normalize to 0-5
	#multiply the weight
	# first 0 is not considered
	this_user_df = users_df.loc[users_df['user_id'] == user_id]
	#print(len(this_user_df))
	for i, col in enumerate(genres_col):
		valid = this_user_df.loc[this_user_df[col] != 0]
		if len(valid) == 0:
			#preference_weight[i] = 0.0
			preference_nonweight[i] = 0.0 # means that there's no corresponding datapoint
		else:
			#preference_weight[i] = valid[col].mean(axis=0) * len(valid) / len(this_user_df)
			weight[i] = len(valid) / len(this_user_df)
			mean = valid[col].mean(axis=0)

			rating_global[i] += mean
			user_count[i] += 1
			preference_nonweight[i] = mean
		#print(this_user_df.loc[this_user_df[col] != 0][col].mean(axis=0))
	#print(preference_nonweight)
	# preserve the norm of the vector
	#print("non",preference_nonweight)
	#print("weight",weight)
	for i in range(len(preference_nonweight)):
		this_user_preference += (preference_nonweight[i],)
	preference_res.append(this_user_preference)
	for i in range(len(weight)):
		this_user_weight += (weight[i],)
	weight_res.append(this_user_weight)
	#print(res)

for i in range(len(rating_global)):
	rating_global[i] = rating_global[i] / user_count[i]
average = []
average.append(tuple(rating_global))
global_average = pd.DataFrame.from_records(average, columns=genres_col)
#print(rating_global)

global_average.to_csv('global_average.csv', index=False, sep=',', encoding='utf-8')
user_preference = pd.DataFrame.from_records(preference_res, columns=['user_id']+genres_col)
preference_weight = pd.DataFrame.from_records(weight_res, columns=['user_id']+genres_col)
#print(user_preference.head())
user_preference.to_csv('user_preference.csv', index=False, sep=',', encoding='utf-8')
preference_weight.to_csv('preference_weight.csv', index=False, sep=',', encoding='utf-8')
