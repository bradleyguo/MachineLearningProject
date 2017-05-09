import pandas as pd
import numpy as np
# ref: http://stackoverflow.com/questions/24147278/how-do-i-create-test-and-train-samples-from-one-dataframe-with-pandas
df = pd.read_table('data_1m/ratings.csv', header=0, sep=',', names=['user_id', 'movie_id', 'rating', 'timestamp'])
msk = np.random.rand(len(df)) < 0.8
print(msk)
train = df[msk]
test = df[~msk]
print(test.head())
print(train.head())
train.to_csv()