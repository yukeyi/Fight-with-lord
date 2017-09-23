from __future__ import print_function
import copy
from featureG import convertSituation
from featureG import convertChoose
import numpy as np

def model_getSingleMove2(sess, round, model_size,count,enablecard):
    l = len(round)
    temp_game_state = []
    for i in range(0,l):
        temp_game_state.append(convertSituation(round[i]))
    value = []

    card_choose = []
    for i in range(0,count+1):
        card_choose.append([0]*model_size[2])

    for choose in enablecard:
        card_choose[count] = convertChoose(round[count],choose)
        a = sess.predict([np.array([temp_game_state]), np.array([card_choose])], batch_size=1, verbose=0)
        value.append(a[0][count])

    i = np.argmax(value)
    return enablecard[i]


def distract(l1,l2):
    l = len(l2)
    t = [0]*l
    for i in range(0,l):
        t[i] = l1[4*i]-l2[i]
    return t