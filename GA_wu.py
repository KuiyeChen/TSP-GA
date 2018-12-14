# -*- coding: utf-8 -*-

import random
from Life import Life

class GA(object):

      """遗传算法类"""
      def __init__(self, aCrossRate, aMutationRage, aLifeCount, aGeneLenght, dis,aMatchFun = lambda life : 1):
            self.croessRate = aCrossRate              #交叉概率
            self.mutationRate = aMutationRage         #变异概率
            self.lifeCount = aLifeCount               #种群数量
            self.geneLenght = aGeneLenght             #基因长度
            self.matchFun = aMatchFun                 # 适配函数
            self.lives = []                           # 种群
            self.best = None                         # 保存这一代中最好的个体
            self.dis=dis
            self.generation = 1
            self.crossCount = 0
            self.mutationCount = 0
            self.bounds = 0.0                         # 适配值之和，用于选择是计算概率

            self.initPopulation()


      def initPopulation(self):
            """初始化种群"""
            self.lives = []
            for i in range(self.lifeCount):
                  gene = [ x for x in range(self.geneLenght) ]
                  random.shuffle(gene)     #将序列的所有元素随机排序
                  self.modify_circle(gene)
                  life = Life(gene)
                  self.lives.append(life)
            self.best=self.lives[0]
            self.judge()


      def modify_circle(self,gene):
            for m in range(len(gene)-2):
                  n=m+2
                  while n< len(gene)-1:
                        if(self.dis[gene[m]][gene[n]]+self.dis[gene[m+1]][gene[n+1]]
                                <self.dis[gene[m]][gene[m+1]]+self.dis[gene[n]][gene[n+1]]):
                              temp_gene=gene.copy()
                              gene = temp_gene[:m + 1] + temp_gene[m + 1:n + 1][::-1] + temp_gene[n + 1:]
                        n+=1
            return gene


      def judge(self):
            """评估，计算每一个个体的适配值"""
            self.bounds = 0.0
            self.best1 = self.lives[0]
            for life in self.lives:
                  life.score = self.matchFun(life)
                  self.bounds += 1/life.score
                  if self.best1.score < life.score:     #获得当前最佳基因
                        self.best1 = life
            if self.best.score < self.best1.score:
                  self.best = self.best1

      def setRoulette(self):
            for life in self.lives:
                  life.roulette = 1 / life.score / self.bounds
            i = 1
            while i < len(self.lives):
                  self.lives[i].roulette += self.lives[i - 1].roulette
                  i += 1


      def crossover(self,lives):
            queue=[]
            for i in range(self.lifeCount):
                  rant=random.random()
                  if rant<self.croessRate:
                        queue.append(i)
            random.shuffle(queue)
            i = 0
            j = len(queue) - 1
            while i < j:
                  self.docross(lives,queue[i], queue[i + 1])
                  i += 2
            return lives

      def docross(self,lives,x, y):
            child1 = self.getChild(1,lives, x, y)
            child2 = self.getChild(2,lives, x, y)
            lives[x] = Life(child1)
            lives[y] = Life(child2)


      def getChild(self,flag,lives,x,y):
            newGene=[]
            px=lives[x].gene.copy()
            py=lives[y].gene.copy()
            c=px[random.randint(0,len(px)-1)]
            newGene.append(c)
            index1,index2=-1,-1
            dx,dy=-1,-1
            while len(px)>1:
                  for p in px:
                        if p==c:
                              index1=px.index(p)
                              break
                  for p in py:
                        if p==c:
                              index2=py.index(p)
                              break
                  if flag==1:
                        if index1>0:
                              dx=px[index1-1]
                        else:
                              dx=px[len(px)-1]
                        if index2>0:
                              dy=py[index2-1]
                        else:
                              dy=py[len(px)-1]
                  elif flag==2:
                        if index1<len(px)-1:
                              dx=px[index1+1]
                        else:
                              dx=px[0]
                        if index2<len(px)-1:
                              dy=py[index2+1]
                        else:
                              dy=py[0]
                  px.remove(c)
                  py.remove(c)
                  if self.dis[c][dx]<self.dis[c][dy]:
                        c=dx
                  else:
                        c=dy
                  newGene.append(c)
            return newGene

      def mutation(self,lives):
            for i in range(len(lives)):
                  gene_mut=lives[i].gene.copy()
                  rate = random.random()
                  if rate < self.mutationRate:
                        rate2 = random.random()
                        if rate2 > 0.5:
                              lives[i].gene= self.pushmutation(gene_mut)
                        else:
                              lives[i].gene= self.domutation(gene_mut)
                        i-=1
            return lives

      def domutation(self, gene):
            """突变，选两个两两交换"""
            while True:
                  index1 = random.randint(0, self.geneLenght -3)
                  index2 = random.randint(0, self.geneLenght-1)
                  if(index1<index2):
                        break

            newGene = gene[:]  # 产生一个新的基因序列，以免变异的时候影响父种群
            i, j = 0, index2 - index1 + 1
            while i<j:
                  newGene[index1+i], newGene[index2-i] = newGene[index2-i], newGene[index1+i]
                  i+=1
                  j>>1
            self.mutationCount += 1
            return newGene

      def pushmutation(self,gene):
            """突变，选三个两两交换"""
            while True:
                  index1 = random.randint(0, (len(gene)-1)<<1)
                  index2 = random.randint(0, len(gene)-1)
                  if index1<index2 and index1>0:
                        break
            s1=gene[0:index1]
            s2=gene[index1:index2]
            s3=gene[index2:len(gene)]
            newGene=s2+s1+s3
            self.mutationCount += 1
            return newGene

      def getOne(self):
            r=random.random()
            for life in self.lives:
                  if r<=life.roulette:
                        return life
            raise Exception("选择错误", self.bounds)

      def next(self):
            """产生下一代"""

            self.generation += 1
            self.judge()
            do_best=self.domutation(self.best1.gene)
            push_best=self.pushmutation(self.best1.gene)
            newLives = []
            newLives.append(Life(self.best.gene))  # 把最好的个体加入下一代
            newLives.append(Life(do_best))
            newLives.append(Life(push_best))
            newLives.append(Life(self.best1.gene))

            self.setRoulette()

            while len(newLives) < self.lifeCount:
                  newLives.append(self.getOne())

            newLives=self.crossover(newLives)
            newLives=self.mutation(newLives)
            self.lives=newLives






