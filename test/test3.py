from __future__ import print_function
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers import LSTM, Embedding
import numpy as np
from keras.layers import Merge

input_data_1 = np.random.random(size=(10,784))
input_data_2 = np.random.random(size=(10,784))
targets = np.random.random(size=(10,1))

left_branch = Sequential()
left_branch.add(Dense(32, input_dim=784))

right_branch = Sequential()
right_branch.add(Dense(32, input_dim=784))

merged = Merge([left_branch, right_branch], mode='concat')

final_model = Sequential()
final_model.add(merged)
#print(final_model.input_shape)
final_model.add(Dense(1, activation='sigmoid'))

final_model.compile(loss='mean_squared_error', optimizer='adam')  # 编译模型
final_model.fit([input_data_1, input_data_2], targets, nb_epoch=100)  # we pass one data array per model input

