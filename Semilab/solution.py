import re
from enum import Enum

class HeadType(Enum):
    A = 0
    B = 1
    AB = 2

samplemap = dict()

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
    if x not in samplemap:
        samplemap[x] = dict()
    if twoHeads:
        samplemap[x][y] = HeadType.AB
    elif firstHead == 'A':
        samplemap[x][y] = HeadType.A
    else:
        samplemap[x][y] = HeadType.B

f.close()

#w = open("out.txt", "w")
prevx = 0
prevy = 0
currx = 0
curry = 0
checkedx = []
checkedy = []

for key1, item1 in samplemap.items():
    for key2, item2 in item1.items():
        currx = key1
        curry = key2
        break

cost = 0
curreHead = HeadType.A

strout = ''

finished = False
while not finished:
    currpos = samplemap[currx][curry]
    cost += abs(currx - prevx)
    cost += abs(curry - prevy)
    if currpos == HeadType.A:
        if curreHead == HeadType.B:
            cost += 60
        curreHead = HeadType.A
        strout += str(currx) + ';' + str(curry) + ': A\n'
    elif currpos == HeadType.B:
        if curreHead == HeadType.A:
            cost += 60
        curreHead = HeadType.B
        strout += str(currx) + ';' + str(curry) + ': B\n'
    elif currpos == HeadType.AB:
        cost += 60
        if curreHead == HeadType.A:
            curreHead = HeadType.B
            strout += str(currx) + ';' + str(curry) + ': A\n'
            strout += str(currx) + ';' + str(curry) + ': B\n'
        elif curreHead == HeadType.B:
            curreHead = HeadType.A
            strout += str(currx) + ';' + str(curry) + ': B\n'
            strout += str(currx) + ';' + str(curry) + ': A\n'
    
    checkedx.append(currx)
    checkedy.append(curry)
    used = False
    for key1, item1 in samplemap.items():
        for key2, item2 in item1.items():
            used = False
            for i in range(len(checkedx)):
                if checkedx[i] == key1 and checkedy[i] == key2:
                    used = True
                    break
            if not used:
                prevx = currx
                prevy = curry
                currx = key1
                curry = key2
                break
        if not used:
            break
    
    if used:
        break

w = open("out.txt", "w")
w.write(strout)
w.close()