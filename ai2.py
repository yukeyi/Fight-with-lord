import game as gameApp
import copy


# This function modifies card
# Only to be used in handNum(card)
def findSingleStraight(card):
    # 1. Draw 5-card straights from card (from smallest to largest)
    result = []
    for i in reversed(range(3, 15)):
        for j in range(card[i]):
            isStraight = True
            for l in range(5):
                if i - l < 3 or (isStraight and card[i - l] < 1):
                    isStraight = False
                    break
            if isStraight:
                for l in range(5):
                    card[i - l] -= 1
                result.append([i - l, l + 1])  # (prior card, length of straight)

    # 2. Extend 5-card straights if possible (from smallest to largest)
    #    Meanwhile the number of items in result does not change
    for item in result:
        prior = item[0]
        for i in reversed(range(3, prior)):
            if card[i] < 1:
                break
            item[0] -= 1
            item[1] += 1
            card[i] -= 1
    result.sort()

    # 3. Concatenate straights if possible
    action = False
    isEnd = False
    while not isEnd:
        tmpRes = copy.deepcopy(result)
        l = len(result)
        if l <= 1:
            break
        for i in range(l - 1):
            if action:
                break
            for j in range(1, l):
                action = False
                if tmpRes[i][0] + tmpRes[i][1] == tmpRes[j][0]:
                    result.remove(tmpRes[i])
                    result.remove(tmpRes[j])
                    result.append([tmpRes[i][0], tmpRes[i][1] + tmpRes[j][1]])
                    result.sort()
                    action = True
                    break
        # action = False
        isEnd = True
    return result  # listed from larger straights to smaller straights


# This function modifies card
# Only to be used in handNum(card)
def findDoubleStraight(card, hand, singleRes):
    # 1. Draw 6-card double straights from card (from smallest to largest)
    handNew = hand
    result = []
    for i in reversed(range(3, 15)):
        for j in range(card[i]):
            isStraight = True
            for l in range(3):
                if i - l < 3 or (isStraight and card[i - l] < 2):
                    isStraight = False
                    break
            if isStraight:
                for l in range(3):
                    card[i - l] -= 2
                result.append([i - l, 2 * (l + 1)])  # (prior card, length of straight)

    # 2. Extend 6-card double straights to 8-card double straights if possible (from smallest to largest)
    #    Meanwhile the number of items in result does not change
    for item in result:
        i = item[0] - 1
        if card[i] < 3 or i < 3:
            break
        item[0] -= 1
        item[1] += 1
        card[i] -= 2

    # 3. Combine (exactly) same single straights to double straights
    singleResNew = copy.deepcopy(singleRes)
    for item in singleRes:
        if singleRes.count(item) >= 2 and [item[0], 2 * item[1]] not in result:
            handNew -= 2
            result.append([item[0], 2 * item[1]])
            singleResNew.remove(item)
            singleResNew.remove(item)

    # 4. Contactenation
    ll = len(result)  # By rule we have ll <= 3
    if ll >= 2 and result[0][0] + result[0][1] // 2 == result[1][0]:
        result.insert(2, [result[0][0], result[0][1] + result[1][1]])
        result.pop(0)
        result.pop(1)
    if ll >= 3 and result[-2][0] + result[-2][1] // 2 == result[-1][0]:
        result.insert(-2, [result[-2][0], result[-2][1] + result[-1][1]])
        result.pop(-1)
        result.pop(-1)

    handNew += len(result)
    result.sort()
    return result, handNew, singleResNew


def handNum(card):
    tmpCard = copy.deepcopy(card)
    hand = 0
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
        hand = 1
        result[0].append([0, 2])

    # 1 Bomb (no need for cardCount[4].clear())
    hand += len(cardCount[4])
    for i in cardCount[4]:
        tmpCard[i] = 0
        result[1].append([i, 4])

    # 2 Single Straight (tmpCard renewed in findSingleStraight(tmpCard))
    result[2] = findSingleStraight(tmpCard)
    hand += len(result[2])
    # Renew cardCount
    cardCount = [[], [], [], [], []]
    for i in range(15):
        cardCount[tmpCard[i]].append(i)

    # 3 Triple (no need for cardCount[3].clear())
    hand += len(cardCount[3])
    for i in cardCount[3]:
        tmpCard[i] = 0
        result[3].append([i, 3])

    # 4 Triple Straight
    l = len(result[3])
    i = 3
    while i < l:
        for j in range(1, l - i + 1):
            if j == l - i or result[3][i][0] + j != result[3][i + j][0]:
                if j > 1:
                    hand += 1
                    result[4].append([result[3][i][0], 3 * j])
                i += j
                break
    for item in result[4]:
        hand -= item[1] // 3
        for x in range(item[0], item[0] + item[1] // 3):
            result[3].remove([x, 3])

    # 5 Double Straight (tmpCard modified inside function)
    result[5], hand, result[2] = findDoubleStraight(tmpCard, hand, result[2])
    # Renew cardCount
    cardCount = [[], [], [], [], []]
    for i in range(15):
        cardCount[tmpCard[i]].append(i)

    # 6 Double (no need for cardCount[2].clear())
    hand += len(cardCount[2])
    for i in cardCount[2]:
        tmpCard[i] = 0
        result[6].append([i, 2])

    # 7 Single (no need for cardCount[1].clear())
    hand += len(cardCount[1])
    for i in cardCount[1]:
        tmpCard[i] = 0
        result[7].append([i, 1])

    assert sum(tmpCard) == 0
    # result.sort()
    return hand, result


# Play smallest
def cardPlayGeneral(card, singleFirst=True):
    hand, legalCard = handNum(card)
    typeCount = [len(item) for item in legalCard]
    #assert sum(typeCount) > 0
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # Single
    if singleFirst and typeCount[7] > 0 and (typeCount[3] == 0 or typeCount[3] <= typeCount[6] + typeCount[7] - 2):
        result[legalCard[7][-1][0]] = 1
        return result
    # Double
    if typeCount[6] > 0 and (typeCount[3] == 0 or typeCount[3] <= typeCount[6] + typeCount[7] - 2):
        result[legalCard[6][-1][0]] = 2
        return result
    # Double Straight
    if typeCount[5] > 0:
        sel = legalCard[5][-1]
        for i in range(sel[0], sel[0] + sel[1] // 2):
            result[i] = 2
        return result
    # Single Straight
    if typeCount[2] > 0:
        sel = legalCard[2][-1]
        for i in range(sel[0], sel[0] + sel[1]):
            result[i] = 1
        return result
    # Triple Straight
    if typeCount[4] > 0:
        sel = legalCard[4][-1]
        for i in range(sel[0], sel[0] + sel[1] // 3):
            result[i] = 3
        return result
    # Triple
    if typeCount[3] > 0:
        result[legalCard[3][-1][0]] = 3
        if typeCount[7] > 0:
            result[legalCard[7][-1][0]] = 1
        elif typeCount[6] > 0:
            result[legalCard[6][-1][0]] = 2
        return result
    # Bomb
    if typeCount[1] > 0:
        result[legalCard[1][-1][0]] = 4
        return result
    # Rocket
    if typeCount[0] > 0:
        return [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # Single (play largest)
    else:
        result[legalCard[7][0][0]] = 1
        return result


def cardFollowSmallestFirst(card, lastCard):
    hand, legalCard = handNum(card)
    typeCount = [len(item) for item in legalCard]
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    type, prior = gameApp.cardType(lastCard)
    length = sum(lastCard)
    # Single
    if type == 2:
        if typeCount[7] > 0 and legalCard[7][0][0] < prior:  # single
            for item in reversed(legalCard[7]):
                if item[0] < prior:
                    result[item[0]] = 1
                    return result
        if 2 < prior and card[2] > 0:  # 2
            return [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if typeCount[6] > 0 and legalCard[6][0][0] < prior:  # double
            for item in reversed(legalCard[6]):
                if item[0] < prior:
                    result[item[0]] = 1
                    return result
        if typeCount[2] > 0 and legalCard[2][0][0] < prior:  # single straight (length >= 6)
            for item in reversed(legalCard[2]):
                if item[1] < 6:
                    continue
                for i in range(1, item[1] - 4):
                    if item[0] + item[1] - i < prior:
                        result[item[0] + item[1] - i] = 1
                        return result
                if item[0] < prior:
                    result[item[0]] = 1
                    return result
        if typeCount[3] > 0 and legalCard[3][0][0] < prior:  # triple
            for item in reversed(legalCard[3]):
                if item[0] < prior:
                    result[item[0]] = 1
                    return result
        if typeCount[4] > 0 and legalCard[4][0][0] < prior:  # triple straight
            for item in reversed(legalCard[4]):
                for i in reversed(range(item[1] // 3)):
                    if item[0] + i < prior:
                        result[item[0] + i] = 1
                        return result
        if typeCount[2] > 0 and legalCard[2][0][0] < prior:  # single straight (length == 5)
            for item in reversed(legalCard[2]):
                if item[1] >= 6:
                    continue
                for i in reversed(range(item[1])):
                    if item[0] + i < prior:
                        result[item[0] + i] = 1
                        return result
        if typeCount[5] > 0 and legalCard[5][0][0] < prior:  # double straight
            for item in reversed(legalCard[5]):
                for i in reversed(range(item[1] // 2)):
                    if item[0] + i < prior:
                        result[item[0] + i] = 1
                        return result
        if typeCount[1] > 0:  # bomb
            result[legalCard[1][-1][0]] = 4
            return result
        if typeCount[0] > 0:  # rocket
            return [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # pass
        return [0] * 15
    # Double
    if type == 3:
        if typeCount[6] > 0 and legalCard[6][0][0] < prior:  # double
            for item in reversed(legalCard[6]):
                if item[0] < prior:
                    result[item[0]] = 2
                    return result
        if typeCount[5] > 0 and legalCard[5][0][0] < prior:  # double straight (length >= 8)
            for item in reversed(legalCard[5]):
                if item[1] < 4:
                    continue
                for i in reversed(range(item[1] // 2)):
                    if item[0] + i < prior:
                        result[item[0] + i] = 2
                        return result
                if item[0] < prior:
                    result[item[0]] = 2
                    return result
        if typeCount[3] > 0 and legalCard[3][0][0] < prior:  # triple
            for item in reversed(legalCard[3]):
                if item[0] < prior:
                    result[item[0]] = 2
                    return result
        if typeCount[5] > 0 and legalCard[5][0][0] < prior:  # double straight (length == 6)
            for item in reversed(legalCard[5]):
                for i in reversed(range(item[1] // 2)):
                    if item[0] + i < prior:
                        result[item[0] + i] = 2
                        return result
        if typeCount[4] > 0 and legalCard[4][0][0] < prior:  # triple straight
            for item in reversed(legalCard[4]):
                for i in reversed(range(item[1] // 3)):
                    if item[0] + i < prior:
                        result[item[0] + i] = 2
                        return result
        if typeCount[1] > 0:  # bomb
            result[legalCard[1][-1][0]] = 4
            return result
        if typeCount[0] > 0:  # rocket
            return [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # pass
        return [0] * 15
    # Double Straight
    if type == 6:
        if typeCount[5] > 0 and legalCard[5][0][0] < prior:  # double straight
            for item in reversed(legalCard[5]):  # (same length)
                if item[1] != length or item[0] >= prior:
                    continue
                for i in range(length // 2):
                    result[item[0] + i] = 2
                return result
            for item in reversed(legalCard[5]):  # (longer length)
                if item[1] <= length or item[0] + item[1] // 2 >= prior + length // 2:
                    continue
                for i in reversed(range(item[1] // 2)):
                    if item[0] + i < prior + length // 2:
                        for j in range(length // 2):
                            result[item[0] + j] = 2
                        return result
        if typeCount[4] > 0 and legalCard[4][0][0] < prior:  # triple straight
            for item in reversed(legalCard[4]):  # (longer 'length')
                if item[1] // 3 <= length // 2 or item[0] + item[1] // 3 >= prior + length // 2:
                    continue
                for i in reversed(range(item[1] // 3)):
                    if item[0] + i < prior + length // 2:
                        for j in range(length // 2):
                            result[item[0] + j] = 2
                        return result
            for item in reversed(legalCard[4]):  # (same 'length')
                if item[1] // 3 != length // 2 or item[0] >= prior:
                    continue
                for i in range(item[1] // 3):
                    result[item[0] + i] = 2
                return result
        if typeCount[1] > 0:  # bomb
            result[legalCard[1][-1][0]] = 4
            return result
        if typeCount[0] > 0:  # rocket
            return [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # pass
        return [0] * 15
    # Single Straight
    if type == 5:
        if typeCount[2] > 0 and legalCard[2][0][0] < prior:  # single straight (same length)
            for item in reversed(legalCard[2]):
                if item[1] != length or item[0] >= prior:
                    continue
                for i in range(item[1]):
                    result[item[0] + i] = 1
                return result
        if typeCount[5] > 0 and legalCard[5][0][0] < prior:  # double straight (same 'length')
            for item in reversed(legalCard[5]):
                if item[1] // 2 != length or item[0] >= prior:
                    continue
                for i in range(item[1] // 2):
                    result[item[0] + i] = 1
                return result
        if typeCount[4] > 0 and legalCard[4][0][0] < prior:  # triple straight (same 'length')
            for item in reversed(legalCard[4]):
                if item[1] // 3 != length or item[0] >= prior:
                    continue
                for i in range(item[1] // 3):
                    result[item[0] + i] = 1
                return result
        if typeCount[2] > 0 and legalCard[2][0][0] < prior:  # single straight (longer length)
            for item in reversed(legalCard[2]):
                if item[1] <= length or item[0] + item[1] >= prior + length:
                    continue
                for i in reversed(range(item[1])):
                    if item[0] + i < prior + length:
                        for j in range(length):
                            result[item[0] + j] = 1
                        return result
        if typeCount[5] > 0 and legalCard[5][0][0] < prior:  # double straight (longer 'length')
            for item in reversed(legalCard[5]):
                if item[1] // 2 <= length or item[0] + item[1] // 2 >= prior + length:
                    continue
                for i in reversed(range(item[1] // 2)):
                    if item[0] + i < prior + length:
                        for j in range(length):
                            result[item[0] + j] = 1
                        return result
        if typeCount[4] > 0 and legalCard[4][0][0] < prior:  # triple straight (longer 'length')
            for item in reversed(legalCard[4]):
                if item[1] // 3 <= length or item[0] + item[1] // 3 >= prior + length:
                    continue
                for i in reversed(range(item[1] // 3)):
                    if item[0] + i < prior + length:
                        for j in range(length):
                            result[item[0] + j] = 1
                        return result
        if typeCount[1] > 0:  # bomb
            result[legalCard[1][-1][0]] = 4
            return result
        if typeCount[0] > 0:  # rocket
            return [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # pass
        return [0] * 15
    # Triple Straight
    if type == 7:
        if typeCount[4] > 0 and legalCard[4][0][0] < prior:  # triple straight
            for item in reversed(legalCard[4]):  # (same length)
                if item[1] != length or item[0] >= prior:
                    continue
                for i in range(length // 3):
                    result[item[0] + i] = 3
                return result
            for item in reversed(legalCard[4]):  # (longer length)
                if item[1] <= length or item[0] + item[1] // 3 >= prior + length // 3:
                    continue
                for i in reversed(range(item[1] // 3)):
                    if item[0] + i < prior + length // 3:
                        for j in range(length // 3):
                            result[item[0] + j] = 3
                        return result
        if typeCount[1] > 0:  # bomb
            result[legalCard[1][-1][0]] = 4
            return result
        if typeCount[0] > 0:  # rocket
            return [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # pass
        return [0] * 15
    # Triple + X
    if type == 4:
        if typeCount[3] > 0 and legalCard[3][0][0] < prior:  # triple
            for item in reversed(legalCard[3]):
                if item[0] >= prior:
                    continue
                result[item[0]] = 3
                if length == 3:
                    return result
                elif length == 4:
                    tmpCard = copy.deepcopy(card)
                    tmpCard[item[0]] -= 3
                    # single = lastCard.index(1)
                    if tmpCard[14] >= 1:
                        res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                    else:
                        res = cardFollowSmallestFirst(tmpCard, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
                    if sum(res) != 1 or (hand > 3 and sum(res[0:3]) > 0):
                        result = [0] * 15
                        break
                    result[res.index(1)] += 1
                    # result = [result[i] + res[i] for i in range(15)]
                    return result
                elif length == 5:
                    tmpCard = copy.deepcopy(card)
                    tmpCard[item[0]] -= 3
                    # double = lastCard.index(2)
                    if tmpCard[14] >= 2:
                        res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
                    else:
                        res = cardFollowSmallestFirst(tmpCard, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2])
                    if sum(res) != 2 or res[0] == 1 or (hand > 3 and sum(res[0:3]) > 0):
                        result = [0] * 15
                        break
                    result[res.index(2)] += 2
                    # result = [result[i] + res[i] for i in range(15)]
                    return result
        if typeCount[4] > 0 and legalCard[4][0][0] < prior:  # triple straight
            for item in reversed(legalCard[4]):
                item1 = item[0]
                for i in reversed(range(item[1] // 3)):
                    if item[0] + i >= prior:
                        continue
                    item1 = item[0] + i
                    result[item1] = 3
                    break
                if length == 3:
                    return result
                elif length == 4:
                    tmpCard = copy.deepcopy(card)
                    tmpCard[item1] -= 3
                    # single = lastCard.index(1)
                    if tmpCard[14] >= 1:
                        res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                    else:
                        res = cardFollowSmallestFirst(tmpCard, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
                    if sum(res) != 1 or (hand > 3 and sum(res[0:3]) > 0):
                        result = [0] * 15
                        break
                    result[res.index(1)] += 1
                    # result = [result[i] + res[i] for i in range(15)]
                    return result
                elif length == 5:
                    tmpCard = copy.deepcopy(card)
                    tmpCard[item1] -= 3
                    # double = lastCard.index(2)
                    if tmpCard[14] >= 2:
                        res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
                    else:
                        res = cardFollowSmallestFirst(tmpCard, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2])
                    if sum(res) != 2 or res[0] == 1 or (hand > 3 and sum(res[0:3]) > 0):
                        result = [0] * 15
                        break
                    result[res.index(2)] += 2
                    # result = [result[i] + res[i] for i in range(15)]
                    return result
        if typeCount[1] > 0:  # bomb
            result[legalCard[1][-1][0]] = 4
            return result
        if typeCount[0] > 0:  # rocket
            return [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # pass
        return [0] * 15
    # Bomb
    if type == 1:
        if typeCount[1] > 0 and legalCard[1][0][0] < prior:
            for item in reversed(legalCard[1]):
                if item[0] < prior:
                    result[item[0]] = 4
                    return result
        if typeCount[0] > 0:  # rocket
            return [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # pass
        return [0] * 15
    # Rocket
    return [0] * 15


def cardFollowLargestFirst(card, lastCard):
    hand, legalCard = handNum(card)
    typeCount = [len(item) for item in legalCard]
    assert sum(typeCount) > 0
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    type, prior = gameApp.cardType(lastCard)
    length = sum(lastCard)
    # Rocket
    if type == 0:
        return [0] * 15
    # Bomb
    if type == 1:
        if typeCount[0] > 0:  # rocket
            return [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if typeCount[1] > 0 and legalCard[1][-1][0] < prior:  # bomb
            result[legalCard[1][-1][0]] = 4
            return result
        return [0] * 15
    # General: Follow by Rocket or Bomb
    if typeCount[0] > 0:  # rocket
        return [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if typeCount[1] > 0:  # bomb
        result[legalCard[1][-1][0]] = 4
        return result
    # Single
    if type == 2:
        for i in range(prior):
            if card[i] > 0:
                result[i] = 1
                return result
        return [0] * 15
    # Double
    if type == 3:
        for i in range(prior):
            if card[i] > 1:
                result[i] = 2
                return result
        return [0] * 15
    # Double Straight
    if type == 6:
        if typeCount[5] > 0 and legalCard[5][0][0] < prior:  # double straight
            for item in legalCard[5]:
                if item[0] >= prior:
                    break
                if item[1] < length:
                    continue
                for i in range(length // 2):
                    result[item[0] + i] = 2
                return result
        if typeCount[3] > 0 and legalCard[3][0][0] < prior:  # triple straight
            for item in legalCard[3]:
                if item[0] >= prior:
                    break
                if item[1] // 3 < length // 2:
                    continue
                for i in range(length // 2):
                    result[item[0] + i] = 2
                return result
        return [0] * 15
    # Single Straight
    if type == 5:
        if typeCount[2] > 0 and legalCard[2][0][0] < prior:  # single straight
            for item in legalCard[2]:
                if item[0] >= prior:
                    break
                if item[1] < length:
                    continue
                for i in range(length):
                    result[item[0] + i] = 1
                return result
        if typeCount[5] > 0 and legalCard[5][0][0] < prior:  # double straight
            for item in legalCard[5]:
                if item[0] >= prior:
                    break
                if item[1] // 2 < length:
                    continue
                for i in range(length):
                    result[item[0] + i] = 1
                return result
        if typeCount[3] > 0 and legalCard[3][0][0] < prior:  # triple straight
            for item in legalCard[3]:
                if item[0] >= prior:
                    break
                if item[1] // 3 < length:
                    continue
                for i in range(length):
                    result[item[0] + i] = 1
                return result
        return [0] * 15
    # Triple Straight
    if type == 7:
        if typeCount[3] > 0 and legalCard[3][0][0] < prior:  # triple straight
            for item in legalCard[3]:
                if item[0] >= prior:
                    break
                if item[1] < length:
                    continue
                for i in range(length):
                    result[item[0] + i] = 3
                return result
        return [0] * 15
    # Triple + X
    if type == 4:
        if typeCount[3] > 0 and legalCard[3][0][0] < prior:  # triple
            result[legalCard[3][0][0]] = 3
            if length == 3:
                return result
            elif length == 4:
                tmpCard = copy.deepcopy(card)
                tmpCard[legalCard[3][0][0]] -= 3
                if tmpCard[14] >= 1:
                    res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                else:
                    res = cardFollowSmallestFirst(tmpCard, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
                if not (sum(res) != 1 or (hand > 3 and sum(res[0:3]) > 0)):
                    result[res.index(1)] += 1
                    # result = [result[i] + res[i] for i in range(15)]
                    return result
            elif length == 5:
                tmpCard = copy.deepcopy(card)
                tmpCard[legalCard[3][0][0]] -= 3
                if tmpCard[14] >= 2:
                    res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
                else:
                    res = cardFollowSmallestFirst(tmpCard, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2])
                if not (sum(res) != 2 or res[0] == 1 or (hand > 3 and sum(res[0:3]) > 0)):
                    result[res.index(2)] += 2
                    # result = [result[i] + res[i] for i in range(15)]
                    return result
        if typeCount[4] > 0 and legalCard[4][0][0] < prior:  # triple straight
            result[legalCard[4][0][0]] = 3
            if length == 3:
                return result
            elif length == 4:
                tmpCard = copy.deepcopy(card)
                tmpCard[legalCard[4][0][0]] -= 3
                if tmpCard[14] >= 1:
                    res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                else:
                    res = cardFollowSmallestFirst(tmpCard, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
                if not (sum(res) != 1 or (hand > 3 and sum(res[0:3]) > 0)):
                    result[res.index(1)] += 1
                    # result = [result[i] + res[i] for i in range(15)]
                    return result
            elif length == 5:
                tmpCard = copy.deepcopy(card)
                tmpCard[legalCard[4][0][0]] -= 3
                if tmpCard[14] >= 2:
                    res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
                else:
                    res = cardFollowSmallestFirst(tmpCard, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2])
                if not (sum(res) != 2 or res[0] == 1 or (hand > 3 and sum(res[0:3]) > 0)):
                    result[res.index(2)] += 2
                    # result = [result[i] + res[i] for i in range(15)]
                    return result
        return [0] * 15
    return


def cardFollowCooperate(card, lastCard):
    hand, legalCard = handNum(card)
    typeCount = [len(item) for item in legalCard]
    assert sum(typeCount) > 0
    type, prior = gameApp.cardType(lastCard)
    length = sum(lastCard)
    # Single
    if type == 2:
        result = cardFollowSmallestFirst(card, lastCard)
        if sum(result[0:3]) > 0 or sum(result) == 4:
            return [0] * 15
        else:
            return result
    # Double:
    if type == 3:
        result = cardFollowSmallestFirst(card, lastCard)
        if sum(result[0:4]) > 0 or sum(result) == 4:
            return [0] * 15
        else:
            return result
    return [0] * 15


def getNextMove(gameinfo, id):
    #assert gameinfo['turn'] == id
    tmpinfo = copy.deepcopy(gameinfo)
    if tmpinfo['last'] == id or tmpinfo['last'] == -1:
        if id == 0 and (tmpinfo['handRemain'][1] == 1 or tmpinfo['handRemain'][2] == 1):
            return cardPlayGeneral(tmpinfo['handCard'][id], False)
        elif id == 2 and tmpinfo['handRemain'][0] == 1:
            return cardPlayGeneral(tmpinfo['handCard'][id], False)
        else:
            return cardPlayGeneral(tmpinfo['handCard'][id])
    else:
        if id == 0:
            if tmpinfo['handRemain'][1] == 1 or tmpinfo['handRemain'][2] == 1:
                return cardFollowLargestFirst(tmpinfo['handCard'][id], tmpinfo['lastCard'])
            else:
                return cardFollowSmallestFirst(tmpinfo['handCard'][id], tmpinfo['lastCard'])
        elif id == 1:
            if tmpinfo['last'] == 2:
                return cardFollowCooperate(tmpinfo['handCard'][id], tmpinfo['lastCard'])
            else:
                return cardFollowSmallestFirst(tmpinfo['handCard'][id], tmpinfo['lastCard'])
        else:
            if tmpinfo['handRemain'][0] == 1:
                return cardFollowLargestFirst(tmpinfo['handCard'][id], tmpinfo['lastCard'])
            elif tmpinfo['last'] == 1:
                return cardFollowCooperate(tmpinfo['handCard'][id], tmpinfo['lastCard'])
            else:
                return cardFollowSmallestFirst(tmpinfo['handCard'][id], tmpinfo['lastCard'])

"""
#      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14]
card = [1, 1, 4, 1, 1, 1, 1, 1, 0, 2, 2, 2, 3, 3, 0]  # Zz2222AKQJ0887766555444
print(handNum(card))  # [[9, 5], [9, 5], [3, 5]]
print(card)

#      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14]  # 2AKQJ099877766543
card = [0, 0, 1, 1, 1, 1, 1, 1, 2, 1, 3, 2, 1, 1, 1]
print(handNum(card))  # [[10, 5], [3, 9]]
print(card)
"""
