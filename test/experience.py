import game as gameApp
import ai2 as ai2App
import numpy as np
import split as splitApp
import copy
import farmerExp as farmerExpApp


DEBUG = 1
DEBUG = 0

CARDS = ['W', 'w', '2', 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3']
REVERSE_SPLIT = [0, 1, 1, 0, 1, 1]

def printCard(play_card):
    for i in range(15):
        if play_card[i] > 0:
            for j in range(play_card[i]):
                print(CARDS[i], end="")
    print(" ", end="")

def printSplit(pos_split):
    for k in pos_split.keys():
        if type(pos_split[k]) != list:
            continue
        cnt_len = len(pos_split[k])
        for j in range(cnt_len):
            printCard(pos_split[k][j])



def addAditionalInfo(gameinfo, pos_split):
    cnt_id = gameinfo['turn']
    pos_split['sum'] = gameinfo['handRemain'][cnt_id]
    pos_split['remain_len'] = pos_split['sum'] - len(pos_split['bomb']) * 4 - len(pos_split['rocket']) * 2
    pos_split['other_depth'] = pos_split['depth'] - len(pos_split['bomb']) - len(pos_split['rocket'])
    pos_split['small_single'] = 0
    pos_split['lord_card'] = gameinfo['handRemain'][0]
    pos_split['farmer_card'] = min(gameinfo['handRemain'][1], gameinfo['handRemain'][2])
    for i in range(len(pos_split['single'])):
        value = getPlayMax(pos_split['single'][i])
        if value <= 10:
            pos_split['small_single'] += 1
    pos_split['small_double'] = 0
    for i in range(len(pos_split['double'])):
        value = getPlayMax(pos_split['double'][i])
        if value <= 10:
            pos_split['small_double'] += 1
    pos_split['small_triple_len'] = 0
    triple_len = len(pos_split['triple'])
    for i in range(triple_len):
        value = getPlayMax(pos_split['triple'][i])
        if value <= 13:
            pos_split['small_triple_len'] += 1


def lordMustPlay(gameinfo):
    must_play = gameinfo['handRemain'][1] == 1 or gameinfo['handRemain'][2] == 1 or gameinfo['handRemain'][1] == 2 or gameinfo['handRemain'][2] == 2
    return must_play

def farmerCard(gameinfo):
    return min(gameinfo['handRemain'][1], gameinfo['handRemain'][2])

def noJoker(gameinfo):
    no_joker = False
    cnt_turn = gameinfo['turn']
    joker_num = 0
    for i in range(3):
        if i != cnt_turn:
            joker_num += gameinfo['handCard'][i][0]
            joker_num += gameinfo['handCard'][i][1]
    if joker_num == 0:
        no_joker = True
    return no_joker

def findMin(cards):
    pos_len = len(cards)
    min_value = 20
    min_index = 0
    for i in range(pos_len):
        for j in range(14, -1, -1):
            if cards[i][j] > 0:
                if min_value > 17 - j:
                    min_value = 17 - j
                    min_index = i
                break
    if min_value == 20:
        return [0] * 15
    return cards[min_index]

def getPlayMin(card):
    for i in range(14, -1, -1):
        if card[i] > 0:
            return 17 - i
    return 0

def getPlayMax(card):
    for i in range(15):
        if card[i] > 0:
            return 17 - i
    return 0


def playTriple(pos_split):
    play_card = findMin(pos_split['triple'])
    play_value = getPlayMax(play_card)
    single_card = findMin(pos_split['single'])
    value = getPlayMax(single_card)
    single_len = len(pos_split['single'])
    double_len = len(pos_split['double'])
    if value == 0 or value > play_value: #no single or single card > triple
        if value != 0 and pos_split['depth'] == 1:
            return list(np.array(play_card) + np.array(single_card))
        if value != 0 and (play_value >= 3 and play_value <= 6) :
            if value - play_value <= 5 or (single_len == 1 and value <= 15 and double_len == 0) or value <= 12:
                return list(np.array(play_card) + np.array(single_card))
        if value != 0 and (play_value >= 7 and play_value <= 11):
            if value <= 13 or (single_len == 1 and value <= 15 and double_len == 0):
                return list(np.array(play_card) + np.array(single_card))
        if value != 0 and (play_value >= 12 and play_value <= 13) and pos_split['remain_len'] <= 9:  # sum less than 9: play triple
            if value < play_value or (single_len == 1 and value <= 15 and double_len == 0):
                return list(np.array(play_card) + np.array(single_card))
        small_value = 0
        for i in range(len(pos_split['single'])):
            value = getPlayMax(pos_split['single'][i])
            if value <= play_value:
                small_value += 1
        double_card = findMin(pos_split['double'])
        value = getPlayMax(double_card)
        if value == 0:
            return play_card
        if pos_split['other_depth'] == 1:
            return list(np.array(play_card) + np.array(double_card))
        if play_value >= 3 and play_value <= 6:
            if value - play_value <= 5:
                return list(np.array(play_card) + np.array(double_card))
        if play_value >= 7 and play_value <= 11:
            if value <= 10:
                return list(np.array(play_card) + np.array(double_card))
        if play_value >= 12 and value < play_value:
            return list(np.array(play_card) + np.array(double_card))
        if pos_split['depth'] - len(pos_split['bomb']) - len(pos_split['rocket']) <= 2:
            return list(np.array(play_card) + np.array(double_card))
        if value != 0 and pos_split['remain_len'] <= 8 and pos_split['small_single'] <= 1:
            return list(np.array(play_card) + np.array(single_card))
        if play_value == 15 and pos_split['remain_len'] <= 8 and pos_split['small_single'] <= 2:
            return list(np.array(play_card) + np.array(single_card))
        if value != 0 and pos_split['other_depth'] <= 2:
            return list(np.array(play_card) + np.array(single_card))
    else:
        return list(np.array(play_card) + np.array(single_card))
    return [0] * 15
"""

def playTriple(pos_split):
    triple_card = findMin(pos_split['triple'])
    triple_value = getPlayMax(triple_card)
    single_card = findMin(pos_split['single'])
    single_value = getPlayMax(single_card)
    double_card = findMin(pos_split['double'])
    double_value = getPlayMax(double_card)
    if single_value == 0 and double_value == 0:
        return triple_card
    if single_value == 0:

    if single_value < double_value:

    else:
"""

def getSingleMax(gameinfo, pos_split):
    max_value = 0
    for i in range(15):
        if (gameinfo['handCard'][1][i] > 0 or gameinfo['handCard'][2][i] > 0) and 17 - i > max_value:
            max_value = 17 - i
    return max_value

def playStraight(pos_split):
    play_card = findMin(pos_split['straight'])
    return play_card

def playBomb(pos_split):
    play_card = findMin(pos_split['bomb'])
    return play_card

def playDoubleStraight(pos_split):
    play_card = findMin(pos_split['double_straight'])
    return play_card

def playDouble(pos_split):
    play_card = findMin(pos_split['double'])
    return play_card

def playSingle(gameinfo, pos_split):
    single_len = len(pos_split['single'])
    no_joker = noJoker(gameinfo)
    farmer_max = getSingleMax(gameinfo, pos_split)
    if no_joker and pos_split['other_depth'] == 2:
        for i in range(single_len):
            cnt_value = getPlayMax(pos_split['single'][i])
            if cnt_value > farmer_max:
                final_card = [0] * 15
                final_card[17 - cnt_value] = 1
                return final_card
    if (len(pos_split['rocket']) > 0 or len(pos_split['bomb']) > 0) and pos_split['other_depth'] == 3:
        for i in range(single_len):
            cnt_value = getPlayMax(pos_split['single'][i])
            if cnt_value > farmer_max:
                final_card = [0] * 15
                final_card[17 - cnt_value] = 1
                return final_card
    single_value = []
    for i in range(single_len):
        value = getPlayMax(pos_split['single'][i])
        single_value.append(value)
    single_value.sort()
    if pos_split['small_triple_len'] >= len(single_value):
        return [0] * 15
    single_value = single_value[pos_split['small_triple_len']: ]
    for i in range(single_len):
        value = getPlayMax(pos_split['single'][i])
        if value == single_value[0]:
            return pos_split['single'][i]
    return [0] * 15

def playSingleReverse(pos_split):
    single_len = len(pos_split['single'])
    max_value = 0
    max_single_index = 0
    for i in range(single_len):
        value = getPlayMax(pos_split['single'][i])
        if value > max_value:
            max_value = value
            max_single_index = i
    return pos_split['single'][max_single_index]


#if have small value, play small first
def playSmall(pos_split):
    single_len = len(pos_split['single'])
    triple_len = len(pos_split['triple'])
    double_len = len(pos_split['double'])
    small_single = 0
    small_double = 0
    small_single_value = []
    small_double_value = []
    for i in range(single_len):
        value = getPlayMax(pos_split['single'][i])
        if value <= 6:
            small_single += 1
            small_single_value.append(value)
    for i in range(double_len):
        value = getPlayMax(pos_split['double'][i])
        if value <= 6:
            small_double += 1
            small_double_value.append(value)
    if small_single + small_double - triple_len >= 3 and pos_split['remain_len'] >= 15:
        if small_single > triple_len:
            small_single_value = small_single_value[triple_len:]
            small_single_value.sort()
            for i in range(single_len):
                value = getPlayMax(pos_split['single'][i])
                if value == small_single_value[0]:
                    return pos_split['single'][i]
        else:
            triple_len -= small_single
            if small_double > triple_len:
                small_double_value = small_double_value[triple_len:]
                small_double_value.sort()
                for i in range(double_len):
                    value = getPlayMax(pos_split['double'][i])
                    if value == small_double_value[0]:
                        return pos_split['double'][i]
    return [0] * 15

def checkSingleMax(gameinfo, max_value):
    for i in range(15):
        if (gameinfo['handCard'][1][i] >= 1 or gameinfo['handCard'][2][i] >= 1) and 17 - i > max_value:
            return False
    return True

def checkDoubleMax(gameinfo, max_value):
    for i in range(15):
        if (gameinfo['handCard'][1][i] >= 2 or gameinfo['handCard'][2][i] >= 2)and 17 - i > max_value:
            return False
    return True


#if only two depth, play biggest first
def playDepthTwo(gameinfo, pos_split):
    single_len = len(pos_split['single'])
    max_value = 0
    for i in range(single_len):
        value = getPlayMax(pos_split['single'][i])
        if value > max_value:
            max_value = value
    if max_value != 0 and checkSingleMax(gameinfo, max_value):
        final_card = [0] * 15
        final_card[17 - max_value] = 1
        return final_card
    double_len = len(pos_split['double'])
    max_value = 0
    for i in range(double_len):
        value = getPlayMax(pos_split['double'][i])
        if value > max_value:
            max_value = value
    if max_value != 0 and checkDoubleMax(gameinfo, max_value):
        final_card = [0] * 15
        final_card[17 - max_value] = 2
        return final_card
    return [0] * 15

def playBombTwo(gameinfo, pos_split):
    bomb_len = len(pos_split['bomb'])
    must_play = lordMustPlay(gameinfo)
    if bomb_len == 1 and (pos_split['sum'] == 7 or pos_split['sum'] == 8): #play 4 + 2
        if pos_split['small_single'] >= 3:
            play_card = pos_split['bomb'][0]
            small_single = []
            for i in range(len(pos_split['single'])):
                value = getPlayMax(pos_split['single'][i])
                if value <= 10:
                    small_single.append(value)
            small_single.sort()
            play_card[17 - small_single[0]] = 1
            play_card[17 - small_single[1]] = 1
            return play_card
    single_len = len(pos_split['single'])
    max_value = 0
    bigger_num = 0
    for i in range(15):
        if (gameinfo['handCard'][1][i] > 0 or gameinfo['handCard'][2][i] > 0) and 17 - i > max_value:
            max_value = 17 - i
    small_single = 0
    for i in range(single_len):
        value = getPlayMax(pos_split['single'][i])
        if value < max_value:
            small_single += 1
    if bomb_len >= 1 and must_play:
        if small_single >= 2:
            play_card = pos_split['bomb'][0]
            small_single = []
            for i in range(len(pos_split['single'])):
                value = getPlayMax(pos_split['single'][i])
                if value < max_value:
                    small_single.append(value)
            small_single.sort()
            play_card[17 - small_single[0]] = 1
            play_card[17 - small_single[1]] = 1
            return play_card
    return [0] * 15


def playSingleDouble(gameinfo, pos_split):
    if pos_split['small_double'] >= 2 or pos_split['small_single'] >= 2:
        if pos_split['small_double'] >= pos_split['small_single']:
            has_two = gameinfo['handRemain'][1] == 2 or gameinfo['handRemain'][2] == 2
            if has_two and pos_split['depth'] != 1:
                play_card = playSingle(gameinfo, pos_split)
                value = getPlayMin(play_card)
                if sum(play_card) != 0 and value <= 13:
                    return play_card
                play_card = playDouble(pos_split)
                value = getPlayMin(play_card)
                if value <= 13:
                    final_card = [0] * 15
                    final_card[17 - value] = 1
                    return final_card
            play_card = playDouble(pos_split)
            return play_card
        elif pos_split['small_double'] < pos_split['small_single']:
            play_card = playSingle(gameinfo, pos_split)
            if pos_split['depth'] == 1:
                return play_card
            has_one = gameinfo['handRemain'][1] == 1 or gameinfo['handRemain'][2] == 1
            if has_one:
                return [0] * 15
            return play_card
    return [0] * 15

def activePlay(gameinfo, id):
    pos_split = splitApp.get_split(gameinfo['handCard'][id], REVERSE_SPLIT)
    if DEBUG == 1:
        printSplit(pos_split)
        print("")
    addAditionalInfo(gameinfo, pos_split)
    rocket = pos_split['rocket']
    rocket_len = len(rocket)
    bomb = pos_split['bomb']
    bomb_len = len(bomb)
    triple = pos_split['triple']
    triple_len = len(triple)
    straight = pos_split['straight']
    straight_len = len(straight)
    double_straight = pos_split['double_straight']
    double_straight_len = len(double_straight)
    single = pos_split['single']
    single_len = len(single)
    double = pos_split['double']
    double_len = len(double)
    must_play = lordMustPlay(gameinfo)
    if must_play == False:
        play_card = playSmall(pos_split)
        if sum(play_card) != 0:
            return play_card
    play_card = playBombTwo(gameinfo, pos_split)
    if sum(play_card) != 0:
        return play_card
    if straight_len > 0:
        play_card = playStraight(pos_split)
        if pos_split['other_depth'] == 1:
            return play_card
        if pos_split['sum'] >= 17 and sum(play_card) >= 9:
            if single_len >= 3:
                playSingle(gameinfo, pos_split)
        min_value = getPlayMin(play_card)
        max_value = getPlayMax(play_card)
        if max_value <= 10:
            return play_card
        if pos_split['other_depth'] <= 4:
            return play_card
        if min_value >= 8 and pos_split['remain_len'] >= 12:
            play_card = [0] * 15
    if double_straight_len > 0:
        play_card = playDoubleStraight(pos_split)
        value = getPlayMin(play_card)
        if pos_split['other_depth'] == 1:
            return play_card
        if value < 6:
            return play_card
        if pos_split['other_depth'] <= 3:
            return play_card
    #lord QQ 555 66   farmer:999 66 J T   --- 2 A
    if pos_split['other_depth'] == 2:
        play_card = playDepthTwo(gameinfo, pos_split)
        if sum(play_card) != 0:
            return play_card
    if triple_len > 0:
        play_card = playTriple(pos_split)
        if pos_split['other_depth'] == 1:
            return play_card
        value = getPlayMax(play_card)
        if sum(play_card) == 0: #if x very bigger
            value = 20
        if value <= 12:  #less than 10, play 3+x
            return play_card
        if value <= 13 and pos_split['remain_len'] < 10:
            return play_card
        #if greated than 10: only depth < 4
        if value == 14 and pos_split['other_depth'] < 4:
            return play_card
        if value == 15 and pos_split['other_depth'] < 3:
            return play_card
    if double_straight_len > 0:
        play_card = playDoubleStraight(pos_split)
        value = getPlayMin(play_card)
        if pos_split['other_depth'] == 1:
            return play_card
        if value < 10:
            return play_card
        if pos_split['other_depth'] <= 3:
            return play_card
    play_card = playSingleDouble(gameinfo, pos_split)
    if sum(play_card) != 0:
        return play_card
    if double_len > 0:
        has_two = gameinfo['handRemain'][1] == 2 or gameinfo['handRemain'][2] == 2
        if has_two and pos_split['depth'] != 1:
            play_card = playSingle(gameinfo, pos_split)
            value = getPlayMin(play_card)
            if sum(play_card) != 0 and value <= 13:
                return play_card
            play_card = playDouble(pos_split)
            value = getPlayMin(play_card)
            if value <= 13:
                final_card = [0] * 15
                final_card[17 - value] = 1
                return final_card
        play_card = playDouble(pos_split)
        if pos_split['other_depth'] == 1:
            return play_card
        value = getPlayMax(play_card)
        if value <= 12:
            return play_card
        if value == 13 and pos_split['other_depth'] <= 3:
            return play_card
        if value >= 14 and value <= 15 and pos_split['other_depth'] <= 2:
            return play_card
        if single_len == 1:
            return play_card
        if double_len > single_len:
            return play_card
    if single_len > 0:
        play_card = playSingle(gameinfo, pos_split)
        if pos_split['other_depth'] == 1:
            return play_card
        has_one = gameinfo['handRemain'][1] == 1 or gameinfo['handRemain'][2] == 1
        if has_one:
            play_card = playSingleReverse(pos_split)
        return play_card
    if rocket_len > 0:
        play_card = pos_split['rocket'][0]
        if pos_split['depth'] <= 1:
            return play_card
    if bomb_len > 0:
        play_card = playBomb(pos_split)
        if pos_split['depth'] <= bomb_len:
            return play_card
    return [0] * 15

##########################################################
## lord passive play card
#########

def checkCard(gameinfo, pos_split, play_card):
    gameinfo['handCard'][0] = list(np.array(gameinfo['handCard'][0]) - np.array(play_card))
    single_len = len(pos_split['single'])
    max_value = 0
    bigger_num = 0
    for i in range(15):
        if (gameinfo['handCard'][1][i] > 0 or gameinfo['handCard'][2][i] > 0) and 17 - i > max_value:
            max_value = 17 - i
    small_single = 0
    for i in range(single_len):
        value = getPlayMax(pos_split['single'][i])
        if value < max_value:
            small_single += 1
    for i in range(15):
        if 17 - i > max_value and gameinfo['handCard'][0][i] > 0:
            bigger_num += gameinfo['handCard'][0][i]
    if bigger_num < small_single:
        gameinfo['handCard'][0] = list(np.array(gameinfo['handCard'][0]) + np.array(play_card))
        return False
    max_value = 0
    bigger_num = 0
    for i in range(15):
        if (gameinfo['handCard'][1][i] > 1 or gameinfo['handCard'][2][i] > 1) and (17 - i) > max_value:
            max_value = 17 - i
    double_len = len(pos_split['double'])
    for i in range(double_len):
        value = getPlayMax(pos_split['double'][i])
        if value > max_value:
            bigger_num += 1
    if bigger_num < pos_split['small_double']:
        gameinfo['handCard'][0] = list(np.array(gameinfo['handCard'][0]) + np.array(play_card))
        return False
    gameinfo['handCard'][0] = list(np.array(gameinfo['handCard'][0]) + np.array(play_card))
    return True

def getNegSingle(triple_value, pos_split, must_play):
    single_len = len(pos_split['single'])
    min_value = 20
    for i in range(single_len):
        cnt_value = getPlayMax(pos_split['single'][i])
        if cnt_value < min_value:
            min_value = cnt_value
    if min_value != 20 and triple_value >= 3 and triple_value <= 6:
        if min_value - triple_value <= 5 or must_play:
            return min_value
    if min_value != 20 and triple_value >= 7 and triple_value <= 11:
        if min_value <= 12 or must_play:
            return min_value
    if min_value != 20 and triple_value >= 12:
        if min_value < triple_value or must_play:
            return min_value
    if min_value != 20 and pos_split['other_depth'] <= 2:
        return min_value
    if min_value < triple_value:
        return min_value
    straight_len = len(pos_split['straight'])
    min_value = 20
    for i in range(straight_len):
        cnt_len = sum(pos_split['straight'][i])
        if cnt_len >= 6:
            for j in range(15):
                if pos_split['straight'][i][j] >= 1 and 17 - j < min_value:
                    min_value = 17 - j
            if min_value < triple_value or must_play:
                return min_value
    double_len = len(pos_split['double'])
    min_value = 20
    for i in range(double_len):
        cnt_value = getPlayMax(pos_split['double'][i])
        if cnt_value < min_value:
            min_value = cnt_value
    if min_value != 20 and triple_value >= 3 and triple_value <= 6:
        if min_value - triple_value <= 5 or must_play:
            return min_value
    if min_value != 20 and triple_value >= 7 and triple_value <= 11:
        if min_value <= 12 or must_play:
            return min_value
    if min_value != 20 and triple_value >= 12 and triple_value <= 13:
        if min_value < triple_value or must_play:
            return min_value
    if min_value != 20 and pos_split['remain_len'] <= 5:
        return min_value

    return min_value if min_value != 20 else 0


def getNegDouble(triple_value, pos_split):
    double_len = len(pos_split['double'])
    min_value = 20
    for i in range(double_len):
        cnt_value = getPlayMax(pos_split['double'][i])
        if cnt_value < min_value:
            min_value = cnt_value
    if min_value != 20 and triple_value >= 3 and triple_value <= 6:
        if min_value - triple_value <= 5:
            return min_value
    if min_value != 20 and triple_value >= 7 and triple_value <= 11:
        if min_value <= 12:
            return min_value
    if min_value != 20 and triple_value >= 12 and triple_value <= 13:
        if min_value < triple_value:
            return min_value
    if min_value != 20 and pos_split['sum'] <= 7:
        return min_value
    if triple_value >= 3 and triple_value <= 6:
        if min_value <= 11:
            return min_value
    double_straight_len = len(pos_split['double_straight'])
    for i in range(double_straight_len):
        cnt_card = pos_split['double_straight'][i]
        min_value = getPlayMin(cnt_card)
        if min_value >= 7 and min_value <= 11:
            return min_value
    return 0

def negPlayBomb(gameinfo, pos_split):
    other_bomb = gameinfo['lastCard']
    bombs = pos_split['bomb']
    bomb_len = len(bombs)
    other_value = getPlayMax(other_bomb)
    min_value = 20
    for i in range(bomb_len):
        cnt_value = getPlayMax(bombs[i])
        if cnt_value > other_value and cnt_value < min_value:
            min_value = cnt_value
    for i in range(bomb_len):
        cnt_value = getPlayMax(bombs[i])
        if cnt_value == min_value:
            return bombs[i]
    return [0] * 15

def negPlaySingleReverse(gameinfo, pos_split):
    other_single = gameinfo['lastCard']
    single_len = len(pos_split['single'])
    other_value = getPlayMin(other_single)
    single_max_value = 0
    last_person = gameinfo['last']
    last_remain = gameinfo['handRemain'][last_person]
    small_single = 0
    return_value = []
    for i in range(single_len):
        cnt_value = getPlayMax(pos_split['single'][i])
        if cnt_value <= 13:
            small_single += 1
        if cnt_value > other_value and single_max_value < cnt_value:
            single_max_value = cnt_value
    if single_max_value != 0 and single_max_value >= 14:
        final_card = [0] * 15
        final_card[17 - single_max_value] = 1
        return final_card
    single_index = 0
    for i in range(single_len):
        cnt_value = getPlayMax(pos_split['single'][i])
        if cnt_value == single_max_value and single_len >= 2:
            return pos_split['single'][i]
    double_max_value = 0
    double_len = len(pos_split['double'])
    for i in range(double_len):
        cnt_value = getPlayMax(pos_split['double'][i])
        if double_max_value < cnt_value and cnt_value > other_value:
            double_max_value = cnt_value
    triple_len = len(pos_split['triple'])
    triple_max_value = 0
    for i in range(triple_len):
        cnt_value = getPlayMax(pos_split['triple'][i])
        if cnt_value > triple_max_value and cnt_value > other_value:
            triple_max_value = cnt_value
    two_bomb_len = 0
    bomb_len = len(pos_split['bomb'])
    for i in range(bomb_len):
        value = getPlayMax(pos_split['bomb'][i])
        if value == 15:
            two_bomb_len = 1
    final_max_value = max(triple_max_value, double_max_value)
    return_value.append(final_max_value)
    if final_max_value != 0 and (two_bomb_len == 0 or final_max_value >= 14):
        final_card = [0] * 15
        final_card[17 - final_max_value] = 1
        return final_card
    # split 2222
    if two_bomb_len > 0:
        if pos_split['depth'] <= 2:
            return pos_split['bomb'][0]
        if pos_split['sum'] <= 10 and small_single - len(pos_split['triple']) >= 3 and other_value < 15:
            final_card = [0] * 15
            final_card[2] = 1
            return final_card
    # split rocket
    rocket_len = len(pos_split['rocket'])
    if rocket_len > 0:
        if pos_split['sum'] <= 8 and small_single - len(pos_split['triple']) >= 3:
            final_card = [0] * 15
            final_card[1] = 1
            return final_card
        if pos_split['depth'] <= 2:
            return pos_split['rocket'][0]
    straight_len = len(pos_split['straight'])
    max_value = 0
    for i in range(straight_len):
        cnt_value = getPlayMax(pos_split['straight'][i])
        if sum(pos_split['straight'][i]) > 5 and cnt_value > other_value and max_value < cnt_value:
            max_value = cnt_value
    for i in range(straight_len):
        cnt_value = getPlayMax(pos_split['straight'][i])
        if sum(pos_split['straight'][i]) > 5 and max_value == cnt_value:
            final_card = [0] * 15
            final_card[17 - cnt_value] += 1
            return final_card
    for i in range(single_len):
        cnt_value = getPlayMax(pos_split['single'][i])
        if cnt_value == single_max_value:
            return pos_split['single'][i]
    return [0] * 15


def negPlaySingle(gameinfo, pos_split):
    other_single = gameinfo['lastCard']
    single_len = len(pos_split['single'])
    other_value = getPlayMin(other_single)
    min_value = 20
    last_person = gameinfo['last']
    last_remain = gameinfo['handRemain'][last_person]
    small_single = 0
    no_joker = noJoker(gameinfo)
    single_value = []
    for i in range(single_len):
        cnt_value = getPlayMax(pos_split['single'][i])
        if cnt_value <= 13:
            small_single += 1
        if cnt_value > other_value:
            single_value.append(cnt_value)
        if cnt_value > other_value and min_value > cnt_value:
            min_value = cnt_value
    if no_joker and pos_split['remain_len'] == 2:
        for i in range(single_len):
            cnt_value = getPlayMax(pos_split['single'][i])
            if cnt_value == 15 and cnt_value > other_value:
                final_card = [0] * 15
                final_card[2] = 1
                return final_card
    if len(pos_split['rocket']) > 0 and pos_split['remain_len'] == 3:
        for i in range(single_len):
            cnt_value = getPlayMax(pos_split['single'][i])
            if cnt_value == 15 and cnt_value > other_value:
                final_card = [0] * 15
                final_card[2] = 1
                return final_card
    single_index = 0

    for i in range(single_len):
        cnt_value = getPlayMax(pos_split['single'][i])
        if cnt_value == min_value:
            if min_value == 17 and (small_single - len(pos_split['triple']) >= 3): # or pos_split['small_double']) >= 4:
                break
            if min_value == 16 and (small_single - len(pos_split['triple']) >= 3):
                break
            if (min_value == 16 or min_value == 16) and (len(pos_split['bomb']) == 0 and pos_split['small_double'] == 2):
                break
            return pos_split['single'][i]
    """
    if len(single_value) > pos_split['small_triple_len']:
        single_value.sort()
        single_value = single_value[pos_split['small_triple_len']:]
        for i in range(single_len):
            cnt_value = getPlayMax(pos_split['single'][i])
            if cnt_value == single_value[0]:
                if (cnt_value == 16 or cnt_value == 17) and (small_single - pos_split['small_triple_len'] >= 3):
                    break
                if (cnt_value == 16 or cnt_value == 17) and (len(pos_split['bomb']) == 0 and pos_split['small_double'] == 2):
                    break
                #if (cnt_value == 17 or cnt_value == 16) and (pos_split['small_double'] + pos_split['small_single'] - pos_split['small_triple_len'] >= 3):
                #    break
                return pos_split['single'][i]
    """
    double_len = len(pos_split['double'])
    for i in range(double_len):
        cnt_value = getPlayMax(pos_split['double'][i])
        if cnt_value > other_value and cnt_value >= 14:
            final_card = [0] * 15
            final_card[17 - cnt_value] += 1
            return final_card
        if cnt_value > other_value and cnt_value >= 11 and sum(gameinfo['handCard'][gameinfo['turn']]) <= 3:
            final_card = [0] * 15
            final_card[17 - cnt_value] += 1
            return final_card
        if last_remain <= 2 and cnt_value > other_value:
            final_card = [0] * 15
            final_card[17 - cnt_value] += 1
            return final_card
    triple_len = len(pos_split['triple'])
    for i in range(triple_len):
        cnt_value = getPlayMax(pos_split['triple'][i])
        if cnt_value >= 13 and cnt_value > other_value:
            final_card = [0] * 15
            final_card[17 - cnt_value] = 1
            return final_card
        if last_remain <= 2 and cnt_value > other_value:
            final_card = [0] * 15
            final_card[17 - cnt_value] = 1
            return final_card
    straight_len = len(pos_split['straight'])
    max_value = 0
    for i in range(straight_len):
        cnt_value = getPlayMax(pos_split['straight'][i])
        if sum(pos_split['straight'][i]) > 5 and cnt_value > other_value and max_value < cnt_value:
            max_value = cnt_value
    for i in range(straight_len):
        cnt_value = getPlayMax(pos_split['straight'][i])
        if sum(pos_split['straight'][i]) > 5 and max_value == cnt_value:
            final_card = [0] * 15
            final_card[17 - cnt_value] += 1
            return final_card
    #split 2222
    two_bomb_len = 0
    bomb_len = len(pos_split['bomb'])
    for i in range(bomb_len):
        value = getPlayMax(pos_split['bomb'][i])
        if value == 15:
            two_bomb_len = 1
    if two_bomb_len > 0:
        if pos_split['sum'] <= 10 and small_single >= 3 and other_value < 15:
            final_card = [0] * 15
            final_card[2] = 1
            return final_card

    #split rocket
    rocket_len = len(pos_split['rocket'])
    if rocket_len > 0:
        if pos_split['sum'] <= 8 and small_single >= 3:
            final_card = [0] * 15
            final_card[1] = 1
            return final_card
    return [0] * 15

def negPlaySingleDepthTwo(gameinfo, pos_split):
    single_len = len(pos_split['single'])
    other_value = getPlayMax(gameinfo['lastCard'])
    max_value = 0
    for i in range(single_len):
        value = getPlayMax(pos_split['single'][i])
        if value > max_value and value > other_value:
            max_value = value
    if max_value != 0 and checkSingleMax(gameinfo, max_value):
        final_card = [0] * 15
        final_card[17 - max_value] = 1
        return final_card
    return [0] * 15

def negPlayDouble(gameinfo, pos_split):
    other_double = gameinfo['lastCard']
    other_value = getPlayMax(other_double)
    double_len = len(pos_split['double'])
    min_value = 20
    for i in range(double_len):
        cnt_value = getPlayMax(pos_split['double'][i])
        if cnt_value > other_value and min_value > cnt_value:
            min_value = cnt_value
    lord_must_play = lordMustPlay(gameinfo)
    farmer_card = farmerCard(gameinfo)
    for i in range(double_len):
        cnt_value = getPlayMax(pos_split['double'][i])
        if cnt_value == min_value and ((cnt_value <= 14 and cnt_value - other_value <= 11) or lord_must_play):
            return pos_split['double'][i]
        if cnt_value == min_value and cnt_value == 15 and ((pos_split['small_single'] + pos_split['small_double'] <= 2 and pos_split['remain_len'] < 7) or lord_must_play or farmer_card < 4):# and farmer_card < 9:
            return pos_split['double'][i]
        if cnt_value == min_value and cnt_value == 15 and (pos_split['small_single'] + pos_split['small_double'] == 0):
            return pos_split['double'][i]
        if cnt_value == min_value and cnt_value == 15 and other_value == 14:
            return pos_split['double'][i]
    double_straight_len = len(pos_split['double_straight'])
    for i in range(double_straight_len):
        play_card = pos_split['double_straight'][i]
        tail_value = getPlayMin(play_card)
        head_value = getPlayMax(play_card)
        if tail_value >= 8:
            if tail_value > other_value:
                final_card = [0] * 15
                final_card[17 - tail_value] += 2
                return final_card
            if head_value > other_value:
                final_card = [0] * 15
                final_card[17 - head_value] += 2
                return final_card
    triple_len = len(pos_split['triple'])
    for i in range(triple_len):
        value = getPlayMax(pos_split['triple'][i])
        if (value == 14 or value == 15) and value > other_value:
            if lord_must_play or farmer_card < 8:
                final_card = [0] * 15
                final_card[17 - value] += 2
                return final_card
    return [0] * 15

def negPlayDoubleDepthTwo(gameinfo, pos_split):
    double_len = len(pos_split['double'])
    other_value = getPlayMax(gameinfo['lastCard'])
    max_value = 0
    for i in range(double_len):
        value = getPlayMax(pos_split['double'][i])
        if value > max_value and value > other_value:
            max_value = value
    if max_value != 0 and checkDoubleMax(gameinfo, max_value):
        final_card = [0] * 15
        final_card[17 - max_value] = 2
        return final_card
    return [0] * 15

def negPlayTriple(gameinfo, pos_split):
    other_triple = gameinfo['lastCard']
    other_value = 0
    is_single = -1
    for i in range(15):
        if other_triple[i] == 3:
            other_value = 17 - i
        if other_triple[i] == 2:
            is_single = 0
        if other_triple[i] == 1:
            is_single = 1
    triple_len = len(pos_split['triple'])
    min_value = 20
    for i in range(triple_len):
        cnt_value = getPlayMax(pos_split['triple'][i])
        if cnt_value > other_value and min_value > cnt_value:
            min_value = cnt_value
    if min_value == 15 and min_value - other_value >= 2 and gameinfo['handRemain'][gameinfo['last']] >= 3:
        return [0] * 15
    if min_value == 14 and min_value - other_value >= 3 and gameinfo['handRemain'][gameinfo['last']] >= 3:
        return [0] * 15
    for i in range(triple_len):
        cnt_value = getPlayMax(pos_split['triple'][i])
        if cnt_value == min_value:
            if is_single == 1: #3 + x
                must_play = lordMustPlay(gameinfo)
                single_value = getNegSingle(cnt_value, pos_split, must_play)
                if single_value == 0:
                    return [0] * 15
                pos_split['triple'][i][17 - single_value] += 1
                return pos_split['triple'][i]
            if is_single == -1: # 3
                return pos_split['triple'][i]
            if is_single == 0: # 3 + xx
                double_value = getNegDouble(cnt_value, pos_split)
                if double_value == 0:
                    return [0] * 15
                pos_split['triple'][i][17 - double_value] += 2
                return pos_split['triple'][i]
    return [0] * 15

def negPlayStraight(gameinfo, pos_split):
    other_straight = gameinfo['lastCard']
    other_value = getPlayMin(other_straight)
    other_len = sum(other_straight)
    min_value = 20
    straight_len = len(pos_split['straight'])
    for i in range(straight_len):
        cnt_len = sum(pos_split['straight'][i])
        cnt_value = getPlayMin(pos_split['straight'][i])
        if cnt_len == other_len and cnt_value > other_value and min_value > cnt_value:
            min_value = cnt_value
    for i in range(straight_len):
        cnt_len = sum(pos_split['straight'][i])
        cnt_value = getPlayMin(pos_split['straight'][i])
        if cnt_len == other_len and min_value == cnt_value:
            return pos_split['straight'][i]
    other_value = getPlayMax(other_straight)
    other_value_min = getPlayMin(other_straight)
    for i in range(straight_len):
        cnt_len = sum(pos_split['straight'][i])
        cnt_value = getPlayMax(pos_split['straight'][i])
        if cnt_len > other_len and cnt_len - other_len <= 2 and cnt_value > other_value:
            cnt_min = getPlayMin(pos_split['straight'][i])
            find_min = 0
            for j in range(cnt_min, cnt_value + 1):
                if j > other_value_min:
                    find_min = j
                    break
            cnt_remain = []
            for j in range(cnt_min, find_min):
                cnt_remain.append(j)
            if len(cnt_remain) == 2:
                continue
            for j in range(find_min + other_len, cnt_value):
                cnt_remain.append(j)
            if len(cnt_remain) == 2:
                if cnt_remain[0] <= 4:
                    continue
                final_card = [0] * 15
                for j in range(find_min, find_min + other_len):
                    final_card[17 - j] += 1
                return final_card
            if len(cnt_remain) == 1:
                if cnt_remain[0] <= 4:
                    continue
                final_card = [0] * 15
                for j in range(find_min, find_min + other_len):
                    final_card[17 - j] += 1
                return final_card
        if cnt_len > other_len and cnt_len - other_len >= 5:
            cnt_min = getPlayMin(pos_split['straight'][i])
            find_min = 0
            for j in range(cnt_min, cnt_value + 1):
                if j > other_value_min:
                    find_min = j
                    break
            bigger_remain = []
            less_remain = []
            for j in range(cnt_min, find_min):
                less_remain.append(j)
            for j in range(find_min + other_len, cnt_value):
                bigger_remain.append(j)
            if len(less_remain) == 0 and len(bigger_remain) >= 5:
                final_card = [0] * 15
                for j in range(find_min, find_min + other_len):
                    final_card[17 - j] += 1
                return final_card
    return [0] * 15

def negPlayStraightDouble(gameinfo, pos_split):
    other_double_straight = gameinfo['lastCard']
    other_value = getPlayMin(other_double_straight)
    other_len = sum(other_double_straight) // 2
    min_value = 20
    double_straight_len = len(pos_split['double_straight'])
    must_play = gameinfo['handRemain'][2] == 1 or gameinfo['handRemain'][1] == 1 or gameinfo['handRemain'][2] == 2 or gameinfo['handRemain'][1] == 2
    for i in range(double_straight_len):
        cnt_len = sum(pos_split['double_straight'][i]) // 2
        cnt_value = getPlayMin(pos_split['double_straight'][i])
        if cnt_len == other_len and cnt_value > other_value and min_value > cnt_value and (cnt_value - other_value <= 8 or must_play):
            min_value = cnt_value
    for i in range(double_straight_len):
        cnt_len = sum(pos_split['double_straight'][i]) // 2
        cnt_value = getPlayMin(pos_split['double_straight'][i])
        if cnt_len == other_len and cnt_value == min_value:
            return pos_split['double_straight'][i]
    for i in range(double_straight_len):
        cnt_len = sum(pos_split['double_straight'][i]) // 2
        cnt_value = getPlayMin(pos_split['double_straight'][i])
        if cnt_len > other_len and cnt_value > other_value and (cnt_value - other_value <= 8 or must_play):
            final_card = [0] * 15
            for i in range(cnt_value, cnt_value + other_len):
                final_card[17 - i] += 2
            return final_card
    return [0] * 15


def checkTripleMax(gameinfo, triple_value):
    for i in range(15):
        if (gameinfo['handCard'][1][i] >= 3 or gameinfo['handCard'][2][i] >= 3) and 17 - i > triple_value:
            return False
        if gameinfo['handCard'][1][i] == 4 or gameinfo['handCard'][2][i] == 4:
            return False
    return True


def negActiveBombRocket(gameinfo, pos_split):
    rocket_len = len(pos_split['rocket'])
    bomb_len = len(pos_split['bomb'])
    card_type, max_num = gameApp.cardType(gameinfo['lastCard'])
    #return [0] * 15
    if pos_split['depth'] <= (bomb_len + rocket_len) * 2:
        if bomb_len > 0:
            if card_type == 1:
                play_card = negPlayBomb(gameinfo, pos_split)
                if sum(play_card) == 0:
                    if rocket_len > 0:
                        return pos_split['rocket'][0]
            else:
                return playBomb(pos_split)
        if rocket_len > 0:
            return pos_split['rocket'][0]
    if pos_split['depth'] <= (bomb_len + rocket_len) * 2 + 1:  # one bomb + two others(others can be straight or triple)
        if card_type == 1:
            play_card = negPlayBomb(gameinfo, pos_split)
        else:
            play_card = playBomb(pos_split)
        if sum(play_card) == 0:
            if rocket_len > 0:
                play_card = pos_split['rocket'][0]
            else:
                return [0] * 15
        if len(pos_split['straight']) > 0:
            if len(pos_split['straight']) == 2:
                len_1 = len(pos_split['straight'][0])
                len_2 = len(pos_split['straight'][1])
                value_1 = getPlayMin(pos_split['straight'][0])
                value_2 = getPlayMin(pos_split['straight'][1])
                straight_len = min(len_1, len_2)
                straight_value = min(value_1, value_2)
                if straight_len == 5:
                    if straight_value >= 5:
                        return play_card
                if straight_len >= 6:
                    return play_card
            if len(pos_split['straight']) == 1:
                straight_len = len(pos_split['straight'][0])
                value = getPlayMin(pos_split['straight'][0])
                if straight_len == 5 and value >= 7:
                    return play_card
                if straight_len >= 6:
                    return play_card
        if len(pos_split['triple']) > 0:
            value = getPlayMax(pos_split['triple'][0])
            if checkTripleMax(gameinfo, value):
                return play_card
        single_len = len(pos_split['single'])
        big_value = 0
        for i in range(single_len):
            value = getPlayMax(pos_split['single'][i])
            if value >= 15:
                big_value += 1
        if big_value >= 1:
            return play_card
        if checkCard(gameinfo, pos_split, play_card):
            return play_card
    return [0] * 15


def negPlay(gameinfo, id):
    pos_split = splitApp.get_split(gameinfo['handCard'][id], REVERSE_SPLIT)
    if DEBUG == 1:
        printSplit(pos_split)
        print("")
    addAditionalInfo(gameinfo, pos_split)
    rocket = pos_split['rocket']
    rocket_len = len(rocket)
    bomb = pos_split['bomb']
    bomb_len = len(bomb)
    triple = pos_split['triple']
    triple_len = len(triple)
    straight = pos_split['straight']
    straight_len = len(straight)
    double_straight = pos_split['double_straight']
    double_straight_len = len(double_straight)
    single = pos_split['single']
    single_len = len(single)
    double = pos_split['double']
    double_len = len(double)
    last_person = gameinfo['last']
    remain_last = gameinfo['handCard'][last_person]
    card_type, max_num = gameApp.cardType(gameinfo['lastCard'])
    play_card = [0] * 15
    if card_type == 0: #rocket
        return [0] * 15
    if card_type == 1:#bomb
        if bomb_len <= 0:
            return [0] * 15
    if card_type == 2: #single
        if pos_split['depth'] - rocket_len - bomb_len == 2:
            play_card = negPlaySingleDepthTwo(gameinfo, pos_split)
            if sum(play_card) != 0:
                return play_card
        has_one = gameinfo['handRemain'][1] == 1 or gameinfo['handRemain'][2] == 1
        if has_one:
            play_card = negPlaySingleReverse(gameinfo, pos_split)
        else:
            play_card = negPlaySingle(gameinfo, pos_split)
        if sum(play_card) != 0:
            return play_card
        if bomb_len > 0:
            play_card = negActiveBombRocket(gameinfo, pos_split)
            if sum(play_card) != 0:
                return play_card
        if rocket_len > 0:
            final_card = [0] * 15
            if pos_split['depth'] >= pos_split['other_depth'] * 2:
                final_card[0] = 1
                final_card[1] = 1
                return final_card
            if pos_split['depth'] <= 3 or has_one:
                final_card[1] = 1
                return final_card
    if card_type == 3: #double
        if pos_split['depth'] - rocket_len - bomb_len == 2:
            play_card = negPlayDoubleDepthTwo(gameinfo, pos_split)
            if sum(play_card) != 0:
                return play_card
        play_card = negPlayDouble(gameinfo, pos_split)
        if sum(play_card) != 0:
            return play_card
    if card_type == 4: #triple
        play_card = negPlayTriple(gameinfo, pos_split)
        #if pos_split['depth'] <= 3:
        #    return ai2App.getNextMove(gameinfo, id)
        if sum(play_card) != 0:
            return play_card
    if card_type == 5: #straight
        play_card = negPlayStraight(gameinfo, pos_split)
        if sum(play_card) != 0:
            return play_card
    if card_type == 6: #straight double
        play_card = negPlayStraightDouble(gameinfo, pos_split)
        if sum(play_card) != 0:
            return play_card
    #play_card = ai2App.getNextMove(gameinfo, id)
    if sum(play_card) == 0 or lordMustPlay(gameinfo):
        if lordMustPlay(gameinfo):
            if bomb_len > 0:
                if card_type == 1:
                    return negPlayBomb(gameinfo, pos_split)
                else:
                    return playBomb(pos_split)
            if rocket_len > 0:
                return pos_split['rocket'][0]
        if bomb_len > 0:
            play_card = negActiveBombRocket(gameinfo, pos_split)
            if sum(play_card) != 0:
                return play_card
        if rocket_len > 0:
            play_card = negActiveBombRocket(gameinfo, pos_split)
            if sum(play_card) != 0:
                return play_card

    return [0] * 15



def getNextMove(gameinfo, id):
    copy_game = copy.deepcopy(gameinfo)
    #printCard(copy_game['handCard'][0])
    #print("")
    if id == 0:
        if sum(gameinfo['lastCard']) == 0:
            play_card = activePlay(copy_game, id)
            #print(play_card)
            if sum(play_card) == 0:
                return ai2App.getNextMove(gameinfo, id)
            else:
                return play_card
        else:
            return negPlay(copy_game, id)
    else:
        if sum(copy_game['lastCard']) == 0:
            play_card = farmerExpApp.activePlay(copy_game, id)
            if sum(play_card) == 0:
                return ai2App.getNextMove(gameinfo, id)
            else:
                return play_card
        else:
            last_person = copy_game['last']
            if last_person == 0:
                return farmerExpApp.negPlayLord(copy_game, id)
            else:
                return farmerExpApp.negPlayTeammate(copy_game, id)


def getLord(play_card):
    sum = play_card[0] + play_card[1] + play_card[2]
    if sum >= 3:
        return True
    have_joker = play_card[0] + play_card[1]
    have_joker = have_joker >= 1
    if have_joker and sum >= 2:
        return True
    pos_split = splitApp.get_split(play_card)
    if pos_split['depth'] <= 4:
        return True
    return False

if __name__ == '__main__':
    gameinfo = gameApp.newGame()
    gameinfo['last'] = 0
    #gameinfo['turn'] = 0
    #gameinfo['handCard'][1] = [0, 0, 1, 2, 0, 0, 0, 3, 0, 0, 2, 0, 0, 0, 0]
    gameinfo['handCard'][1] = [0, 0, 2, 3, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0]
    gameinfo['handCard'][2] = [0, 0, 0, 1, 1, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0]
    gameinfo['handCard'][0] = [0, 0, 0, 0, 0, 0, 1, 0, 0, 3, 0, 1, 2, 0, 0]
    for i in range(3):
        gameinfo['handRemain'][i] = sum(gameinfo['handCard'][i])
    #gameinfo['lastCard'] = [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1]
    #gameinfo['lastCard'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    #gameinfo['lastCard'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    #gameinfo['lastCard'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    #gameinfo['lastCard'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    #gameinfo['lastCard'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #gameinfo['lastCard'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #gameinfo['lastCard'] = [0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    #gameinfo['lastCard'] = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    #gameinfo['lastCard'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    gameinfo['lastCard'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    #result = ai2App.getNextMove(gameinfo, 1)
    test = []
    result = getNextMove(gameinfo, 0)
    print(result)