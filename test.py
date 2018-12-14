
import math


def docross(lives, x, y,index):
    child1 = getChild(1, lives, x, y,index)
    child2 = getChild(2, lives, x, y,index)
    print(index,":",child1,distance(child1))
    print(index,":",child2,distance(child2))

def getChild(flag, lives, x, y,index):
    newGene = []
    px = lives[x].copy()
    py = lives[y].copy()
    c = px[index]
    newGene.append(c)
    index1, index2 = -1, -1
    dx, dy = -1, -1
    while len(px) > 1:
        for p in px:
            if p == c:
                index1 = px.index(p)
                break
        for p in py:
            if p == c:
                index2 = py.index(p)
                break
        if flag == 1:
            if index1 > 0:
                dx = px[index1 - 1]
            else:
                dx = px[len(px) - 1]
            if index2 > 0:
                dy = py[index2 - 1]
            else:
                dy = py[len(px) - 1]
        elif flag == 2:
            if index1 < len(px) - 1:
                dx = px[index1 + 1]
            else:
                dx = px[0]
            if index2 < len(px) - 1:
                dy = py[index2 + 1]
            else:
                dy = py[0]
        px.remove(c)
        py.remove(c)
        if dis[c][dx] < dis[c][dy]:
            c = dx
        else:
            c = dy
        newGene.append(c)
    return newGene


def distance(order):
    distance = 0.0
    for i in range(-1, len(order) - 1):
        index1, index2 = order[i], order[i + 1]
        distance += dis[index1][index2]
    return distance


citys=[[0,0],[3,0],[3,4],[7,3],[9,1],[]]
city_num=5
dis = [[0 for x in range(city_num)] for y in range(city_num)]
for i in range(city_num):
    for j in range(city_num):
        dis[i][j] = math.sqrt((citys[i][0] -citys[j][0]) ** 2 + (citys[i][1] - citys[j][1]) ** 2)




lives=[[0,1,4,2,3],[2,1,3,4,0]]
# lives=[[1, 0, 3, 2, 4],[1, 3, 4, 2, 0]]
print(dis)

print(distance(lives[0]))
print(distance(lives[1]))

docross(lives,0,1,0)
docross(lives,0,1,1)
docross(lives,0,1,2)
docross(lives,0,1,3)
docross(lives,0,1,4)