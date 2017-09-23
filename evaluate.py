from __future__ import print_function
from colorama import Fore
from testset import testset
from gamestate_maintain import update_game, end_game
from ai_rules import ai_getSingleMove
from enable import enable
from singlemove import model_getSingleMove2
import copy


# models是测试的三个模型， num是测试局数， 返回胜局数
def evaluate(models, num, model_size):

    remainsum = 0
    wingame = 0
    evalset = copy.deepcopy(testset[0:num])

    for finishgame in range(0,num):
        #print("finish %d, win %d",finishgame,wingame)
        allmessage = evalset[finishgame]
        turn = 0
        count = 0
        game_state = [0]*60
        for i in range(0,15):
            game_state[4*i] = allmessage[3*i]
        card_on_table = [0] * 16

        memory_game_state = []
        round = {}
        round['handCard'] = [[0] * 15, [0] * 15, [0] * 15]
        for i in range(0, 15):
            round['handCard'][0][i] = allmessage[3 * i]
            round['handCard'][1][i] = allmessage[3 * i + 1]
            round['handCard'][2][i] = allmessage[3 * i + 2]
        round['gameinfo'] = copy.deepcopy(game_state)
        round['last'] = card_on_table[15]
        round['lastCard'] = copy.deepcopy(card_on_table[0:15])
        memory_game_state.append(copy.deepcopy(round))

        while(1):
            if(end_game(game_state)):
                if(turn == 1):
                    wingame += 1
                for i in range(0,15):
                    remainsum += allmessage[3 * i]
                break
            if(turn == 1):
                move = ai_getSingleMove(allmessage,1,card_on_table)
                allmessage, card_on_table, game_state = update_game(game_state,move, 1, card_on_table, allmessage)
            elif(turn == 2):
                move = ai_getSingleMove(allmessage,2,card_on_table)
                allmessage, card_on_table, game_state = update_game(game_state, move, 2, card_on_table, allmessage)
                round = {}
                round['handCard'] = [[0] * 15, [0] * 15, [0] * 15]
                for i in range(0, 15):
                    round['handCard'][0][i] = allmessage[3 * i]
                    round['handCard'][1][i] = allmessage[3 * i + 1]
                    round['handCard'][2][i] = allmessage[3 * i + 2]
                round['gameinfo'] = copy.deepcopy(game_state)
                round['last'] = card_on_table[15]
                round['lastCard'] = copy.deepcopy(card_on_table[0:15])
                memory_game_state.append(copy.deepcopy(round))
            else:
                enablecard = enable(game_state,card_on_table)
                move = model_getSingleMove2(models[0], memory_game_state, model_size, count, enablecard)
                memory_game_state[-1]['choose'] = copy.deepcopy(move)
                allmessage, card_on_table, game_state = update_game(game_state, move, 0, card_on_table, allmessage)
                count+=1
            turn = (turn+1) % 3
    print (Fore.RED + 'sum of cards remain = %d , wingame_rate = (%d/%d)' % (remainsum, wingame, finishgame+1))
    return wingame