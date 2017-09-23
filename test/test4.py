from __future__ import print_function
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers import LSTM, Embedding
from keras.layers import Merge
from collections import deque
from colorama import Fore
import copy
import time
import numpy as np

np.random.seed(0)
y_train = np.random.random(size=(1, 4, 1))
x1_train = np.random.random(size=(1, 4, 10))

def my_init(shape):
    #temp = keras.initializers.Constant(value=0)
    #return temp
    return np.array([0.2, 0.2, 0.2, 0.2, 0.2])

model_LSTM = Sequential()  # 层次模型
#model_LSTM.add(LSTM(5, kernel_initializer=keras.initializers.Constant(value=0.3), input_dim=10, input_length=4, return_sequences=True, activation='sigmoid', name = 'yukeyi'))
#model_LSTM.add(LSTM(5, input_dim=10, kernel_initializer=my_init(5),input_length=4, return_sequences=True, activation='sigmoid', name = 'yukeyi'))
model_LSTM.add(LSTM(5, input_dim=10, input_length=4, return_sequences=True, activation='sigmoid', name = 'yukeyi'))
#model_LSTM.add(Dense(1))
model_LSTM.compile(loss='mean_squared_error', optimizer='adam')  # 编译模型
#print(model_LSTM.input_shape)
#print(model_LSTM.output_shape)
#b = model_LSTM.get_layer(name = 'yukeyi')
#print(b)
a = model_LSTM.predict(x1_train, batch_size=1, verbose=0)
print(a)
model_LSTM.reset_states = np.array([1,2,3,4,5])
a = model_LSTM.predict(x1_train, batch_size=1, verbose=0)
print(a)
config = model_LSTM.get_config()