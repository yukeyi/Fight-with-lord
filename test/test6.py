import keras.backend as K
from keras.layers import LSTM, Input

I = Input(shape=(None, 200)) # unknown timespan, fixed feature size
lstm = LSTM(20)
f = K.function(inputs=[I], outputs=[lstm(I)])

import numpy as np
data1 = np.random.random(size=(1, 100, 200)) # batch_size = 1, timespan = 100
print(f([data1])[0].shape)
# (1, 20)

data2 = np.random.random(size=(1, 314, 200)) # batch_size = 1, timespan = 314
print(f([data2])[0].shape)
# (1, 20)