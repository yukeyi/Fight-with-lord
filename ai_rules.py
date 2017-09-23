from __future__ import print_function
import experience as ex
import game as gameApp

def ai_getSingleMove(game_state, id, card_on_table):
    zhiheng_state = convert(game_state, id, card_on_table)
    return ex.getNextMove(zhiheng_state, id)

#allmessage = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 2, 1, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 1, 0, 0]
#card0 = [0]*15
#card1 = [0]*15
#card2 = [0]*15
#for i in range(0,15):
#    card0[i] = allmessage[3*i]
#    card1[i] = allmessage[3 * i+1]
#    card2[i] = allmessage[3 * i+2]
#card_on_table = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
#card = ai_getSingleMove(allmessage,1,card_on_table)
#print(card)

def convert(game_state, id, card_on_table):
    gameinfo = gameApp.newGame()
    gameinfo['last'] = card_on_table[15]

    gameinfo['handCard'][1] = []
    gameinfo['handCard'][2] = []
    gameinfo['handCard'][0] = []

    for i in range(0,15):
        gameinfo['handCard'][0].append(game_state[3*i])
        gameinfo['handCard'][1].append(game_state[3*i+1])
        gameinfo['handCard'][2].append(game_state[3*i+2])

    for i in range(3):
        gameinfo['handRemain'][i] = sum(gameinfo['handCard'][i])

    if(id == card_on_table[15]):
        gameinfo['lastCard'] = [0]*15
    else:
        gameinfo['lastCard'] = card_on_table[0:15]
    return gameinfo