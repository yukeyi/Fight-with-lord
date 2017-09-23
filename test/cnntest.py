# encoding=utf-8
__author__ = 'yukeyi'
import tensorflow as tf
import numpy as np

def add_layer(inputs, in_size, out_size, activation_function=None,):
    # add one more layer and return the output of this layer
    Weights = tf.Variable(tf.random_normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1,)
    Wx_plus_b = tf.matmul(inputs, Weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b,)
    return outputs

def createData(dim, dataNum):
    train_y = [np.random.random(dataNum)]
    train_x = [np.random.random(dim) for _ in train_y]
    return train_x, train_y


def linerRegression(train_x, train_y, epoch=1000, rate=0.00001):
    train_x = np.array(train_x)
    train_y = np.array(train_y)
    x = tf.placeholder(tf.float32, [None, 10])
    y = tf.placeholder("float")

    pred = add_layer(x, 10, 1, activation_function=tf.nn.sigmoid)
    #pred = tf.add(tf.multiply(x, w), b)
    loss = tf.reduce_sum(tf.pow(pred - y, 2))
    optimizer = tf.train.GradientDescentOptimizer(rate).minimize(loss)

    init = tf.initialize_all_variables()
    sess = tf.Session()
    sess.run(init)

    for index in range(epoch):
        # for tx,ty in zip(train_x,train_y):
        # sess.run(optimizer,{x:tx,y:ty})
        sess.run(optimizer, {x: train_x, y: train_y})
        #print('w is ',sess.run(w))
        #print 'b is ',sess.run(b)
        #print 'pred is ',sess.run(pred,{x:train_x})
        print('loss is ',sess.run(loss,{x:train_x,y:train_y}))
        # print '------------------'
    print('loss is ', sess.run(loss, {x: train_x, y: train_y}))


def predictionTest(test_x, test_y, w, b):
    W = tf.placeholder(tf.float32)
    B = tf.placeholder(tf.float32)
    X = tf.placeholder(tf.float32)
    Y = tf.placeholder(tf.float32)
    pred = tf.add(tf.multiply(X, W), B)
    loss = tf.reduce_mean(tf.pow(pred - Y, 2))
    sess = tf.Session()
    loss = sess.run(loss, {X: test_x, Y: test_y, W: w, B: b})
    return loss


if __name__ == "__main__":
    train_x, train_y = createData(10,4)
    linerRegression(train_x, train_y)
    #loss = predictionTest(train_x, train_y, w, b)
    #print(loss)

