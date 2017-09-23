from __future__ import print_function
import copy

def end_game(game_state):
    sum0 = 0
    sum1 = 0
    sum2 = 0
    for i in range(0,15):
        sum0 += game_state[4*i+1]
        sum1 += game_state[4*i+2]
        sum2 += game_state[4*i+3]
    if(sum0 == 20 or sum1 == 17 or sum2 == 17):
        return True
    else:
        return False

def update_game(game_state,move, turn, card_on_table, allmessage):
    if(sum(move) != 0):
        card_on_table = copy.deepcopy(move)
        card_on_table.append(turn)

        if(turn == 1):
            for i in range(0,15):
                game_state[4*i+2] += move[i]
                allmessage[3*i+1] -= move[i]
        elif(turn == 2):
            for i in range(0,15):
                game_state[4*i+3] += move[i]
                allmessage[3*i+2] -= move[i]
        else:
            for i in range(0,15):
                game_state[4*i] -= move[i]
                game_state[4*i+1] += move[i]
                allmessage[3*i] -= move[i]

    return allmessage, card_on_table, game_state

#game_state = [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 4, 0, 0, 0]
#card_on_table = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#move = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#turn = 0
#update_game(game_state,move,turn,card_on_table)