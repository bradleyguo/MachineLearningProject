import pandas as pd
import numpy as np
from tqdm import tqdm
import math
from sklearn.preprocessing import normalize

# prediction based on test data:
# also examine the RMSE of our prediction
movie_genres = pd.read_table('movie_genres.csv', header=0, sep=',')
#user_columns = ['user_id','movie_id','rating','timestamp','movie_title','Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','IMAX','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']
user_preferences = pd.read_table('user_preference.csv', header=0, sep=',')
preference_weight = pd.read_table('preference_weight.csv', header=0, sep=',')
rating_genres_test = pd.read_table('rating_genres_test.csv', header=0, sep=',')
global_average = pd.read_table('global_average.csv', header=0, sep=',')
movie_categories = movie_genres.columns[2:]
#print(len(movie_categories))

def dot_product(vector_1, vector_2, weight):
	total_weight = 0.0
	valid_weight = []
	non_weight = []
	use_average = []
	inx = 0
	non_appear_sum = 0.0
	appear_sum = 0.0
	sum = 0.0
	#print(vector_1, vector_2, weight)
	for i, j in zip(vector_1, vector_2):
		#print("q",i)
		if(i != 0 and j!=0):
			non_weight.append(i*j)
			total_weight += weight[inx]
			valid_weight.append(weight[inx])
		else:
			if (i != 0 and j == 0):
				#print("this genre is not recorded in the user's profile, use global average instead")
				# since they also dont appear in weight dataset
				use_average.append(global_average.iloc[0,inx])
				print(inx)
				print(global_average.iloc[0, inx])
		inx += 1

	if total_weight != 0:
		for i in range(len(valid_weight)):
			appear_sum += non_weight[i] * valid_weight[i] / total_weight
	# the multiplier could be adjusted:
	# consider those datapoints that did not appear in the user's profile
	if len(use_average)!=0:
		print(len(use_average))
		print(use_average)
		for non_appear in use_average:
			non_appear_sum += non_appear
		print("non appear sum: ", non_appear_sum)
		non_appear_sum = non_appear_sum / len(use_average)
		print("non appear sum after average: ", non_appear_sum)
	if non_appear_sum == 0:
		sum = appear_sum
	else:
		if appear_sum == 0:
			sum = non_appear_sum
		else:
			sum = (non_appear_sum+appear_sum)/2
	print(non_appear_sum)
	print(appear_sum)
	print("final prediction: ", sum)
	# error detection
	if sum == 0:
		exit(1)
	return sum

count = 0
square_loss = 0.0
for user_id in tqdm(rating_genres_test.user_id.unique()):
	print("user_id: ", user_id)
	user_preference = user_preferences[user_preferences["user_id"]==user_id].iloc[0, 1:]
	user_weight = preference_weight[preference_weight["user_id"] == user_id].iloc[0, 1:]
	inxs = rating_genres_test["user_id"] == user_id
	#print(rating_genres_test[inxs])
	# movies for this user in the test dataset
	this_user = rating_genres_test[inxs]

	this_user_scores = []
	for _, row in this_user.iterrows():
		count += 1
		#print(row.ix[5:23])
		#print("index: ", index)
		#print("user: %d, the film: "%user_id, row["movie_id"])
		score = dot_product(row.ix[5:24].values, user_preference.values, user_weight.values)
		#if math.isnan(score):
		#	print(row.ix[5:24].values)
		#	print(user_preference.values)
		#	print(user_weight.values)
		#	exit(1)
		#compute the square loss:
		#print("score: ", score)
		#print("rating: ", row["rating"])
		#print(abs(score-row["rating"])**2)
		square_loss += abs(score-row["rating"])**2
		#print(square_loss)
		#print(score[0])
		this_user_scores.append(score)
		#rating_genres_test.set_value(index, "score", score[0])
	# normalize to 0-5
	#this_user_score = np.array(this_user_scores)
	#this_user_norm = 5*(normalize(this_user_score[:,np.newaxis], axis=0).ravel())
	#this_user_score_list = this_user_score.tolist()
	i = 0
	for index, row in this_user.iterrows():
		rating_genres_test.set_value(index, "score", this_user_scores[i])
		i += 1
	#print("i'm done")
	#print(rating_genres_test[rating_genres_test["user_id"]==user_id]["score"])
	#movies_test = rating_genres_test[rating_genres_test["user_id"]==user_id].iloc[:,5:]
	#print(movies_test)
	#scores = np.dot(rating_genres_test[inxs][movie_categories].values, user_preference.values.T)
	#rating_genres_test = rating_genres_test[inxs].assign(score=pd.Series(scores.flatten()))
	#print(scores)
	#print(user_preference)
#print(get_movie_recommendations(first_user_preference, 10))
print(square_loss)
print(count)
RMSE = math.sqrt(square_loss/count)
print("RMSE: ", RMSE)
rating_genres_test.to_csv('rating_genres_test_predict.csv', index=False, sep=',', encoding='utf-8')
