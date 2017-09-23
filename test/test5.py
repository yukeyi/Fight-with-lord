### 验证了mask层的作用

from __future__ import print_function
import keras
from keras.models import Sequential
from keras.layers import Masking
from keras.layers.core import Dense, Activation
from keras.layers import LSTM, Embedding
from keras.layers import Merge
from collections import deque
from colorama import Fore
import copy
import time
import numpy as np

batch_size = 1
il = 5

x1_train = np.array([[[1,2,1,2,1],[2,3,2,1,2]]])
x2_train = np.array([[[1,1,1,1,1],[1,2,1,2,1],[2,3,2,1,2]]])
#x1_train = np.random.random(size=(1,4,5))

model_LSTM = Sequential()  # 层次模型
#model_LSTM.add(Embedding(1000, ol, input_length=il,mask_zero=True))
#model_LSTM.add(Masking(mask_value=0, input_shape=(4,5)))
model_LSTM.add(LSTM(1, input_dim=5, return_sequences=True, activation='sigmoid', name = 'yukeyi'))
model_LSTM.compile(loss='mean_squared_error', optimizer='adam')  # 编译模型
a = model_LSTM.predict(x1_train, batch_size=1, verbose=0)
b = model_LSTM.predict(x2_train, batch_size=1, verbose=0)
print(a)
print(b)
