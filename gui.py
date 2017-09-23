
background_image_path = './image/background.png'
poker_image_path = './image/Poker.png'
joker_image_path = './image/Joker.png'
back_image_path = './image/back.png'

card_wh = (135, 180)
back_pos = (34, 35)
joker_pos = (60, 51)
joker_gap = (38, 0)
poker_pos = (34, 46)
poker_gap = (35, 47)

scale_size = (90, 120)
card_gap = 20
card_pos = [(60, 80), (60, 250), (60, 440)]
play_pos = (550, 250)

button_list = ['start', 'save', 'load', 'open', 'dark', 'exit', 'play', 'pass']

button_info = {} #(posX, posY, width, height, text)
button_info['start'] = (500, 20, 80, 40, 'Start')
button_info['save'] = (600, 20, 80, 40, 'Save')
button_info['load'] = (700, 20, 80, 40, 'Load')
button_info['open'] = (800, 20, 80, 40, 'Open')
button_info['dark'] = (800, 20, 80, 40, 'Dark')
button_info['exit'] = (900, 20, 80, 40, 'Exit')

button_info['play'] = (550, 100, 80, 40, 'Play')
button_info['pass'] = (550, 140, 80, 40, 'Pass')

button_status = {} #0 enabled 1 highlight 2 disabled
button_status['start'] = 0
button_status['save'] = 0
button_status['load'] = 0
button_status['open'] = 0
button_status['dark'] = 2
button_status['exit'] = 0

button_status['play'] = 2
button_status['pass'] = 2


import pygame
import sys
import copy
import time
sys.path.append('./pylib')
sys.path.append('./train')

from pygame.locals import *
from sys import exit
from pylib.game import Game
#import ai as aiApp
from mytest import model_getSingleMove2
from mytest import createNetwork
from mytest import enable
import experience as ai2App
import card as cardApp

pygame.init()
clock = pygame.time.Clock()

#init
def calcRect(initPos, gap, pos):
	global card_wh
	(w, h) = card_wh
	(x, y) = initPos
	(dx, dy) = gap
	(i, j) = pos
	nx = x + i * (w + dx)
	ny = y + j * (h + dy)
	return ((nx, ny), (w, h))

screen = pygame.display.set_mode((1056, 660), 0, 32)
pygame.display.set_caption("Doudizhu")

background = pygame.image.load(background_image_path).convert()
back_image = pygame.image.load(back_image_path).convert_alpha()
poker_image = pygame.image.load(poker_image_path).convert_alpha()
joker_image = pygame.image.load(joker_image_path).convert_alpha()

image = {}

image['b'] = back_image.subsurface(calcRect(back_pos, (0, 0), (0, 0)))
image['Z'] = joker_image.subsurface(calcRect(joker_pos, joker_gap, (0, 0)))
image['z'] = joker_image.subsurface(calcRect(joker_pos, joker_gap, (1, 0)))

symbol = 'A234567890JQK'
color = 'SHDC'

for i in range(13):
	for j in range(4):
		image[symbol[i] + color[j]] = poker_image.subsurface(calcRect(poker_pos, poker_gap, (i, j)))

for (i, j) in image.items():
	image[i] = pygame.transform.smoothscale(j, scale_size)

button_font = pygame.font.SysFont('ubuntu', 32)
id_font = pygame.font.SysFont('ubuntu', 32)



#Game info
app = Game()
AI0 = 'model/test0'
AI1 = 'ai2'
AI2 = 'ai2'

selectedCard = [False] * 20
AIController = [AI0, AI1, AI2]

best_name = 'Qmodel_best'
sess = createNetwork(1517,200,474,100,30,10)
sess.load_weights(best_name)

def processPlayOrPass(oper):
	global app, selectedCard
	card = [0] * 15
	if oper == 'play':
		tmp = copy.copy(app.gameinfo['handCard'][0])
		count = 0
		for i in range(15):
			for j in [3, 2, 1, 0]:
				if tmp[i] >= 2 ** j:
					if selectedCard[count] == True:
						card[i] += 2 ** j
					tmp[i] -= 2 ** j
					count += 1
		if sum(card) == 0:
			return 

	if app.play(0, card) == True:
		selectedCard = [False] * 20
		return


def displayButton():
	global button_list, button_info, button_status, button_font, screen
	for name in button_list:
		if button_status[name] == 2:
			continue
		(x, y, w, h, t) = button_info[name]
		if button_status[name] == 1:
			color = (50, 50, 50)
		else:
			color = (200, 200, 200)
		button_surface = button_font.render(t, True, color)
		screen.blit(button_surface, (x, y))

def displayId(ids, turn, winner):
	global card_pos
	for i in range(3):
		(x, y) = card_pos[i]
		x -= 30
		if winner[i] == True:
			id_surface = button_font.render(ids[i], True, (0, 200, 0))
		elif turn == i:
			id_surface = button_font.render(ids[i], True, (200, 0, 0))
		else:
			id_surface = button_font.render(ids[i], True, (200, 200, 200))
		screen.blit(id_surface, (x, y))


def displayCard(card, pos, selected):
	global screen
	count = 0
	card0 = copy.copy(card)
	symbol = 'Zz2AKQJ09876543'
	color = 'SHDC'
	(x, y) = pos
	for i in range(15):
		for j in [3, 2, 1, 0]:
			if card0[i] >= 2 ** j:
				if i < 2:
					tag = symbol[i]
				else:
					tag = symbol[i] + color[j]
				if selected[count] == True:
					screen.blit(image[tag], (x, y - 10))
				else:
					screen.blit(image[tag], (x, y))
				x += card_gap
				card0[i] -= 2 ** j
				count += 1

def displayUnknown(n, pos):
	global screen
	(x, y) = pos
	for i in range(n):
		screen.blit(image['b'], (x, y))
		x += card_gap

def processClickOnCard(pos, n):
	global scale_size, card_gap, card_pos, selectedCard
	(x, y) = pos
	(cx, cy) = card_pos[0]
	(lx, ly) = scale_size
	if x < cx or x > cx + (n - 1) * card_gap + lx:
		return 
	pos = (x - cx) // card_gap
	if pos >= n:
		pos = n - 1
	if selectedCard[pos] == True:
		cy -= 10
	if y >= cy and y <= cy + ly:
		selectedCard[pos] ^= True

def processClickOnButton(pos):
	global button_list, button_info, button_status, app, selectedCard
	(mx, my) = pos
	for name in button_list:
		if button_status[name] == 2:
			continue
		(x, y, w, h, t) = button_info[name]
		if mx >= x and mx < x + w and my >= y and my < y + h:
			if name == 'start':
				app.startNewGame()
				app.selectLandlord(0)
				selectedCard = [False] * 20
			elif name == 'open':
				button_status['open'] = 2
				button_status['dark'] = 0
			elif name == 'dark':
				button_status['dark'] = 2
				button_status['open'] = 0
			elif name == 'exit':
				sys.exit()
			elif name == 'play' or name == 'pass':
				processPlayOrPass(name)
			break

def processClick(pos):
	global app
	#card
	n = app.gameinfo['handRemain'][0]
	processClickOnCard(pos, n)

	#button
	processClickOnButton(pos)

def processMove(pos):
	global button_list, button_info, button_status
	(mx, my) = pos
	for name in button_list:
		if button_status[name] == 2:
			continue
		(x, y, w, h, t) = button_info[name]
		if mx >= x and mx < x + w and my >= y and my < y + h:
			button_status[name] = 1
		else:
			button_status[name] = 0

count = 0
memory_game_state = []
start_allmessage = [0] * 45
start = 1
for i in range(0, 15):
	start_allmessage[3*i] = app.gameinfo['handCard'][0][i]
	start_allmessage[3*i+1] = app.gameinfo['handCard'][1][i]
	start_allmessage[3*i+2] = app.gameinfo['handCard'][2][i]
while True:
	#ai
	curId = app.gameinfo['turn']
	if curId >= 0 and AIController[curId] != None:
		time.sleep(2)
		game = copy.deepcopy(app.gameinfo)
		for i in range(3):
			game['handCard'][i] = cardApp.convertF2C(game['handCard'][i])
		game['lastCard'] = cardApp.convertF2C(game['lastCard'])
		game['remainCard'] = cardApp.convertF2C(game['remainCard'])
		if start == 1:
			for i in range(0, 15):
				start_allmessage[3 * i] = game['handCard'][0][i]
				start_allmessage[3 * i + 1] = game['handCard'][1][i]
				start_allmessage[3 * i + 2] = game['handCard'][2][i]
			start = 0
		if AIController[curId] == 'ai2':
			card = ai2App.getNextMove(game, curId)
		else:
			#print(game)
			#print(curId)
			#print(AIController[curId])
			#card = aiApp.getNextMove(game, curId, AIController[curId], True)
			gameinfo = [0]*60
			for i in range(0,15):
				gameinfo[4*i] = game['handCard'][0][i]
				gameinfo[4*i+1] = start_allmessage[3*i]-game['handCard'][0][i]
				gameinfo[4*i+2] = start_allmessage[3*i+1]-game['handCard'][1][i]
				gameinfo[4*i+3] = start_allmessage[3*i+2]-game['handCard'][2][i]
			if(game['last'] == -1):
				game['last'] = 0
			game['gameinfo'] = copy.deepcopy(gameinfo)
			enableCard = enable(gameinfo, game['lastCard']+[game['last']])
			memory_game_state.append(copy.deepcopy(game))
			card = model_getSingleMove2(sess, memory_game_state, [1517,200,474,100,30,10], count, enableCard)
			count+=1
		#print(card)
		card = cardApp.convertC2F(card, app.gameinfo['handCard'][curId])
		if app.play(curId, card) == True:
			print('Success', curId)

	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		elif event.type == MOUSEBUTTONDOWN:
			processClick(event.pos)
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE or event.key == 81 or event.key == 113: #Q
				sys.exit()

	screen.blit(background, (0, 0))

	#button
	button_status['play'] = 2
	button_status['pass'] = 2
	if app.gameinfo['turn'] == 0:
		button_status['play'] = 0
		if app.gameinfo['last'] != 0:
			button_status['pass'] = 0
	processMove(pygame.mouse.get_pos())
	displayButton()

	displayId(['L', 'F', 'F'], app.gameinfo['turn'], app.gameinfo['winner'])
	displayCard(app.gameinfo['handCard'][0], card_pos[0], selectedCard)
	if button_status['dark'] != 2:
		displayCard(app.gameinfo['handCard'][1], card_pos[1], [False]*20)
		displayCard(app.gameinfo['handCard'][2], card_pos[2], [False]*20)
	else:
		displayUnknown(app.gameinfo['handRemain'][1], card_pos[1])
		displayUnknown(app.gameinfo['handRemain'][2], card_pos[2])
	displayCard(app.gameinfo['lastCard'], play_pos, [False]*20)
	pygame.display.update()
