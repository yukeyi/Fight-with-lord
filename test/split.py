# -*- coding: utf-8 -*-
import copy
import math
import numpy as np

CARD_DEFINE = ['W', 'w', '2', 'A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3']

'''
权重 (type: [base, step])
1. single: [1, 0.1]
2. double: [2, 0.1]
3. triple: [3, 0.1]
4. straight: [4, 0.1] (0.1*((len-5) + (max-7)), [0, 0.8])
5. double_straight: [5, 0.1] (0.1*((len-3) + (max-5)), [0, 1.3])
6. bomb: [7, 0.1]
7. rocket: [9, ]
'''

WEIGHT = {
    'single': lambda x: 1 + x / 10,
    'double': lambda x: 2 + x / 10,
    'triple': lambda x: 3 + x / 10,
    'straight': lambda l, m: 4 + 0.1 * ((l - 5) + (m - 4)),
    'double_straight': lambda l, m: 5 + 0.1 * ((l - 3) + (m - 2)),
    'bomb': lambda x: 7 + x / 10,
    'rocket': 9
}


# WEIGHT = {
#     'single': 1 * 2,
#     'double': 2 * 2,
#     'straight_base': 4 * 2,
#     'straight_add': 0.5,
#     'triple': 3 * 2,
#     'double_straight_base': 5 * 2,
#     'double_straight_add': 2,
#     'bomb': 7 * 2,
#     'rocket': 8 * 2
# }


class CardStyle(object):
    def __init__(self):
        self.max = 0
        self.min = 0
        self.weight = 0


class ZongCard(object):
    def __init__(self):
        self.rocket = []
        self.bomb = []
        self.triple = []
        self.straight = []
        self.double_straight = []
        self.double = []
        self.single = []


def make_double_straight(double, double_straight):
    if len(double) >= 3:
        index = 0
        j = 0
        for i in range(0, len(double) - 1, 1):
            if double[i].max + 1 == double[i + 1].max and double[i + 1].max < 12:
                index += 1
                j = double[i].max + 1
            else:
                if index >= 2:
                    card_style = CardStyle()
                    card_style.max = j
                    card_style.min = j - index
                    # card_style.weight = WEIGHT['double_straight_base'] + (card_style.max - card_style.min - 2) * WEIGHT[
                    #     'double_straight_add']
                    card_style.weight = WEIGHT['double_straight'](card_style.max - card_style.min + 1, card_style.max)
                    double_straight.append(card_style)
                index = 0

        if index >= 2:
            card_style = CardStyle()
            card_style.max = j
            card_style.min = j - index
            # card_style.weight = WEIGHT['double_straight_base'] + (card_style.max - card_style.min - 2) * WEIGHT[
            #     'double_straight_add']
            card_style.weight = WEIGHT['double_straight'](card_style.max - card_style.min + 1, card_style.max)
            double_straight.append(card_style)
    return double, double_straight


def delete_element(src, des):
    if len(des) != 0:
        for i in range(0, len(des), 1):
            for j in range(des[i].min, des[i].max + 1, 1):
                for k in range(0, len(src), 1):
                    if src[k] is None:
                        continue
                    if src[k].max == j:
                        src[k] = None

        src = [s for s in src if s is not None]
    return src, des


def traverse_card(bomb, double_straight, triple, double, hand_card, card):
    zong_card = ZongCard()
    zong_card.rocket = card['rocket']
    hand_card = copy.deepcopy(hand_card)

    # if bomb:
    #     for i in range(0, len(card['bomb']), 1):
    #         zong_card.bomb.append(card['bomb'][i])
    #         hand_card[card['bomb'][i].max] = 0
    # if double_straight:
    #     for i in range(0, len(card['double_straight']), 1):
    #         zong_card.double_straight.append(card['double_straight'][i])
    #         for j in range(card['double_straight'][i].min, card['double_straight'][i].max + 1, 1):
    #             hand_card[j] -= 2
    # if triple:
    #     for i in range(0, len(card['triple']), 1):
    #         zong_card.triple.append(card['triple'][i])
    #         hand_card[card['triple'][i].max] -= 3
    # if double:
    #     for i in range(0, len(card['double']), 1):
    #         zong_card.double.append(card['double'][i])
    #         hand_card[card['double'][i].max] -= 2

    for i in range(0, len(card['bomb']), 1):
        if bomb & (1 << i) != 0:
            zong_card.bomb.append(card['bomb'][i])
            hand_card[card['bomb'][i].max] = 0

    for i in range(0, len(card['double_straight']), 1):
        if double_straight & (1 << i) != 0:
            zong_card.double_straight.append(card['double_straight'][i])
            for j in range(card['double_straight'][i].min, card['double_straight'][i].max + 1, 1):
                hand_card[j] -= 2

    for i in range(0, len(card['triple']), 1):
        if triple & (1 << i) != 0:
            zong_card.triple.append(card['triple'][i])
            hand_card[card['triple'][i].max] -= 3

    for i in range(0, len(card['double']), 1):
        if double & (1 << i) != 0:
            zong_card.double.append(card['double'][i])
            hand_card[card['double'][i].max] -= 2
    index = 0
    i = 0
    while i < 12:
        if hand_card[i] > 0:
            index += 1
            if index == 5:
                card_style = CardStyle()
                card_style.max = i
                card_style.min = card_style.max - 4
                # card_style.weight = WEIGHT['straight_base']
                card_style.weight = WEIGHT['straight'](card_style.max - card_style.min + 1, card_style.max)
                zong_card.straight.append(card_style)
                for j in range(card_style.min, card_style.max + 1, 1):
                    hand_card[j] -= 1
                index = 0
                i = -1
        else:
            index = 0
        i += 1

    if len(zong_card.straight) != 0:
        for i in range(0, 12, 1):
            for j in range(0, len(zong_card.straight), 1):
                if hand_card[i] > 0:
                    if zong_card.straight[j].max + 1 == i:
                        zong_card.straight[j].max = i
                        hand_card[i] -= 1
                        # zong_card.straight[j].weight += WEIGHT['straight_add']
                        zong_card.straight[j].weight = WEIGHT['straight'](
                            zong_card.straight[j].max - zong_card.straight[j].min + 1,
                            zong_card.straight[j].max)
        for i in range(0, len(zong_card.straight) - 1, 1):
            if zong_card.straight[i].max + 1 == zong_card.straight[i + 1].min:
                zong_card.straight[i + 1].min = zong_card.straight[i].min
                # zong_card.straight[i + 1].weight += (zong_card.straight[i].max - zong_card.straight[i].min + 1) * \
                #                                     WEIGHT['straight_add']
                zong_card.straight[i + 1].weight = WEIGHT['straight'](
                    zong_card.straight[i + 1].max - zong_card.straight[
                        i + 1].min + 1, zong_card.straight[i + 1].max)
                zong_card.straight[i] = None
        zong_card.straight = [s for s in zong_card.straight if s is not None]

    for i in range(0, 15, 1):
        card_style = CardStyle()
        cur_card = hand_card[i]
        if cur_card == 4:
            card_style.max = i
            card_style.min = i
            # card_style.weight = WEIGHT['bomb']
            card_style.weight = WEIGHT['bomb'](card_style.max)
            zong_card.bomb.append(card_style)
        elif cur_card == 3:
            card_style.max = i
            card_style.min = i
            # card_style.weight = WEIGHT['triple']
            card_style.weight = WEIGHT['triple'](card_style.max)
            zong_card.triple.append(card_style)
        elif cur_card == 2:
            card_style.max = i
            card_style.min = i
            # card_style.weight = WEIGHT['double']
            card_style.weight = WEIGHT['double'](card_style.max)
            zong_card.double.append(card_style)
        elif cur_card == 1:
            card_style.max = i
            card_style.min = i
            # card_style.weight = WEIGHT['single']
            card_style.weight = WEIGHT['single'](card_style.max)
            zong_card.single.append(card_style)

    zong_card.double, zong_card.double_straight = make_double_straight(zong_card.double, zong_card.double_straight)
    zong_card.double, zong_card.double_straight = delete_element(zong_card.double, zong_card.double_straight)

    return zong_card


def sum_weight(zong_card):
    res = 0
    for i in range(0, len(zong_card), 1):
        res += zong_card[i].weight
    return res


def make_card(card, depth):
    res_card = dict()
    res_card['depth'] = depth
    res_card['rocket'] = []
    res_card['bomb'] = []
    res_card['triple'] = []
    res_card['straight'] = []
    res_card['double_straight'] = []
    res_card['double'] = []
    res_card['single'] = []

    for i in range(0, len(card.rocket), 1):
        card_style = card.rocket[i]
        l = [0] * 15
        l[card_style.max] = 1
        l[card_style.min] = 1
        l.reverse()
        res_card['rocket'].append(l)

    for i in range(0, len(card.bomb), 1):
        card_style = card.bomb[i]
        l = [0] * 15
        l[card_style.max] = 4
        l.reverse()
        res_card['bomb'].append(l)

    for i in range(0, len(card.triple), 1):
        card_style = card.triple[i]
        l = [0] * 15
        l[card_style.max] = 3
        l.reverse()
        res_card['triple'].append(l)

    for i in range(0, len(card.straight), 1):
        card_style = card.straight[i]
        l = [0] * 15
        for j in range(card_style.min, card_style.max + 1, 1):
            l[j] = 1
        l.reverse()
        res_card['straight'].append(l)

    for i in range(0, len(card.double_straight), 1):
        card_style = card.double_straight[i]
        l = [0] * 15
        for j in range(card_style.min, card_style.max + 1, 1):
            l[j] = 2
        l.reverse()
        res_card['double_straight'].append(l)

    for i in range(0, len(card.double), 1):
        card_style = card.double[i]
        l = [0] * 15
        l[card_style.max] = 2
        l.reverse()
        res_card['double'].append(l)

    for i in range(0, len(card.single), 1):
        card_style = card.single[i]
        l = [0] * 15
        l[card_style.max] = 1
        l.reverse()
        res_card['single'].append(l)

    return res_card


# reverse: bomb, triple, double, single, straight, double_straight
def get_split(do_not_modify_card, reverse=(False, False, False, False, False, False)):
    hand_card = copy.deepcopy(do_not_modify_card)
    hand_card.reverse()

    card = dict()
    card['depth'] = []
    card['rocket'] = []
    card['bomb'] = []
    card['triple'] = []
    card['straight'] = []
    card['double_straight'] = []
    card['double'] = []
    card['single'] = []

    if hand_card[13] == 1 and hand_card[14] == 1:
        card_style = CardStyle()
        card_style.min = 13
        card_style.max = 14
        # card_style.weight = WEIGHT['rocket']
        card_style.weight = WEIGHT['rocket']
        hand_card[13] = hand_card[14] = 0
        card['rocket'].append(card_style)

    origin_hand_card = copy.deepcopy(hand_card)

    for i in range(0, 12, 1):
        card_style = CardStyle()
        cur_card = hand_card[i]
        if cur_card == 4:
            card_style.max = i
            card_style.min = i
            # card_style.weight = WEIGHT['bomb']
            card_style.weight = WEIGHT['bomb'](card_style.max)
            hand_card[i] = 0
            card['bomb'].append(card_style)
        elif cur_card == 3:
            card_style.max = i
            card_style.min = i
            # card_style.weight = WEIGHT['triple']
            card_style.weight = WEIGHT['triple'](card_style.max)
            hand_card[i] = 0
            card['triple'].append(card_style)
        elif cur_card == 2:
            card_style.max = i
            card_style.min = i
            # card_style.weight = WEIGHT['double']
            card_style.weight = WEIGHT['double'](card_style.max)
            hand_card[i] = 0
            card['double'].append(card_style)

    card['double'], card['double_straight'] = make_double_straight(card['double'], card['double_straight'])
    card['double'], card['double_straight'] = delete_element(card['double'], card['double_straight'])

    has_bomb = False if len(card['bomb']) == 0 else True
    has_double_straight = False if len(card['double_straight']) == 0 else True
    has_triple = False if len(card['triple']) == 0 else True
    has_double = False if len(card['double']) == 0 else True

    hands = []
    # for i in range(0, has_bomb + 1, 1):
    #     for j in range(0, has_double_straight + 1, 1):
    #         for k in range(0, has_triple + 1, 1):
    #             for h in range(0, has_double + 1, 1):
    #                 zong_card = traverse_card(i, j, k, h, origin_hand_card, card)
    #                 hands.append(zong_card)

    for i in range(0, 1 if not has_bomb else int(math.pow(2, len(card['bomb']))), 1):
        for j in range(0, 1 if not has_double_straight else int(math.pow(2, len(card['double_straight']))), 1):
            for k in range(0, 1 if not has_triple else int(math.pow(2, len(card['triple']))), 1):
                for h in range(0, 1 if not has_double else int(math.pow(2, len(card['double']))), 1):
                    zong_card = traverse_card(i, j, k, h, origin_hand_card, card)
                    hands.append(zong_card)
    quanzhi = []
    depth = []
    for i in range(0, len(hands), 1):
        zong_card = hands[i]
        s = len(zong_card.rocket) + len(zong_card.bomb) + len(zong_card.triple) \
            + len(zong_card.double_straight) + len(zong_card.double) \
            + len(zong_card.straight) + len(zong_card.single)
        s -= min(len(zong_card.triple), len(zong_card.double) + len(zong_card.single))
        # s -= len(zong_card.rocket)

        q = sum_weight(zong_card.rocket) + sum_weight(zong_card.bomb) + sum_weight(zong_card.triple) \
            + sum_weight(zong_card.double_straight) + sum_weight(zong_card.double) \
            + sum_weight(zong_card.straight) + sum_weight(zong_card.single)

        depth.append(s)
        quanzhi.append(q)

    quanzhi = np.array(quanzhi)
    depth = np.array(depth)

    total = -3 * depth + quanzhi
    total_max_idx = total.argmax()

    return make_card(sort_card(hands[total_max_idx], reverse), depth[total_max_idx])

    # min_depth_idx = depth.argmin()
    # min_depth = depth[min_depth_idx]
    #
    # min_depth_idx = []
    # for i in range(0, len(depth), 1):
    #     if depth[i] == min_depth:
    #         min_depth_idx.append(i)
    #
    # max_quanzhi = quanzhi[min_depth_idx[0]]
    # max_quanzhi_idx = min_depth_idx[0]
    # for i in range(1, len(min_depth_idx), 1):
    #     if max_quanzhi < quanzhi[min_depth_idx[i]]:
    #         max_quanzhi = quanzhi[min_depth_idx[i]]
    #         max_quanzhi_idx = min_depth_idx[i]
    # # print(max_quanzhi)
    #
    # res_card = hands[max_quanzhi_idx]
    #
    # return make_card(res_card, min_depth)


# reverse: bomb, triple, double, single, straight, double_straight
def sort_card(card, reverse):
    card.bomb.sort(key=lambda x: x.max, reverse=reverse[0])
    card.triple.sort(key=lambda x: x.max, reverse=reverse[1])
    card.double.sort(key=lambda x: x.max, reverse=reverse[2])
    card.single.sort(key=lambda x: x.max, reverse=reverse[3])
    card.straight.sort(key=lambda x: x.max, reverse=reverse[4])
    card.double_straight.sort(key=lambda x: x.max, reverse=reverse[5])

    return card


if __name__ == '__main__':
    import experience as exp

    hand_card = [0, 0, 2, 0, 2, 1, 1, 1, 1, 2, 0, 0, 0, 1, 1]
    # hand_card = [0, 0, 0, 0, 0, 0, 0, 3, 1, 2, 1, 2, 2, 0, 0]
    # hand_card = [0, 0, 0, 0, 0, 4, 1, 1, 1, 1, 1, 1, 1, 0, 0]
    # hand_card = [0, 1, 4, 2, 2, 2, 0, 2, 0, 2, 2, 0, 2, 2, 0]
    # reverse: bomb, triple, double, single, straight, double_straight
    # card_split = get_split(hand_card, (True, True, True, False, True, True))
    card_split = get_split(hand_card, (1, 1, 1, 1, 1, 1))
    exp.printSplit(card_split)
    print('')
    for k in card_split.keys():
        print(k, card_split[k])
