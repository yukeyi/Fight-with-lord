from __future__ import print_function
import os
import random
import copy
import numpy as np

def load_testdata(filename):
    data = []
    for line in open(filename):
        temp = list(line)
        temp.pop()
        temp = [int(x) for x in temp]
        data.append(copy.deepcopy(temp))
    return data

def geninitdata(filename):
    if os.path.exists(filename):
        return load_testdata(filename)

    data = []
    for i in range(0,1000):
        _, onedata = newGame()
        data.append(onedata)
    save(data,filename)
    return data


def save(data,filename):
    f = open(filename, "w+")
    data = ["".join([str(i) for i in x]) for x in data]
    data = [x+'\n' for x in data]
    f.writelines(data)
    f.close()

def newGame():
    while (1):
        num0 = 0
        num1 = 0
        num2 = 0
        nowcard = 0
        gameinfo = []
        allmessage = []
        tempmessage = [0, 0, 0]
        # big small 2 1 K Q J 10 9 8 7 6 5 4 3

        a = 3 * random.random()
        if (a > 2):
            num2 += 1
            allmessage = allmessage + [0, 0, 1]
        elif (a > 1):
            num1 += 1
            allmessage = allmessage + [0, 1, 0]
        else:
            num0 += 1
            allmessage = allmessage + [1, 0, 0]

        a = 3 * random.random()
        if (a > 2):
            num2 += 1
            allmessage = allmessage + [0, 0, 1]
        elif (a > 1):
            num1 += 1
            allmessage = allmessage + [0, 1, 0]
        else:
            num0 += 1
            allmessage = allmessage + [1, 0, 0]

        while (num0 + num1 + num2 < 54):
            a = 3 * random.random()
            if (a > 2):
                if (num2 == 18):
                    continue
                tempmessage[2] += 1
                nowcard += 1
                num2 += 1
            elif (a > 1):
                if (num1 == 18):
                    continue
                tempmessage[1] += 1
                nowcard += 1
                num1 += 1
            else:
                if (num0 == 18):
                    continue
                tempmessage[0] += 1
                nowcard += 1
                num0 += 1
            if (nowcard == 4):
                nowcard = 0
                allmessage.append(tempmessage[0])
                allmessage.append(tempmessage[1])
                allmessage.append(tempmessage[2])
                tempmessage = [0, 0, 0]

        give0 = random.randint(0, 17)
        give1 = random.randint(0, 17)
        give2 = random.randint(0, 17)
        for i in range(0, 15):
            give0 -= allmessage[3 * i]
            if (give0 < 0):
                allmessage[3 * i] -= 1
                break
        for i in range(0, 15):
            give1 -= allmessage[3 * i + 1]
            if (give1 < 0):
                allmessage[3 * i + 1] -= 1
                break
        for i in range(0, 15):
            give2 -= allmessage[3 * i + 2]
            if (give2 < 0):
                allmessage[3 * i + 2] -= 1
                break
        '''
        sum0 = 0
        sum1 = 0
        sum2 = 0
        for i in range(0, 15):
            sum0 += allmessage[3 * i]
            sum1 += allmessage[3 * i + 1]
            sum2 += allmessage[3 * i + 2]
        if (sum0 != 17 or sum1 != 17 or sum2 != 17):
            print(sum0,sum1,sum2)
        '''
        scores = [0, 0, 0]
        card0 = [0] * 15
        card1 = [0] * 15
        card2 = [0] * 15
        for i in range(0, 15):
            card0[i] = allmessage[3 * i]
            card1[i] = allmessage[3 * i + 1]
            card2[i] = allmessage[3 * i + 2]
        scores[0] = evaluateCard(card0)
        scores[1] = evaluateCard(card1)
        scores[2] = evaluateCard(card2)
        if (scores[0] > 15 or scores[1] > 15 or scores[2] > 15):
            break

    i = np.argmax(scores)
    if (i != 0):
        for j in range(0, 15):
            temp = allmessage[3 * j]
            allmessage[3 * j] = allmessage[3 * j + i]
            allmessage[3 * j + i] = temp

    for i in range(0, 2):
        allmessage[3 * i] = 1 - allmessage[3 * i + 1] - allmessage[3 * i + 2]
    for i in range(2, 15):
        allmessage[3 * i] = 4 - allmessage[3 * i + 1] - allmessage[3 * i + 2]

    for i in range(0, 15):
        gameinfo.append(allmessage[i * 3])
        gameinfo = gameinfo + [0, 0, 0]

    return gameinfo, allmessage


def evaluateCard(card):
    score =  card[0] * 5 + card[1] * 4 + card[2] * 3 + card[3] * 2
    for i in range(15):
        if card[i] == 3:
            score += 2
        if card[i] == 4:
            score += 5
    return score