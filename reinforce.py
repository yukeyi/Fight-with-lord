import tensorflow as tf
import numpy as np

input = [100,20,0.1,1000] # layer1 layer2 lr iterate_time

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

def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs})
    result = np.linalg.norm(y_pre - v_ys)
    #print(y_pre)
    return result

# define placeholder for inputs to network
xs = tf.placeholder(tf.float32, [None, input[0]])  # hidden node
ys = tf.placeholder(tf.float32)

# add output layer
temp = add_layer(xs, input[0], input[1],  activation_function=tf.nn.sigmoid)
prediction = add_layer(temp, input[1], 1,  activation_function=tf.nn.sigmoid)

# the error between prediction and real data
loss = (ys - prediction) ** 2

train_step = tf.train.GradientDescentOptimizer(input[2]).minimize(loss)
sess = tf.Session()
# important step
# tf.initialize_all_variables() no long valid from
# 2017-03-02 if using tensorflow >= 0.12
if int((tf.__version__).split('.')[1]) < 12 and int((tf.__version__).split('.')[0]) < 1:
    init = tf.initialize_all_variables()
else:
    init = tf.global_variables_initializer()
sess.run(init)

batch_ys = [0.5, 0.9, 0.1, 0.4]
batch_xs = [np.random.random(input[0]) for _ in batch_ys]

for i in range(input[3]):
    sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys})
    if i % 50 == 0:
        print(compute_accuracy(batch_xs, batch_ys))
