# -*- coding: utf-8 -*-
# Author: Zhao Zhiheng
# Game engine of Doudizhu
# Card: Array[15]
# Spade: 1; Heart: 2; Dianmond: 4; Clubs: 8;

from pylib.rules import Rule
import copy
from random import shuffle
import pickle

class Game(object):

	def __init__(self, gameinfo = None):
		if gameinfo != None:
			self.gameinfo = copy.deepcopy(gameinfo)
			self.rule_app = Rule()
			return
		self.initCard = [(0, 1), (1, 1)]
		for i in range(2, 15):
			self.initCard += [(i, 1), (i, 2), (i, 4), (i, 8)]

		empty = [0] * 15
		#0,1,2:handCard 3:remainCard
		self.gameinfo = {}
		self.gameinfo['turn'] = -1
		self.gameinfo['last'] = -1
		self.gameinfo['landlord'] = -1
		self.gameinfo['handCard'] = [[0] * 15, [0] * 15, [0] * 15]
		self.gameinfo['handRemain'] = [0, 0, 0]
		self.gameinfo['lastCard'] = [0] * 15
		self.gameinfo['remainCard'] = [0] * 15
		self.gameinfo['winner'] = [False, False, False]
		self.rule_app = Rule()

	def convertCard(self, rawCard):
		result = [0] * 15
		for (i, t) in rawCard:
			result[i] += t
		return result

	def convert2Rule(self, card):
		result = [0] * 15
		bak = copy.copy(card)
		for i in range(15):
			for j in [8, 4, 2, 1]:
				if bak[i] >= j:
					result[i] += 1
					bak[i] -= j
		return result

	def printCard(self, card):
		card0 = copy.copy(card)
		symbol = 'Zz2AKQJ09876543'
		result = ''
		for i in range(15):
			for j in [8, 4, 2, 1]:
				if card0[i] >= j:
					result += symbol[i]
					card0[i] -= j
		return result

	def saveGame(self, filename):
		with open(filename, 'wb') as f:
			pickle.dump(self.gameinfo, f)

	def loadGame(self, filename):
		with open(filename, 'rb') as f:
			self.gameinfo = pickle.load(f)

	#Return: (card0, card1, card2, remain)
	def generateGame(self):
		shuffle(self.initCard)
		card  = copy.copy(self.initCard)
		#shuffle(card)
		card0 = self.convertCard(card[0:17])
		card1 = self.convertCard(card[17:34])
		card2 = self.convertCard(card[34:51])
		remain = self.convertCard(card[51:54])
		return (card0, card1, card2, remain)

	def startNewGame(self):
		self.gameinfo['turn'] = -1
		(card0, card1, card2, remain) = self.generateGame()
		self.gameinfo['handCard'] = [card0, card1, card2]
		self.gameinfo['handRemain'] = [17, 17, 17]
		self.gameinfo['remainCard'] = remain
		self.gameinfo['lastCard'] = [0] * 15
		self.gameinfo['winner'] = [False, False, False]

	def selectLandlord(self, id):
		if self.gameinfo['turn'] != -1:
			return
		for i in range(15):
			self.gameinfo['handCard'][id][i] += self.gameinfo['remainCard'][i]
		self.gameinfo['turn'] = id
		self.gameinfo['landlord'] = id
		self.gameinfo['handRemain'][id] = 20

	def play(self, id, card):
		if id != self.gameinfo['turn']:
			return False
		couldPass = True
		if id == self.gameinfo['last']:
			#self.gameinfo['lastCard'] = [0] * 15
			couldPass = False
		if card == [0] * 15:
			if couldPass:
				self.gameinfo['turn'] = (self.gameinfo['turn'] + 1) % 3
				if (self.gameinfo['turn'] == self.gameinfo['last']):
					self.gameinfo['lastCard'] = [0] * 15
				return True
			else:
				return False

		handCard = self.gameinfo['handCard'][id]
		for i in range(15):
			if handCard[i] != handCard[i] | card[i]:
				return False
		curCard = self.convert2Rule(card)
		lastCard = self.convert2Rule(self.gameinfo['lastCard'])
		if self.rule_app.judge(curCard, lastCard):
			for i in range(15):
				handCard[i] ^= card[i]
				self.gameinfo['lastCard'][i] = card[i]
			self.gameinfo['handRemain'][id] -= sum(curCard)
			self.gameinfo['last'] = id
			self.gameinfo['turn'] = (self.gameinfo['turn'] + 1) % 3
			if handCard == [0] * 15:
				self.endGame(id)
			return True
		return False

	def endGame(self, id):
		if self.gameinfo['landlord'] == id:
			landlordWin = True
		else:
			landlordWin = False

		for i in range(3):
			if self.gameinfo['landlord'] == i:
				self.gameinfo['winner'][i] = landlordWin
			else:
				self.gameinfo['winner'][i] = landlordWin ^ True

		self.gameinfo['turn'] = -1

