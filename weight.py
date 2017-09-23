import copy
import ai2
import random
from game import convertCard
from math import exp

#     [rocket, bomb,  singleS, doubleS, tripleS, single, double, triple]
# r = [0.298,  0.250, 0,       0.029,   0.349,   0,      0,      0.030]



def typeCount(card):
    tmpCard = copy.deepcopy(card)
    hand = [0, 0, 0, 0, 0, 0, 0, 0]
    result = [[], [], [], [], [], [], [], []]  # Each item in result[cardType]: [prior card, length]
    cardCount = [[], [], [], [], []]  # cardCount[0] won't always be maintained as it's not used
    for i in range(15):
        cardCount[tmpCard[i]].append(i)

    # 0 Rocket
    if tmpCard[0] == 1 and tmpCard[1] == 1:
        tmpCard[0] = 0
        tmpCard[1] = 0
        cardCount[1].remove(0)
        cardCount[1].remove(1)
        result[0].append([0, 2])

    # 1 Bomb (no need for cardCount[4].clear())
    for i in cardCount[4]:
        tmpCard[i] = 0
        result[1].append([i, 4])

    # 2 Single Straight (tmpCard renewed in findSingleStraight(tmpCard))
    result[2] = ai2.findSingleStraight(tmpCard)
    # Renew cardCount
    cardCount = [[], [], [], [], []]
    for i in range(15):
        cardCount[tmpCard[i]].append(i)

    # 3 Triple (no need for cardCount[3].clear())
    for i in cardCount[3]:
        tmpCard[i] = 0
        result[7].append([i, 3])

    # 4 Triple Straight
    l = len(result[7])
    i = 3
    while i < l:
        for j in range(1, l - i + 1):
            if j == l - i or result[7][i][0] + j != result[7][i + j][0]:
                if j > 1:
                    result[4].append([result[7][i][0], 3 * j])
                i += j
                break
    for item in result[4]:
        for x in range(item[0], item[0] + item[1] // 3):
            result[7].remove([x, 3])

    # 5 Double Straight (tmpCard modified inside function)
    result[3], _, result[2] = ai2.findDoubleStraight(tmpCard, 100, result[2])
    # Renew cardCount
    cardCount = [[], [], [], [], []]
    for i in range(15):
        cardCount[tmpCard[i]].append(i)

    # 6 Double (no need for cardCount[2].clear())
    for i in cardCount[2]:
        tmpCard[i] = 0
        result[6].append([i, 2])

    # 7 Single (no need for cardCount[1].clear())
    for i in cardCount[1]:
        tmpCard[i] = 0
        result[5].append([i, 1])

    # Calculate hand
    for i in range(8):
        hand[i] = len(result[i])

    assert sum(tmpCard) == 0
    # result.sort()
    return hand, result


def calWeight(card):
    hand, result = typeCount(card)
    weight = 0
    # rarity (added 0.05 for sS(plus) and single(minus))
    r = [0.298, 0.250, 0.05, 0.029, 0.349, -0.05, 0, 0.030]
    for i in range(8):
        for j in range(hand[i]):
            # print('i', i, 'r[i]', r[i], 'result[i][j][0]', result[i][j][0])
            weight += r[i] * (1 - 0.05 * result[i][j][0]) * result[i][j][1]
    return (1 / (1 + exp(-10 * weight)))  # normalize to [0, 1]


if __name__ == "__main__":
    max = -100
    min = 100
    for round in range(10000):
        initCard = [0, 1]
        for j in range(2, 15):
            initCard += [j] * 4
        random.shuffle(initCard)

        card = [None, None, None]
        card[0] = convertCard(initCard[0:17])
        card[1] = convertCard(initCard[17:34])
        card[2] = convertCard(initCard[34:54])
        if round % 1000 == 0:
            print(round)

        hand, _ = ai2.handNum(card[0]); hand1, _ = typeCount(card[0]); assert hand == sum(hand1)
        hand, _ = ai2.handNum(card[1]); hand1, _ = typeCount(card[1]); assert hand == sum(hand1)
        hand, _ = ai2.handNum(card[2]); hand1, _ = typeCount(card[2]); assert hand == sum(hand1)
        '''
        print(calWeight(card[0]))
        print(calWeight(card[1]))
        print(calWeight(card[2]))
        '''
