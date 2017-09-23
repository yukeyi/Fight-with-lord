from keras.models import Sequential
from keras.layers import Dense, Activation

def createNet():
    model = Sequential()
    model.add(Dense(32, input_shape=(784,)))
    model.add(Activation('relu'))
    model.compile(loss='mean_squared_error', optimizer='adam')  # 编译模型
    return model

sess0 = createNet()
sess1 = createNet()
sess0.set_weights(sess1.get_weights())
a = 1