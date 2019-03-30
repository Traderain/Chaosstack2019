import re
import collections
from enum import Enum
from random import randint

class HeadType(Enum):
    A = 0
    B = 1
    AB = 2

def calculatecost(samplemap):
    cost = 0

    curreHead = HeadType.A
    prevx = 0
    prevy = 0
    for i in range(len(samplemap)):
        currx = samplemap[i][0]
        curry = samplemap[i][1]
        currpos = samplemap[i][2]
        cost += abs(currx - prevx)
        cost += abs(curry - prevy)
        if currpos == HeadType.A:
            if curreHead == HeadType.B:
                cost += 60
            curreHead = HeadType.A
            cost += 2
        elif currpos == HeadType.B:
            if curreHead == HeadType.A:
                cost += 60
            curreHead = HeadType.B
            cost += 3
        elif currpos == HeadType.AB:
            cost += 60
            if curreHead == HeadType.A:
                curreHead = HeadType.B
            elif curreHead == HeadType.B:
                curreHead = HeadType.A
        prevx = currx
        prevy = curry
    return cost

def swapTwoItems(currMovingIdx, samplemap):
    if currMovingIdx + 1 < len(samplemap):
        samplemap[currMovingIdx], samplemap[currMovingIdx + 1] = samplemap[currMovingIdx + 1], samplemap[currMovingIdx]
        return True
    else:
        return False

def swapTwoItemsIdx(currMovingIdx, toMovingIdx, samplemap):
    if currMovingIdx < len(samplemap) and toMovingIdx < len(samplemap):
        samplemap[currMovingIdx], samplemap[toMovingIdx] = samplemap[toMovingIdx], samplemap[currMovingIdx]
        return True
    else:
        return False

def writeout(newsamplemap):
    curreHead = HeadType.A
    strout = ''
    for i in range(len(newsamplemap)):
        currx = newsamplemap[i][0]
        curry = newsamplemap[i][1]
        currpos = newsamplemap[i][2]
        if currpos == HeadType.A:
            curreHead = HeadType.A
            strout += str(currx) + ';' + str(curry) + ': A\n'
        elif currpos == HeadType.B:
            curreHead = HeadType.B
            strout += str(currx) + ';' + str(curry) + ': B\n'
        elif currpos == HeadType.AB:
            if curreHead == HeadType.A:
                curreHead = HeadType.B
                strout += str(currx) + ';' + str(curry) + ': A\n'
                strout += str(currx) + ';' + str(curry) + ': B\n'
            elif curreHead == HeadType.B:
                curreHead = HeadType.A
                strout += str(currx) + ';' + str(curry) + ': B\n'
                strout += str(currx) + ';' + str(curry) + ': A\n'

    w = open("out.txt", "w")
    w.write(strout)
    w.close()

samplemapread = collections.OrderedDict()

f = open("input.txt", "r")

lines = f.readlines()

for i in range(len(lines)):
    line = re.split(r";|:| |\+|\n", lines[i])
    firstHead = line[3]

    twoHeads = False
    if len(line) > 5:
        twoHeads = True

    x = int(line[0])
    y = int(line[1])
    if x not in samplemapread:
        samplemapread[x] = collections.OrderedDict()
    if twoHeads:
        samplemapread[x][y] = HeadType.AB
    elif firstHead == 'A':
        samplemapread[x][y] = HeadType.A
    else:
        samplemapread[x][y] = HeadType.B

f.close()

startingpoint = (0, 0)

samplemap = []
finished = False
while not finished:
    distances = []
    for x, item in samplemapread.items():
        for y, value in item.items():
            newx = x - startingpoint[0]
            newy = y - startingpoint[1]
            distances.append([x, y, newx*newx + newy*newy])
    
    shortest = distances[0]
    for distance in distances:
        if distance[2] < shortest[2]:
            shortest = distance
    
    x = shortest[0]
    y = shortest[1]
    startingpoint = (x, y)
    samplemap.append([x, y, samplemapread[x][y]])

    del samplemapread[x][y]
    if len(samplemapread[x]) == 0:
        del samplemapread[x]

    if len(samplemapread) == 0:
        break

startMovingIdx = 0
currMovingIdx = 0
toMovingIdx = 0
currMoving = samplemap[0]
minCost = 0
fistCost = True
finished = False
newsamplemap = None
while not finished:
    cost = calculatecost(samplemap)
    if fistCost or cost < minCost:
        fistCost = False
        minCost = cost
        newsamplemap = samplemap.copy()
        writeout(newsamplemap)

    if not swapTwoItemsIdx(toMovingIdx, currMovingIdx, samplemap):
        break
    
    currMovingIdx = randint(0, len(samplemap) - 1)
    toMovingIdx = randint(0, len(samplemap) - 1)
    if not swapTwoItemsIdx(currMovingIdx, toMovingIdx, samplemap):
        break
    #if swapTwoItems(currMovingIdx, samplemap):
    #    currMovingIdx += 1
    #else:
    #    if startMovingIdx + 1 > len(samplemap):
    #        break
    #    samplemap.insert(startMovingIdx, samplemap[currMovingIdx])
    #    samplemap.pop()
    #    startMovingIdx += 1
    #    currMovingIdx = startMovingIdx
