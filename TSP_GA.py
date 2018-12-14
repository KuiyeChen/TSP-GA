# -*- encoding: utf-8 -*-

import random
import math
from GA import GA
import numpy as np
import time

class TSP(object):
      def __init__(self, aLifeCount = 30,):
            self.initCitys()
            self.lifeCount = aLifeCount
            self.ga = GA(aCrossRate = 0.9,
                  aMutationRage = 0.01,
                  aLifeCount = self.lifeCount, 
                  aGeneLenght = len(self.citys),
                  dis=self.dis,
                  aMatchFun = self.matchFun())


      def initCitys(self):
            self.citys =np.loadtxt('data/city300.txt',skiprows=6,usecols=(1,2),comments='EOF')
            city_num=len(self.citys)
            self.dis = [[0 for x in range(city_num)] for y in range(city_num)]
            for i in range(city_num):
                  for j in range(city_num):
                        self.dis[i][j] = math.sqrt(
                              (self.citys[i][0] - self.citys[j][0]) ** 2 + (self.citys[i][1] - self.citys[j][1]) ** 2)

      def distance(self, order):
            distance = 0.0
            for i in range(-1, len(order) - 1):
                  index1, index2 = order[i], order[i + 1]
                  distance += self.dis[index1][index2]
            return distance


      def matchFun(self):
            return lambda life: 1.0 / self.distance(life.gene)


      def run(self, n = 0):
            while n > 0:
                  self.ga.next()
                  distance = self.distance(self.ga.best.gene)
                  print ("当前迭代次数：",self.ga.generation," 当前最优解", distance)
                  n-=1
            print(self.ga.best.gene)


def main():
      print(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())))
      tsp = TSP()
      tsp.run(30000)


if __name__ == '__main__':
      main()


