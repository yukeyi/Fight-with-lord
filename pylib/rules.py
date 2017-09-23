# -*- coding: utf-8 -*-
# Author: Zhao Zhiheng
# Rules of Doudizhu
# Judge/Generate legal cards
# Card: Array[15]

import itertools

class Rule(object):

	def __init__(self):
		self.prior = (15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)
		return

	#return the type of card and the prior of main card (type, prior, n)
	#-1 illegal
	#0 Rocket
	#1 Bomb
	#2 single
	#3 double
	#4 triple+X
	#5 straight
	#6 double straight
	#7 flight
	#8 flight+wings
	#9 bomb+X+X

	def type(self, card):
		n = 0
		m = [0, 0, 0, 0, 0]
		p = [0, 0, 0, 0, 0]
		for i in range(15):
			c = card[i]
			n += c
			m[c] += 1
			if self.prior[i] > p[c]:
				p[c] = self.prior[i]
		#Rocket
		if card[0] == 1 and card[1] == 1 and n == 2:
			return (0, p[1], n)
		#Bomb
		if m[4] == 1 and n == 4:
			return (1, p[4], n)
		#single
		if m[1] == 1 and n == 1:
			return (2, p[1], n)
		#double
		if m[2] == 1 and n == 2:
			return (3, p[2], n)
		#triple+X
		if m[3] == 1 and n >= 3 and n <= 5 and (m[1] == 0 or m[2] == 0):
			return (4, p[3], n)
		#straight
		if m[1] == n and m[1] >= 5 and p[1] <= 12:
			a = 15 - p[1]
			b = a + n
			if sum(card[a:b]) == n:
				return (5, p[1], n)
		#double straight
		if m[2] * 2 == n and m[2] >= 3 and p[2] <= 12:
			a = 15 - p[2]
			b = a + n
			if sum(card[a:b]) == n:
				return (6, p[2], n)
		#flight
		if m[3] + m[4] >= 2:
			'''
			tc = 0
			tn = 0
			tp = 0 
			for i in range(3, 15):
				if card[i] >= 3:
					tc += 1
					if tc > 1:
						tn = tc
						tp = self.prior[i]
				else:
					tc = 0
			if tn >= 2:
				if n == tn * 3:
					return (8, tp, n)
				if (tn == n - tn * 3) or (tn == m[2] + m[4] * 2 and m[1] == 0):
					return (7, tp, n)
			'''
			triple = []
			for i in range(3, 15):
				if card[i] >= 3:
					triple.append(i)
			l = len(triple)
			for i in range(l):
				for j in range(1, l)[::-1]:
					if j - i == triple[j] - triple[i]:
						lf = j - i + 1
						lp = self.prior[triple[i]]
						if n == lf * 3:
							return (7, lp, n)
						if lf * 4 == n or (lf * 5 == n and m[2] + m[4] * 2 == lf):
							return (8, lp, n)

		#bomb+X+X
		if m[4] == 1 and m[3] == 0:
			if (m[1] == 0 and m[2] == 2) or (m[1] == 0 and m[2] == 1) or (m[1] == 2 and m[2] == 0):
				return (9, p[4], n)
		if m[4] == 2 and n == 8:
			return (9, p[4], n)
	    #illegal
		return (-1, 0, n)

	def judge(self, curCard, lastCard):
		(c_type, c_prior, c_n) = self.type(curCard)
		(l_type, l_prior, l_n) = self.type(lastCard)
		#print(c_type, l_type)
		if c_type == -1:
			return False
		if l_n == 0:
			return True
		#Rocket and bomb	
		if c_type == 0:
			return True
		if c_type == 1 and l_type != 0 and l_type != 1:
			return True

		if c_type == l_type and c_n == l_n and c_prior > l_prior:
			return True

		return False

	def genCard(self, cardTuples):
		t = [0] * 15
		for (card, n) in cardTuples:
			t[card] += n
		return t

	def findStraight(self, card):
		dims = [1, 2, 3]
		straights = ([],[],[],[])
		cur = [[],[],[],[]]
		for i in range(3, 15):
			for d in dims:
				if card[i] >= d:
					cur[d].append((i, d))
				if card[i] < d or i == 14:
					straights[d].append(cur[d])
					cur[d] = []
		return straights

	def findLargerStraight(self, straights, p_limit, l_limit, minL):
		#print(p_limit, l_limit)
		result = []
		for item in straights:
			length = len(item)
			if length < l_limit or length < minL:
				continue
			for i in range(length):
				if self.prior[item[i][0]] <= p_limit:
					continue
				for j in range(minL, length - i + 1):
					if l_limit > 0 and j != l_limit:
						continue
					result.append(item[i:(i + j)])
			#print(item, result)
		return result

	def findAllCombination(self, card, dim, n):
		result = []
		valid = []
		for i in range(15):
			for j in range(1, 5):
				if card[i] >= dim * j:
					valid.append(i)
		tmp = set(itertools.combinations(valid, n))
		for item in tmp:
			cards = []
			for i in item:
				cards.append((i, dim))
			result.append(cards)
		return result


	def generate(self, handCard, lastCard):
		(l_type, l_prior, l_n) = self.type(lastCard)
		result = []
		typelist = []
		if lastCard != [0] * 15:
			result.append([0] * 15)
			typelist.append(10)
		if l_type == 0:
			return result
		#Rocket
		if handCard[0] == 1 and handCard[1] == 1:
			result.append(self.genCard([(0, 1), (1, 1)]))
			typelist.append(0)
		#Bomb
		for i in range(2, 15):
			if handCard[i] == 4 and (l_type > 1 or self.prior[i] > l_prior):
				result.append(self.genCard([(i, 4)]))
				typelist.append(1)

		#single
		if l_type == 2 or l_n == 0:
			for i in range(15):
				if handCard[i] >= 1 and self.prior[i] > l_prior:
					result.append(self.genCard([(i, 1)]))
					typelist.append(2)
		#double
		if l_type == 3 or l_n == 0:
			for i in range(2, 15):
				if handCard[i] >= 2 and self.prior[i] > l_prior:
					result.append(self.genCard([(i, 2)]))
					typelist.append(3)
		#triple+X
		if l_type == 4 or l_n == 0:
			if l_n == 0:
				dim = [0, 1, 2]
			else:
				dim = [l_n - 3]
			for i in range(2, 15):
				if handCard[i] >= 3 and self.prior[i] > l_prior:
					if 0 in dim:
						result.append(self.genCard([(i, 3)])) # triple + none
						typelist.append(4)
					for j in range(15):
						if i == j:
							continue
						for d in dim:
							if d != 0 and handCard[j] >= d:
								result.append(self.genCard([(i, 3), (j, d)]))
								typelist.append(4)

		(dc, single, double, triple) = self.findStraight(handCard)
		#straight
		if l_type == 5 or l_n == 0:
			straights = self.findLargerStraight(single, l_prior, l_n, 5)
			for item in straights:
				result.append(self.genCard(item))
				typelist.append(5)
		#double straight
		if l_type == 6 or l_n == 0:
			straights = self.findLargerStraight(double, l_prior, l_n // 2, 3)
			for item in straights:
				result.append(self.genCard(item))
				typelist.append(6)
		#flight
		if l_type == 7 or l_n == 0:
			straights = self.findLargerStraight(triple, l_prior, l_n // 3, 2)
			for item in straights:
				result.append(self.genCard(item))
				typelist.append(7)
		#flight+wings
		if l_type == 8 or l_n == 0:
			if l_n == 0:
				dim = [1, 2]
				l_limit = 0
			else:
				if l_n % 4 == 0:
					dim = [1]
					l_limit = l_n // 4
				else:
					dim = [2]
					l_limit = l_n // 5
			straights = self.findLargerStraight(triple, l_prior, l_limit, 2)
			for item in straights:
				for (i, j) in item:
					handCard[i] -= 3
				for d in dim:
					card = self.findAllCombination(handCard, d, len(item))
					for c in card:
						result.append(self.genCard(item + c))
						typelist.append(8)
				for (i, j) in item:
					handCard[i] += 3

		#bomb+X+X
		if l_type == 9 or l_n == 0:
			if l_n == 0:
				dim = [1, 2]
			else:
				dim = [(l_n - 4) // 2]
			for i in range(2, 15):
				if handCard[i] == 4 and self.prior[i] > l_prior:
					for j in range(2, 15):
						for k in range(2, 15):
							if i == j or i == k:
								continue
							for d in dim:
								if (j == k and handCard[j] > d * 2) or (j != k and handCard[j] >= d and handCard[k] >= d):
									result.append(self.genCard([(i, 4), (j, d), (k, d)]))
									typelist.append(9)

		return result