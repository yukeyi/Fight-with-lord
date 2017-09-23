# -*- coding: utf-8 -*-
# Author: Zhao Zhiheng
# Card functions

#convert count to flower
import copy

def convertC2F(card, handCard):
	tmp = copy.copy(card)
	tmp2 = copy.copy(handCard)
	result = [0] * 15
	for i in range(15):
		for j in [8, 4, 2, 1]:
			if tmp[i] > 0 and tmp2[i] >= j:
				result[i] += j
				tmp[i] -= 1
				tmp2[i] -= j
	return result


def convertF2C(card):
	tmp = copy.copy(card)
	result = [0] * 15
	for i in range(15):
		for j in [8, 4, 2, 1]:
			if tmp[i] >= j:
				result[i] += 1
				tmp[i] -= j
	return result
