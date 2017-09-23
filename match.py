from PIL import Image
from posdef import *


def isSameColor(sourceColor, targetColor):
    if targetColor[3] == 0:
        return True
    if abs(sourceColor[0] - targetColor[0]) + abs(sourceColor[1] - targetColor[1]) + abs(
                    sourceColor[2] - targetColor[2]) < 50:
        return True
    else:
        return False


def match(sourceData, sourceSize, targetImg, rect=None, threshold=1):
    sourceW, sourceH = sourceSize
    targetW, targetH = targetImg.size

    if rect == None:
        rect = (0, 0, sourceW, sourceH)

    # sourceData = list(sourceImg.getdata())
    targetData = list(targetImg.getdata())

    pointList = []
    for i in range(targetW):
        for j in range(targetH):
            if targetData[j * targetW + i][3] != 0:
                pointList.append((i, j))
    result = []
    for i in range(rect[0], rect[2] - targetW):
        for j in range(rect[1], rect[3] - targetH):
            count = 0
            for (x, y) in pointList:
                if count >= threshold:
                    break
                if isSameColor(sourceData[(j + y) * sourceW + (i + x)], targetData[y * targetW + x]) == False:
                    count += 1
            if count < threshold:
                result.append((i, j))

    return result
