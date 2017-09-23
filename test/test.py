import numpy as np
import tensorflow as tf
from lstm import LstmParam, LstmNetwork

global myParam
# [inputNumber, cellNumber, iterNumber]
myParam = [63, 100, 100]
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
loss2 = (ys - prediction) ** 2

train_step = tf.train.GradientDescentOptimizer(input[2]).minimize(loss2)
sess = tf.Session()
# important step
# tf.initialize_all_variables() no long valid from
# 2017-03-02 if using tensorflow >= 0.12
if int((tf.__version__).split('.')[1]) < 12 and int((tf.__version__).split('.')[0]) < 1:
    init = tf.initialize_all_variables()
else:
    init = tf.global_variables_initializer()
sess.run(init)



class ToyLossLayer:
    """
    Computes square loss with first element of hidden layer array.
    """
    global myParam

    @classmethod
    def loss(self, pred, label):
        return (np.mean(pred) - label) ** 2

    @classmethod
    def bottom_diff(self, pred, label):
        diff = np.zeros_like(pred)
        for i in range(0,myParam[1]):
          diff[i] = (np.mean(pred) - label) / myParam[0]
        return diff

def example_0():
    global myParam
    # learns to repeat simple sequence from random inputs
    np.random.seed(0)

    # parameters for input data dimension and lstm cell count 
    mem_cell_ct = myParam[1]
    x_dim = myParam[0]
    lstm_param = LstmParam(mem_cell_ct, x_dim) 
    lstm_net = LstmNetwork(lstm_param)
    y_list = [-0.5,0.2,0.1, 0.5]
    input_val_arr = [np.random.random(x_dim) for _ in y_list]
    # only four data
    for cur_iter in range(myParam[2]):
        #print("cur iter: " + str(cur_iter))
        for ind in range(len(y_list)):
            lstm_net.x_list_add(input_val_arr[ind])   # calculate the current value of the network when input sequence is the input_val_arr and output sequence is y_list
            #print("y_pred[" + str(ind) + "] : " + str(lstm_net.lstm_node_list[ind].state.h[0]))  # the value is in h[0]

        loss = lstm_net.y_list_is(y_list, ToyLossLayer) # Toy is the rule of loss, calculate the current loss
        #print("loss: " + str(loss))
        lstm_param.apply_diff(lr=0.1) # update param of network
        lstm_net.x_list_clear()

    batch_xs = []
    for ind in range(len(y_list)):
        lstm_net.x_list_add(input_val_arr[ind])
    for ind in range(len(y_list)):
        batch_xs.append(lstm_net.lstm_node_list[ind].state.h)
    batch_ys = y_list
    for i in range(input[3]):
        sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys})
        if i % 50 == 0:
            print(compute_accuracy(batch_xs, y_list))





if __name__ == "__main__":
    example_0()

