import copy
import random
import weight
import game as gameApp

def calcSpecialCard(card):
    tempCard = copy.deepcopy(card)
    rocket = [0]
    if card[0] == 1 and card[1] == 1:
        rocket[0] = 1
        tempCard[0] -= 1
        tempCard[1] -= 1

    #bomb
    bomb = [0] * 13
    numBomb = [0]
    for i in range(2, 15):
        if card[i] == 4:
            bomb[i - 2] = 1
            numBomb[0] += 1
            tempCard[i] -= 4
    #straight
    singleS = [0] * (8 + 7 + 6 + 5 + 4 + 3 + 2 + 1)
    numSingleS = [0]
    for i in range(3, 11):
        for j in range(12):
            if i + j >= 15 or card[i + j] < 1:
                break
            if j >= 4:
                singleS[(12 - i + 8) * (i-3) //2 + (j - 4)] = 1
                numSingleS[0] += 1
                for k in range (i, i+j+1):
                    tempCard[k] -= 1

    doubleS = [0] * (8 + 8 + 8 + 7 + 6 + 5 + 4 + 3 + 2 + 1)
    numDoubleS = [0]
    for i in range(3, 13):
        for j in range(10):
            if i + j >= 15 or card[i + j] < 2:
                break
            if j >= 2:
                numDoubleS[0] += 1
                for k in range(i, i+j+1):
                    tempCard[k] -= 2
                if i == 3:
                    doubleS[j - 2] = 1
                elif i == 4:
                    doubleS[j - 2 + 8] = 1
                else:
                    doubleS[16 + (14 - i + 8) * (i - 5) // 2 + (j - 2)] = 1

    tripleS = [0] * (6 * 5 + 5 + 4 + 3 + 2 +1)
    numTripleS = [0]
    for i in range(3, 14):
        for j in range(6):
            if i + j >= 15 or card[i + j] < 3:
                break
            if j >= 1:
                numTripleS[0] += 1
                for k in range(i, i+j+1):
                    tempCard[k] -= 3
                if i == 3:
                    tripleS[j - 1] = 1
                elif i == 4:
                    tripleS[j - 1 + 5] = 1
                elif i == 5:
                    tripleS[j - 1 + 10] = 1
                elif i == 6:
                    tripleS[j - 1 + 15] = 1
                elif i == 7:
                    tripleS[j - 1 + 20] = 1
                elif i == 8:
                    tripleS[j - 1 + 25] = 1
                else:
                    tripleS[30 + (5 + 15 - i) * (i - 9) //2 + (j - 1)] = 1
    double = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    single = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    triple = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(15):
        if tempCard[i] == 2:
            double[i] = 1
        elif tempCard[i] == 1:
            single[i] = 1
        elif tempCard[i] == 3:
            triple[i] = 1

    return rocket + scale(numBomb, 5) + bomb + scale(numTripleS, 15) + tripleS + scale(numDoubleS, 36) + doubleS + scale(numSingleS, 36) + singleS + triple + double + single + [weight.calWeight(card)]
#    return rocket + numBomb + bomb + numTripleS + tripleS + numDoubleS + doubleS + numSingleS + singleS + triple + double + single
typeCount = [1, 13, 15, 13, 13, 13, 13, 1, 2, 3, 4, 5, 6, 7, 8, 3, 4, 5, 6, 7, 8, 9, 10, 7, 8, 9, 10, 11]
typeCardNum = [2, 4, 1, 2, 3, 4, 5, 12, 11, 10, 9, 8, 7, 6, 5, 10, 9, 8, 7, 6, 5, 4, 3, 6, 5, 4, 3, 2]
def genCardType(card):
    n = len(typeCount)
    cardType = [0] * n
    for i in range(n):
        cardType[i] = [0] * typeCount[i]
    m = [0, 0]
    for i in range(15):
        if card[i] > 0:
            m[0] += 1
        if card[i] > 1:
            m[1] += 1
    #Rocket
    if card[0] == 1 and card[1] == 1:
        cardType[0][0] = 1
    #Bomb
    for i in range(2, 15):
        cardType[1][i - 2] = card[i] // 4
    #single
    for i in range(0, 15):
        cardType[2][i] = card[i]
    #double
    for i in range(2, 15):
        cardType[3][i - 2] = card[i] // 2
    #triple+X
    #0
    for i in range(2, 15):
        cardType[4][i - 2] = card[i] // 3
    #1
    if m[0] > 1:
        for i in range(2, 15):
            cardType[5][i - 2] = card[i] // 3
    #2
    if m[1] > 1:
        for i in range(2, 15):
            cardType[6][i - 2] = card[i] // 3

    straightCount = [[0] * 15, [0] * 15, [0] * 15, [0] * 15]
    for i in range(3, 15):
        for j in range(4):
            if card[i] > j:
                straightCount[j][i] = straightCount[j][i - 1] + 1
            else:
                straightCount[j][i] = straightCount[j][i - 1]
    #straight 12~5
    for i in range(8):
        l = 12 - i
        for p in range(3, 4 + i):
            for j in range(4):
                if straightCount[j][p + l - 1] - straightCount[j][p - 1] == l:
                    cardType[7 + i][p - 3] = j + 1
    #double 10~3
    for i in range(8):
        l = 10 - i
        for p in range(3, 6 + i):
            for j in range(4):
                if straightCount[j][p + l - 1] - straightCount[j][p - 1] == l:
                    cardType[15 + i][p - 3] = (j + 1) // 2
    #triple 6~2
    for i in range(5):
        l = 6 - i
        for p in range(3, 10 + i):
            if straightCount[2][p + l - 1] - straightCount[2][p - 1] == l:
                cardType[23 + i][p - 3] = 1
    return cardType

def getType(card):
    cardType = genCardType(card)
    n = len(typeCount)
    resultT = -1
    resultP = 15
    for i in range(n):
        if sum(cardType[i]) == 1:
            resultT = i
            for j in range(len(cardType[i])):
                if cardType[i][j] == 1:
                    resultP = j
    return resultT, resultP

#getType([0,0,0,0,0,0,0,0,0,0,0,0,1,3,0])

def genTypeInfo(card, lastT, lastP):
    cardType = genCardType(card)
    n = len(typeCount)
    if lastT == -1:
        legalType = copy.deepcopy(cardType)
    else:
        legalType = [0] * n
        for i in range(n):
            legalType[i] = [0] * typeCount[i]
        for i in range(lastP):
            legalType[lastT][i] = cardType[lastT][i]
        #Rocket and Bomb
        legalType[0][0] = cardType[0][0]
        if lastT != 0 and lastT != 1:
            for i in range(typeCount[1]):
                legalType[1][i] = cardType[1][i]

    #count
    countCard = [0] * n
    countLegal = 0
    for i in range(n):
        countCard[i] = sum(cardType[i])
        if countCard[i] > 4:
            countCard[i] = 4
        countLegal += sum(legalType[i])
    if countLegal > 4:
        countLegal = 4

    #remain after play legal
    remain = sum(card)
    play = 0
    for i in range(n):
        for j in range(typeCount[i]):
            if legalType[i][j] > 0:
                if typeCardNum[i] > play:
                    play = typeCardNum[i]
    remain -= play
    if remain > 5:
        remain = 5

    #Pure single card
    single = [1] * 15
    for i in range(15):
        if card[i] == 0:
            single[i] = 0
    if cardType[0][0] == 1:
        single[0] = single[1] = 0
    for i in range(2, 15):
        for j in range(3, 6):
            if cardType[j][i - 2] > 0:
                single[i] = 0
    straightCount = [0] * 15
    for i in range(3, 15):
        if card[i] > 0:
            straightCount[i] = straightCount[i - 1] + 1
        else:
            straightCount[i] = straightCount[i - 1]
    for i in range(3, 10):
        if straightCount[i + 4] - straightCount[i - 1] == 5:
            for j in range(i, i + 5):
                single[j] = 0
    singleCount = sum(single) - sum(cardType[5])
    if singleCount < 0:
        singleCount = 0

    result = []
    for i in range(n):
        result += cardType[i]
    for i in range(n):
        result += legalType[i]
    result += countCard + [countLegal] + [remain] + single + [singleCount]
    return result

def genCompareInfo(cards):
    pass

def scale(feature, maxn):
    result = []
    for f in feature:
        tmp = [0] * (maxn + 1)
        tmp[f] = 1
        result += tmp
    return result

def scale2(feature, maxn):
    result = []
    for f in feature:
        result.append(f / maxn)
    return result

def scale3(feature, maxn):
    result = []
    for f in feature:
        tmp = [0] * maxn
        for i in range(f):
            tmp[i] = 1
        result += tmp
    return result

def generateActionFeature(gameinfo):
    tmpinfo = copy.deepcopy(gameinfo)

    last  = tmpinfo['last']
    lastCard = tmpinfo['lastCard']
    lastT, lastP = getType(lastCard)
    h = tmpinfo['handRemain']
    handRemain = [h[0], h[1], h[2]]

    last = scale([last], 2)
    handRemain = scale(handRemain, 20)
    hc = tmpinfo['handCard']
    cardType = genTypeInfo(hc[0], lastT) + genTypeInfo(hc[1], lastT) + genTypeInfo(hc[2], lastT)
    lastT = scale([lastT], len(typeCount))

    return handRemain + last + lastT + cardType


def generateActionFeature2(gameinfo,leave, choose):
    tmpinfo = copy.deepcopy(gameinfo)

    last  = tmpinfo['last']
    lastCard = tmpinfo['lastCard']
    lastT, lastP = getType(lastCard)
    lastT2, lastP2 = getType(choose)
    h = tmpinfo['handRemain']
    handRemain = [h[0], h[1], h[2]]

    last = scale([last], 2)
    handRemain = scale(handRemain, 20)
    hc = tmpinfo['handCard']
    cardType = genTypeInfo(hc[0], lastT) + genTypeInfo(hc[1], lastT) + genTypeInfo(hc[2], lastT)
    lastT = scale([lastT], len(typeCount))

    return handRemain + last + lastT + cardType, genTypeInfo(leave,lastT2)

def generateActionFeature3(gameinfo):
    tmpinfo = copy.deepcopy(gameinfo)

    last  = tmpinfo['last']
    lastCard = tmpinfo['lastCard']
    lastT, lastP = getType(lastCard)
    h = tmpinfo['handRemain']
    handRemain = [h[0], h[1], h[2]]

    last = scale([last], 2)
    handRemain = scale(handRemain, 20)
    hc = tmpinfo['handCard']
    cardType = genTypeInfo(hc[0], lastT, lastP) + genTypeInfo(hc[1], lastT, lastP) + genTypeInfo(hc[2], lastT, lastP)
    lastT = scale([lastT], len(typeCount))

    return handRemain + last + lastT + cardType



#open the card
def convertCard(allmessage,card_on_table,choose):
    formatinfo = {}
    formatinfo['last'] = card_on_table[16]
    formatinfo['handCard'] = [[0]*15,[0]*15,[0]*15]
    for i in range(0,15):
        formatinfo['handCard'][0][i] = allmessage[3*i]
        formatinfo['handCard'][1][i] = allmessage[3*i+1]
        formatinfo['handCard'][2][i] = allmessage[3*i+2]
    formatinfo['lastCard'] = card_on_table[0:15]
    sum0 = 0
    sum1 = 0
    sum2 = 0
    for i in range(0,15):
        sum0 += allmessage[3*i]
        sum1 += allmessage[3*i+1]
        sum2 += allmessage[3*i+2]
    formatinfo['handRemain'] = [sum0,sum1,sum2]

    leave = [0]*15
    for i in range(0,15):
        leave[i] = allmessage[3*i] - choose[i]

    return generateActionFeature2(formatinfo, leave, choose)

def convertSituation(round):
    formatinfo = copy.deepcopy(round)
    sum0 = 0
    sum1 = 0
    sum2 = 0
    for i in range(0,15):
        sum0 += formatinfo['handCard'][0][i]
        sum1 += formatinfo['handCard'][1][i]
        sum2 += formatinfo['handCard'][2][i]
    formatinfo['handRemain'] = [sum0,sum1,sum2]
    return generateActionFeature3(formatinfo)

def convertChoose(round, choose):
    lastT2, lastP2 = getType(round['lastCard'])
    leave = [0]*15
    for i in range(0,15):
        leave[i] = round['handCard'][0][i] - choose[i]
    return genTypeInfo(leave, lastT2, lastP2)


if __name__ == "__main__":
    gameinfo = {}
    gameinfo['last'] = 0
    gameinfo['handCard'] = [[1,1,2,1,2,3,2,1,2,1,0,1,1,1,1],[0,0,1,1,0,0,2,2,1,2,0,2,2,2,2],[0,0,1,2,2,1,0,1,1,1,4,1,1,1,1]]
    gameinfo['lastCard'] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    gameinfo['handRemain'] = [20,17,17]
    a = generateActionFeature(gameinfo)
    print(a)
