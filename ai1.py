import copy

def getNextMove(gameinfo, id):
    copy_game = copy.deepcopy(gameinfo)

    if id == 0:
        if sum(gameinfo['lastCard']) == 0:
            play_card = activePlay(copy_game, id)
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


def activePlay(gameinfo, id):
    pos_split = splitApp.get_split(gameinfo['handCard'][id], REVERSE_SPLIT)
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