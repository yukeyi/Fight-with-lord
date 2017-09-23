from PIL import Image
from PIL import ImageGrab
import match as matchApp
import card as cardApp
import winapi as winApp
import ai as aiApp
import experience as exApp
from posdef import *
import time
import copy
import traceback

timecount = 0

model0 = aiApp.AI('model/L0/best618', [1517, 1000, 200], False, 50)
model1 = aiApp.AI('model/F1/best457', [1517, 1000, 200], False, 50)
model2 = aiApp.AI('model/F2/best443', [1517, 1000, 200], False, 50)

AI = [model0, model1, model2]

handCardImg = [0] * 15
playCardImg = [0] * 15
remainCardImg = [0] * 15

gameinfo = {}
gameinfo['turn'] = 0  # 当前轮到谁出牌（地主为0）
gameinfo['last'] = 0  # 上一个出牌的人
gameinfo['handCard'] = [None, None, None]  # 每个人的手牌（自己的手牌全纪录，另外两家的手牌都记录可能的牌总数）
gameinfo['handRemain'] = [0, 0, 0]  # 每个人的剩余牌数
gameinfo['lastCard'] = [0] * 15  # 上一个出牌人出的牌
gameinfo['remainCard'] = [0] * 15  # 三张底牌

localinfo = {}
localinfo['status'] = 0 # 0叫地主阶段 1初始化阶段 2打牌阶段 3结束统计阶段
localinfo['pos'] = -1
localinfo['win'] = 0
localinfo['error'] = 0

icon_list = ['start', 'score1', 'score2', 'score3', 'nocall', 'play', 'pass', 'passIcon', 'landlordIcon', 'noLarger']
icon = {}

offset = (0, 0)
sourceImg = None
sourceSize = (0, 0)
sourceData = []

filename = 'record_newmodel.txt'
resultname = 'result_newmodel.txt'

def loadImg():
    global handCardImg, remainCardImg, playCardImg, icon
    for i in range(15):
        handCardImg[i] = [0] * 2
        for j in range(2):
            handCardImg[i][j] = Image.open('pic/hand/{0}_{1}.png'.format(i, j))

    for i in range(15):
        remainCardImg[i] = [0] * 2
        for j in range(2):
            remainCardImg[i][j] = Image.open('pic/remain/{0}_{1}.png'.format(i, j))

    for i in range(15):
        playCardImg[i] = [0] * 2
        for j in range(2):
            playCardImg[i][j] = Image.open('pic/play/{0}_{1}.png'.format(i, j))

    for i in range(10):
        name = icon_list[i]
        icon[name] = Image.open('pic/icon/{0}.png'.format(i))


def getNextMove():
    global gameinfo
    turn = gameinfo['turn']
    info = copy.deepcopy(gameinfo)
    for i in range(3):
        if i != turn:
            info['handCard'][i] = [0] * 15
            break
    return AI[turn].getNextMove(info, turn)

def getPosition():
    global sourceData, sourceSize, icon, landlordIcon_rect
    for i in range(3):
        if len(matchApp.match(sourceData, sourceSize, icon['landlordIcon'], landlordIcon_rect[i])) >= 1:
            return i
    return -1


def getButtonPosition(name, rect=buttonIcon_rect):
    global sourceData, sourceSize, icon
    result = matchApp.match(sourceData, sourceSize, icon[name], rect)
    if len(result) >= 1:
        return result[0]
    else:
        return None


def getImage():
    global sourceImg, sourceSize, sourceData, offset
    rect = winApp.getrect()
    if rect[0] < 0 or rect == (0, 0, 0, 0):
        print('No game')
        return False

    sourceImg = ImageGrab.grab(rect)
    sourceSize = sourceImg.size
    sourceData = list(sourceImg.getdata())
    offset = (rect[0], rect[1])
    return True


# 分三个阶段
# 叫地主/不叫
# 抢地主/不抢
# 加倍/不加倍
def selectLandlord():
    global localinfo, sourceData, sourceSize, handCardImg, offset
    if localinfo['status'] != 0:
        return
    # print(getPosition())
    if getPosition() != -1:
        localinfo['status'] = 1
        return
    # 叫地主/不叫
    # winApp.mouse_click(725, 685, offset)
    handCard, _, _ = cardApp.getHandCard(sourceData, sourceSize, handCardImg)
    if exApp.getLord(handCard):
        pos = getButtonPosition('score3')
        # print(pos)
        if pos != None:
            winApp.mouse_click(pos[0], pos[1], offset)
            localinfo['status'] = 1
            return
        # 初始化新一局游戏信息，只初始化一次
    else:
        pos = getButtonPosition('nocall')
        # print(pos)
        if pos != None:
            winApp.mouse_click(pos[0], pos[1], offset)
            localinfo['status'] = 1
            return


def initGame():
    global gameinfo, localinfo, sourceData, sourceSize, handCardImg, remainCardImg, offset
    if getButtonPosition('nocall') != None:  # happens when all players choose 'nocall'
        localinfo['status'] = 0
        return
    if localinfo['status'] != 1:
        return
    pos = getPosition()  # landlord position (0: self, 1: left 2: right)
    if pos < 0:
        return

    localinfo['pos'] = pos
    localinfo['win'] = 0
    localinfo['error'] = 0
    gameinfo['turn'] = localinfo['pos']
    gameinfo['last'] = 0
    gameinfo['handRemain'] = [20, 17, 17]
    gameinfo['lastCard'] = [0] * 15
    gameinfo['remainCard'] = cardApp.getRemainCard(sourceData, sourceSize, remainCardImg)
    gameinfo['handCard'][pos], _, _ = cardApp.getHandCard(sourceData, sourceSize, handCardImg)

    tmpCard = [1] * 2 + [4] * 13
    for i in range(15):
        tmpCard[i] -= gameinfo['handCard'][pos][i]
    for i in range(3):
        if i != pos:
            gameinfo['handCard'][i] = copy.deepcopy(tmpCard)

    localinfo['status'] = 2
    # print(gameinfo)

# 出牌
def playGame():
    global gameinfo, localinfo, sourceData, sourceSize, handCardImg, remainCardImg, offset
    if localinfo['status'] != 2:
        return
    if getButtonPosition('start', startIcon_rect) != None:
        localinfo['status'] = 3
        return

    # if getButtonPosition('play') == None and getButtonPosition('pass') == None:
    if getButtonPosition('play', timer_rect) == None:
        return

    cardL = cardApp.getPlayCard(sourceData, sourceSize, playCardImg, (240, 600))
    cardR = cardApp.getPlayCard(sourceData, sourceSize, playCardImg, (600, 950))

    # time.sleep(0.5)
    '''
    if getButtonPosition('noLarger', noLarger_rect) != None:
        # passPos = getButtonPosition('pass')
        # winApp.mouse_click(passPos[0], passPos[1], offset)
        winApp.mouse_click(600, 690, offset)
        with open(filename, 'a') as myfile:
            myfile.write('gameinfo ' + str(gameinfo) + '\n')
            myfile.write('cardL ' + str(cardL) + '\n')
            myfile.write('cardR ' + str(cardR) + '\n')
            myfile.write('nextMove ' + str([0] * 15) + '\n')
        # print(gameinfo)
        # print([0] * 15)
        return
    '''
    pos = localinfo['pos']  # my id in gameinfo
    posL = (localinfo['pos'] + 2) % 3  # player on the left-hand side of me
    posR = (localinfo['pos'] + 1) % 3  # player on the right-hand side of me
    handCard, status, leftX = cardApp.getHandCard(sourceData, sourceSize, handCardImg)
    gameinfo['handCard'][pos] = handCard

    gameinfo['handRemain'][pos] = sum(handCard)
    gameinfo['handRemain'][posL] -= sum(cardL)
    gameinfo['handRemain'][posR] -= sum(cardR)

    for i in range(15):
        gameinfo['handCard'][posL][i] -= cardL[i]
        gameinfo['handCard'][posL][i] -= cardR[i]
        gameinfo['handCard'][posR][i] -= cardL[i]
        gameinfo['handCard'][posR][i] -= cardR[i]

    if cardL != [0] * 15:
        gameinfo['lastCard'] = cardL
        gameinfo['last'] = posL
    elif cardR != [0] * 15:
        gameinfo['lastCard'] = cardR
        gameinfo['last'] = posR
    else:
        gameinfo['lastCard'] = [0] * 15
        gameinfo['last'] = pos

    card = getNextMove()

    with open(filename, 'a') as myfile:
        myfile.write('gameinfo ' + str(gameinfo) + '\n')
        myfile.write('cardL ' + str(cardL) + '\n')
        myfile.write('cardR ' + str(cardR) + '\n')
        myfile.write('nextMove ' + str(card) + '\n')
    '''
    print(gameinfo)
    card = getNextMove()
    print(card)
    '''
    if card == [0] * 15:
        # passPos = getButtonPosition('pass')
        # winApp.mouse_click(passPos[0], passPos[1], offset)
        winApp.mouse_click(600, 690, offset)
        return

    l = len(status)
    tmp = [0] * l
    count = 0

    for i in range(15):
        remain = handCard[i] - card[i]
        for j in range(card[i]):
            tmp[count] = 1
            count += 1
        for j in range(remain):
            count += 1

    while status != tmp:
        # print(l, status, tmp)
        if len(status) < l:
            continue
        for i in range(l):
            if status[i] != tmp[i]:
                x = leftX + handCard_W * i + handCard_W // 2
                y = handCard_secondY + 50
                winApp.mouse_click(x, y, offset)
        time.sleep(0.5)
        getImage()
        _, status, leftX = cardApp.getHandCard(sourceData, sourceSize, handCardImg)

    # playPos = getButtonPosition('play')
    winApp.mouse_rclick(1050, 800, offset)
    if card == handCard:
        localinfo['win'] = 1
        localinfo['status'] = 3


# 游戏结束
def endGame():
    global localinfo
    if localinfo['status'] != 3:
        return
    pos = localinfo['pos']  # my id in gameinfo
    if localinfo['pos'] >= 0:
        win = localinfo['win']
        error = localinfo['error']
        t = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        with open(resultname, 'a') as resultfile:
            resultfile.write('%d %d %d %s\n' % (pos, win, error, t))
        localinfo['pos'] = -1
    pos = getButtonPosition('start', startIcon_rect)
    if pos != None:
        # winApp.mouse_click(1080, 125, offset)  # hide statistics
        # cardL = cardApp.getEndCard(sourceData, sourceSize, handCardImg, endCardL_rect)
        # cardR = cardApp.getEndCard(sourceData, sourceSize, handCardImg, endCardR_rect)
        with open(filename, 'a') as myfile:
            myfile.write('endgame\n\n')
            # myfile.write('endL' + str(cardL) + '\n')
            # myfile.write('endR' + str(cardR) + '\n' * 2)
        winApp.mouse_click(pos[0], pos[1], offset)
        localinfo['status'] = 0
        return


def mainLoop():
    # 找到窗口位置
    # 截取窗口图像
    global localinfo, timecount
    if getImage() == False:
        return
    '''
    pos = getButtonPosition('start', startIcon_rect)
    if pos != None:
        winApp.mouse_click(pos[0], pos[1], offset)
        localinfo['status'] = 0
        return
    '''
    if getButtonPosition('start', startIcon_rect) != None:
        localinfo['status'] = 3
    if localinfo['status'] == 0:
        selectLandlord()
    elif localinfo['status'] == 1:
        initGame()
    elif localinfo['status'] == 2:
        playGame()
    elif localinfo['status'] == 3:
        endGame()
    timecount += 1
    if timecount % 10 == 0:
        winApp.mouse_rclick(1050, 800, offset)


loadImg()

while True:
    try:
        mainLoop()
    except:
        localinfo['error'] = 1
        with open('error.log', 'a') as f:
            traceback.print_exc(file=f)
    time.sleep(1)