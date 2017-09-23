from __future__ import print_function
from collections import deque
from colorama import Fore
from featureG import convertCard
from featureG import convertChoose
from featureG import convertSituation
from testset import testset
from gamestate_maintain import update_game, end_game
from evaluate import evaluate
from ai_rules import ai_getSingleMove
from network_model import createNetwork
from enable import enable
from singlemove import model_getSingleMove2
from init import newGame
import random
import copy
import time
import numpy as np

'''
struct round:
    handCard: [15]*3   big small 2 1 K Q J 10 9 8 7 6 5 4 3
    gameinfo:   [60]
    last:    1
    lastCard:   [15]
    choose:  15
(一轮牌结束后记录)
'''



def QLearning(model_dir, learning_rate, model_size, max_epoch=10000000):
    TEST_NUM = 100
    SAVE_EPOCH = 100
    MEMORY_CAPACITY = 5000
    START_CAPCITY = 500
    BATCH_SIZE = 32
    MINIBATCH_EPOCH = 10
    GAMMA = 0.95
    START_EPSILON = 0.1
    FINAL_EPSILON = 0
    DELTA_EPSILON = 0.00005
    bestv = 57
    epsilon = START_EPSILON
    memory = []
    for i in range(50):
        memory.append(deque())
    num = [0] * 50
    model_name0 = 'Qmodel0'
    model_name1 = 'Qmodel1'
    best_name = 'Qmodel_best'

    input_size = model_size[0]
    hidden_size = model_size[1]
    choose_size = model_size[2]
    choose_extract_size = model_size[3]
    layer1_size = model_size[4]
    layer2_size = model_size[5]

    sess0 = createNetwork(input_size, hidden_size, choose_size, choose_extract_size, layer1_size, layer2_size, learning_rate)
    sess1 = createNetwork(input_size, hidden_size, choose_size, choose_extract_size, layer1_size, layer2_size, learning_rate)
    sess0.load_weights(best_name)
    sess1.load_weights(best_name)
    #with open('evaluate.log', 'a') as f:
    #    v = evaluate([sess1, 'ai1', 'ai2'], TEST_NUM, model_size)
    #    f.write('now: wins (%d/%d)\n' % (v, TEST_NUM))
    #return

    for epoch in range(max_epoch):      #一轮迭代

        if epoch >= START_CAPCITY and epoch % SAVE_EPOCH == 0:
            sess1.save_weights(model_name1)
            print('------Start evaluate------')
            with open('evaluate.log', 'a') as f:
                v = evaluate([sess1, 'ai1', 'ai2'], TEST_NUM, model_size)
                f.write('Iteration %d: wins (%d/%d)\n' % (epoch, v, TEST_NUM))
                if v >= bestv:
                    bestv = v
                    sess1.save_weights(best_name)

            sess0.load_weights(model_name1) #更新sess0参数


        if epoch >= START_CAPCITY and epsilon > FINAL_EPSILON:
            epsilon -= DELTA_EPSILON

        if(epoch % 10 == 0):
            print(Fore.GREEN + 'Epoch %d:' % (epoch))
            starttime = time.clock()

        # start a new game
        # gameinfo: landlord have, landlord send, farmer1 send, farmer2 send  15*4
        # allmessage: 15*3
        _, allmessage = newGame()
        #i = random.randint(0,99)
        #allmessage = copy.deepcopy(testset[i])
        gameinfo = [0]*60
        for i in range(0,15):
            gameinfo[4*i] = allmessage[3*i]
        memory_game_state = []
        card_on_table = [0]*16
        count = 0

        while(1):
            # Select action
            # gameinfo = [0, 0, 1, 0, 0, 1, 0, 0, 0, 3, 1, 0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 2, 1, 0, 2, 0, 1, 0, 1, 1, 1, 0, 0, 1, 2, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0]
            # card_on_table = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            # allmessage = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 2, 1, 0, 1, 0, 0, 2, 0, 0, 2, 0, 0, 1, 0, 0, 3]
            #print(gameinfo)
            round = {}
            round['handCard'] = [[0]*15,[0]*15,[0]*15]
            for i in range(0,15):
                round['handCard'][0][i] = allmessage[3*i]
                round['handCard'][1][i] = allmessage[3*i+1]
                round['handCard'][2][i] = allmessage[3*i+2]
            round['gameinfo'] = copy.deepcopy(gameinfo)
            round['last'] = card_on_table[15]
            round['lastCard'] = copy.deepcopy(card_on_table[0:15])
            memory_game_state.append(copy.deepcopy(round))
            enableCard = enable(gameinfo, card_on_table)

            if random.random() <= epsilon:
                card = random.choice(enableCard)  # 探测，从规则允许的出牌中随机选择一个
            else:
                card = model_getSingleMove2(sess1, memory_game_state, model_size, count, enableCard)  # 按照网络计算出来的出牌

            memory_game_state[-1]['choose'] = copy.deepcopy(card)
            allmessage, card_on_table, gameinfo = update_game(gameinfo, card, 0, card_on_table, allmessage)
            count += 1

            if (end_game(gameinfo)):
                r = 1
                break

            card = ai_getSingleMove(allmessage,1,card_on_table)  # 农民1
            allmessage, card_on_table, gameinfo = update_game(gameinfo, card, 1, card_on_table, allmessage)

            if (end_game(gameinfo)):
                r = -1
                break

            card = ai_getSingleMove(allmessage,2,card_on_table)  # 农民2
            allmessage, card_on_table, gameinfo = update_game(gameinfo, card, 2, card_on_table, allmessage)

            if (end_game(gameinfo)):
                r = -1
                break

        memory_game_state.append(r)
        l = len(memory_game_state)
        num[l] += 1
        memory[l].append(copy.deepcopy(memory_game_state))    # 至此打完一局牌
        for i in range(0,50):
            if len(memory[i]) > MEMORY_CAPACITY:  # 存储替换
                memory[i].popleft()
                num[i] -= 1

        # Train
        if epoch >= START_CAPCITY:
            minibatch, matchlength = ranmini(memory,num,epoch, BATCH_SIZE)

            rs = []
            for i in range(len(minibatch)):
                temp = minibatch[i]
                rs.append(temp[-1])

            # value是二位数组，第一维是哪局牌，第二维是哪步牌
            value,gameinfos,chooses = getMultiValue2(minibatch, sess0)  # value是Rt+1+λmaxaQ(St+1,a)
            # print(value)

            y_batch = []
            for i in range(len(minibatch)):
                y = []
                for turn in range(0,len(minibatch[i])-1):
                    if turn == len(minibatch[i])-2:
                        y.append([rs[i]])
                    else:
                        y.append(GAMMA * value[i][turn])
                y_batch.append(copy.deepcopy(y))


            x1 = np.zeros(shape = (BATCH_SIZE, matchlength, 1517))
            x2 = np.zeros(shape = (BATCH_SIZE, matchlength, 474))
            targets = np.zeros(shape=(BATCH_SIZE,matchlength, 1))

            for i in range(0, BATCH_SIZE):
                for j in range(0, matchlength-1):
                    for k in range(0, 1517):
                        x1[i][j][k] = gameinfos[i][j][k]
                    for k in range(0, 474):
                        x2[i][j][k] = chooses[i][j][k]
                    targets[i][j][0] = y_batch[i][j][0]
            ###### change 3
            sess1.fit([x1,x2], targets, nb_epoch=MINIBATCH_EPOCH, verbose=0)

        if (epoch % 10 == 9):
            endtime = time.clock()
            interval = endtime - starttime
            print(Fore.YELLOW + 'Epoch %d end; %fs' % (epoch, interval))


def ranmini(memory,num,epoch, BATCH_SIZE):
    while(1):
        sp = random.randint(0,epoch)
        i = 0
        while(sp >= 0):
            sp -= num[i]
            i+=1
        if(len(memory[i])>BATCH_SIZE):
            break
    minibatch = random.sample(memory[i], BATCH_SIZE)  # 随机选择一些进入minibatch
    return minibatch, i


def distract2(l1,l2):
    l = len(l2[0])
    ans = []
    for k in range(0,len(l1)):
        t = [0]*l
        for i in range(0,l):
            t[i] = l1[k][4*i]-l2[k][i]
        ans.append(t)
    return ans


def getMultiValue2(minibatch, sess):
    values = []
    A = []
    B = []
    for i in range(0,len(minibatch)):
        rounds = minibatch[i]
        gameinfos = []
        chooses = []
        for j in range(0,len(rounds)-1):
            gameinfo = convertSituation(rounds[j])
            choose = convertChoose(rounds[j],rounds[j]['choose'])
            gameinfos.append(copy.deepcopy(gameinfo))
            chooses.append(copy.deepcopy(choose))
        value = [0] * len(gameinfos)
        A.append(gameinfos)
        B.append(chooses)
        ####### change 2
        a = sess.predict([np.array([gameinfos]), np.array([chooses])], batch_size=1, verbose=0)
        for j in range(0, len(gameinfos) - 1):
            value[j] = a[0][j+1]
        values.append(copy.deepcopy(value))

    return values,A,B


if __name__ == "__main__":
    QLearning('/home/yukeyi/Desktop/lstm/old_data', 0.0005, [1517,200,474,100,30,10])
'''
    input_size = model_size[0]
    hidden_size = model_size[1]
    choose_size = model_size[2]
    choose_extract_size = model_size[3]
    layer1_size = model_size[4]
    layer2_size = model_size[5]
'''
