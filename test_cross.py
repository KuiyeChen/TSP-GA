import random
parent2=[0,1,3,2]
parent1=[2,3,1,0]
for i in range(100):
    index1 = random.randint(0, 3)
    index2 = random.randint(index1, 3)
    tempGene = parent2[index1:index2]   # 交叉的基因片段
    newGene = []
    p1len = 0
    for g in parent1:
          if p1len == index1:
                newGene.extend(tempGene)     # 插入基因片段
                p1len += 1
          if g not in tempGene:
                newGene.append(g)
                p1len += 1
    if(tempGene==[1,3]):
        print(newGene)