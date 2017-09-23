import copy
import random

def convertCard(rawCard):
	result = [0] * 15
	for i in rawCard:
		result[i] += 1
	return result

def evaluateCard(card):
	score =  card[0] * 5 + card[1] * 4 + card[2] * 3 + card[3] * 2
	for i in range(15):
		if card[i] == 3:
			score += 2
		if card[i] == 4:
			score += 5
	return score

def newGame():
	initCard = [0, 1]
	for i in range(2, 15):
		initCard += [i] * 4
	random.shuffle(initCard)

	gameinfo = {}
	gameinfo['turn'] = 0
	gameinfo['last'] = 0
	gameinfo['landlord'] = 0
	gameinfo['handCard'] = [None, None, None]
	gameinfo['handCard'][0] = convertCard(initCard[0:17])
	gameinfo['handCard'][1] = convertCard(initCard[17:34])
	gameinfo['handCard'][2] = convertCard(initCard[34:51])

	gameinfo['history'] = [[], [], []]
	gameinfo['historyType'] = [[], [], []]

	score = [0, 0, 0]
	for i in range(3):
		score[i] = evaluateCard(gameinfo['handCard'][i])
	if score[1] > score[0] and score[1] > score[2]:
		tmp = copy.deepcopy(gameinfo['handCard'][0])
		gameinfo['handCard'][0] = copy.deepcopy(gameinfo['handCard'][1])
		gameinfo['handCard'][1] = copy.deepcopy(tmp)
	if score[2] > score[0] and score[2] > score[1]:
		tmp = copy.deepcopy(gameinfo['handCard'][0])
		gameinfo['handCard'][0] = copy.deepcopy(gameinfo['handCard'][2])
		gameinfo['handCard'][2] = copy.deepcopy(tmp)

	gameinfo['handRemain'] = [20, 17, 17]
	gameinfo['lastCard'] = [0] * 15
	gameinfo['remainCard'] = convertCard(initCard[51:54])
	for i in range(15):
		gameinfo['handCard'][0][i] += gameinfo['remainCard'][i]

	return gameinfo

#Determine the type of cards
#Example
#Input:[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
#Output:(0, 0)
def cardType(card):
	n = 0
	m = [0] * 5
	p = [15] * 5
	for i in range(15):
		c = card[i]
		n += c
		m[c] += 1
		if i < p[c]:
			p[c] = i
	#Rocket
	if card[0] == 1 and card[1] == 1 and n == 2:
		return (0, p[1])
	#Bomb
	if m[4] == 1 and n == 4:
		return (1, p[4])
	#single
	if m[1] == 1 and n == 1:
		return (2, p[1])
	#double
	if m[2] == 1 and n == 2:
		return (3, p[2])
	#triple+X
	if m[3] == 1 and n >= 3 and n <= 5 :
		if (m[1] == 0 or m[2] == 0) and m[1] + m[2] * 2 + 3 == n:
			return (4, p[3])
	#straight
	if m[1] == n and m[1] >= 5 and p[1] >= 3:
		a = p[1]
		b = a + n
		if sum(card[a:b]) == n:
			return (5, p[1])
	#double
	if m[2] * 2 == n and m[2] >= 3 and p[2] >= 3:
		a = p[2]
		b = a + n // 2
		if sum(card[a:b]) == n:
			return (6, p[2])
	#flight
	if m[3] * 3 == n and m[3] >= 2 and p[3] >= 3:
		a = p[3]
		b = a + n // 3
		if sum(card[a:b]) == n:
			return (7, p[3])
	#bomb+X+X
	if m[4] == 1 and m[3] == 0:
		if (m[1] == 0 and m[2] == 2) or (m[1] == 0 and m[2] == 1) or (m[1] == 2 and m[2] == 0):
			return (9, p[4])
	if m[4] == 2 and n == 8:
		return (9, p[4])
	return (-1, 15)

#Determine whether the card is legal
#Example
#Input:[0,0,0,0,0,0,0,0,0,1,1,1,1,1,0], [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1]
#Output:True
def judge(curCard, lastCard):
	(c_type, c_prior) = cardType(curCard)
	(l_type, l_prior) = cardType(lastCard)
	c_n = sum(curCard)
	l_n = sum(lastCard)
	if c_type == -1:
		return False
	if l_n == 0:
		return True
	if c_type == 0:
		return True
	if c_type == 1 and l_type != 0 and l_type != 1:
		return True
	if c_type == l_type and c_n == l_n and c_prior < l_prior:
		return True
	return False

#Convert the card representation from tuples to array
#Example
#Input:[(2, 3),(5, 1)]
#Output:[0,0,3,0,0,1,0,0,0,0,0,0,0,0,0]
def genCard(cardTuples):
	t = [0] * 15
	for (card, n) in cardTuples:
		t[card] += n
	return t

#Find all legal straights
def findStraight(card):
	dims = [1, 2, 3]
	straights = [[], [], [], []]
	cur = [[], [], [], []]
	for i in range(3, 15):
		for d in dims:
			if card[i] >= d:
				cur[d].append((i, d))
			if card[i] < d or i == 14:
				if cur[d] != []:
					straights[d].append(cur[d])
					cur[d] = []
	return straights

#Find all legal straights which are larger than last straight(may be None)
def findLargerStraight(straights, p_limit, l_limit, minL):
	result = []
	for item in straights:
		l  = len(item)
		if l < l_limit or l < minL:
			continue
		for i in range(l):
			if item[i][0] >= p_limit:
				continue
			for j in range(minL, l - i + 1):
				if l_limit > 0 and j != l_limit:
					continue
				result.append(item[i:(i + j)])
	return result

#Generate all legal cards for specific situation(gameinfo)
def generate(gameinfo):
	lastCard = gameinfo['lastCard']
	id = gameinfo['turn']
	handCard = gameinfo['handCard'][id]
	(l_type, l_prior) = cardType(lastCard)
	l_n = sum(lastCard)
	result = []
	typelist = []
	if lastCard != [0] * 15:
		result.append([0] * 15)
	if l_type == 0:
		return result
	#Rocket
	if handCard[0] == 1 and handCard[1] == 1:
		result.append(genCard([(0, 1), (1, 1)]))
		typelist.append(0)
	#Bomb
	for i in range(2, 15):
		if handCard[i] == 4 and (l_type != 1 or i < l_prior):
			result.append(genCard([(i, 4)]))
			typelist.append(1)

	#Normal
	for i in range(15):
		#single
		if l_type == 2 or l_n == 0:
			if handCard[i] >= 1 and i < l_prior:
				result.append(genCard([(i, 1)]))
				typelist.append(2)
		#double
		if l_type == 3 or l_n == 0:
			if handCard[i] >= 2 and i < l_prior:
				result.append(genCard([(i, 2)]))
				typelist.append(3)

	#triple+X
	if l_type == 4 or l_n == 0:
		if l_n == 0:
			dim = [0, 1, 2]
		else:
			dim = [l_n - 3]
		for i in range(2, 15):
			if handCard[i] >= 3 and i < l_prior:
				if 0 in dim:
					result.append(genCard([(i, 3)]))
					typelist.append(4)
				for j in range(15):
					if i == j:
						continue
					for d in dim:
						if d != 0 and handCard[j] >= d:
							result.append(genCard([(i, 3), (j, d)]))
							typelist.append(4)

	(dc, single, double, triple) = findStraight(handCard)
	#straight
	if l_type == 5 or l_n == 0:
		straights = findLargerStraight(single, l_prior, l_n, 5)
		for item in straights:
			result.append(genCard(item))
			typelist.append(5)
	#straight
	if l_type == 6 or l_n == 0:
		straights = findLargerStraight(double, l_prior, l_n // 2, 3)
		for item in straights:
			result.append(genCard(item))
			typelist.append(6)	
	#straight
	if l_type == 7 or l_n == 0:
		straights = findLargerStraight(triple, l_prior, l_n // 3, 2)
		for item in straights:
			result.append(genCard(item))
			typelist.append(7)

	return result

#Simulate the play action of the game
def play(gameinfo, id, card):
	if gameinfo['turn'] < 0:
		return 
	assert gameinfo['turn'] >= 0, gameinfo['turn'] == id
	gameinfo['history'][id].append(card)
	if card == [0] * 15:
		if gameinfo['last'] == id:
			print(id, gameinfo)
		assert gameinfo['last'] != id
		gameinfo['turn'] = (gameinfo['turn'] + 1) % 3
		if gameinfo['turn'] == gameinfo['last']:
			gameinfo['lastCard'] = [0] * 15
		return
	else:
		if judge(card, gameinfo['lastCard']) == False:
			print(card)
		assert judge(card, gameinfo['lastCard'])
		gameinfo['historyType'][id].append(cardType(card))
		for i in range(15):
			assert gameinfo['handCard'][id][i] >= card[i]
			gameinfo['handCard'][id][i] -= card[i]
			gameinfo['lastCard'][i] = card[i]
		gameinfo['handRemain'][id] -= sum(card)
		assert gameinfo['handRemain'][id] >= 0
		gameinfo['last'] = id
		gameinfo['turn'] = (gameinfo['turn'] + 1) % 3
		if gameinfo['handRemain'][id] == 0:
			gameinfo['turn'] = -1

#Sample the two other players' hand card
def sampleCard(card, sum1, sum2):
	cards = []
	for i in range(15):
		cards += [i] * card[i]
	random.shuffle(cards)
	card1 = [0] * 15
	card2 = [0] * 15
	#print(sum1, sum2, cards, len(cards))
	for i in range(sum1):
		card1[cards[i]] += 1
	for i in range(sum1, sum1 + sum2):
		card2[cards[i]] += 1
	return card1, card2
'''
def printCard(card):
	card0 = copy.copy(card)
	symbol = 'Zz2AKQJ09876543'
	result = ''
	for i in range(15):
		for j in range(4):
			if card0[i] >= 1:
				result += symbol[i]
				card0[i] -= 1
	return result
g = newGame()
print(printCard(g['handCard'][0]))

c, t = generate(g, 0)

l = len(c)
for i in range(l):
	print(printCard(c[i]))
	assert t[i] == cardType(c[i])[0]
'''
