import pandas as pd
import numpy as np

movie_genres = pd.read_table('movie_genres.csv', header=0, sep=',')
#user_columns = ['user_id','movie_id','rating','timestamp','movie_title','Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','IMAX','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']
user_preferences = pd.read_table('user_preference.csv', header=0, sep=',')
movie_categories = movie_genres.columns[2:]
#print(len(movie_categories))
# let's only consider the first user:
first_user_preference = user_preferences.iloc[0:1, 1:]
print(type(first_user_preference.values))
recommend = pd.DataFrame(columns=['movie_id', 'movie_title', 'score'])
recommend['movie_id'] = movie_genres['movie_id']
recommend['movie_title'] = movie_genres['movie_title']

def dot_product(vector_1, vector_2):
    return sum([i*j for i,j in zip(vector_1, vector_2)])

def get_movie_score(movie_features, user_preferences):
    return dot_product(movie_features, user_preferences)

def get_movie_recommendations(user_preference, n_recommendations):
    #we add a column to the movies_df dataset with the calculated score for each movie for the given user
    #print((movie_genres[movie_categories]))
    #print(len(user_preference.values.T))
    #print(movie_genres[movie_categories].values.shape)
    matrix = np.dot(movie_genres[movie_categories].values, user_preference.values.T)
    #recommend['score'] = movie_genres[movie_categories].apply(lambda row: np.dot(row.reshape(-1,1), user_preference.values), axis=1)
    #print(matrix.shape[0])
    for i in range(matrix.shape[0]):
        #print(matrix[i])
        recommend.set_value(i, 'score', matrix[i][0])
    print(recommend['score'])
    recommend.sort_values(by=['score'], ascending=False)
    recommend.to_csv('recommend_first.csv', sep=',', encoding='utf-8')
    return recommend.sort_values(by=['score'], ascending=False)['movie_title'][:n_recommendations]

print(get_movie_recommendations(first_user_preference, 10))
