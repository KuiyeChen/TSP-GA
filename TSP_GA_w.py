# -*- encoding: utf-8 -*-

import math
import numpy as np
import tkinter as Tkinter
from GA import GA
import time

class TSP_WIN(object):

      def __init__(self, aRoot, aLifeCount = 30, aWidth = 800, aHeight = 800):
            self.root = aRoot
            self.lifeCount = aLifeCount
            self.width = aWidth
            self.height = aHeight
            self.canvas = Tkinter.Canvas(
                        self.root,
                        width = self.width,
                        height = self.height,
                  )
            self.canvas.pack(expand = Tkinter.YES, fill = Tkinter.BOTH)
            self.bindEvents()
            self.initCitys()
            self.new()
            self.title("TSP")


      def initCitys(self):
            self.citys = np.loadtxt('data/city300.txt',skiprows=6,usecols=(1,2),comments='EOF')
            city_num=len(self.citys)

            self.dis = [[0 for x in range(city_num)] for y in range(city_num)]
            for i in range(city_num):
                  for j in range(city_num):
                        self.dis[i][j] = math.sqrt((self.citys[i][0] - self.citys[j][0]) ** 2 + (self.citys[i][1] - self.citys[j][1]) ** 2)

            #坐标变换
            minX, minY = self.citys[0][0], self.citys[0][1]
            maxX, maxY = minX, minY
            for city in self.citys[1:]:
                  if minX > city[0]:
                        minX = city[0]
                  if minY > city[1]:
                        minY = city[1]
                  if maxX < city[0]:
                        maxX = city[0]
                  if maxY < city[1]:
                        maxY = city[1]

            w = maxX - minX
            h = maxY - minY
            xoffset = 15
            yoffset = 15
            ww = self.width - 2 * xoffset
            hh = self.height - 2 * yoffset
            xx = ww / float(w)
            yy = hh / float(h)
            r = 2
            self.nodes = []
            self.nodes2 = []
            for city in self.citys:
                  x = (city[0] - minX ) * xx + xoffset
                  y = hh - (city[1] - minY) * yy + yoffset
                  self.nodes.append((x, y))
                  node = self.canvas.create_oval(x - r, y -r, x + r, y + r,
                        fill = "#ff0000",
                        outline = "#000000",
                        tags = "node",)
                  self.nodes2.append(node)

            

            
      def distance(self, order):                     #计算经过所有城市的路程和
            distance = 0.0
            for i in range(-1, len(self.citys) - 1):
                  index1, index2 = order[i], order[i + 1]
                  distance+=self.dis[index1][index2]
            return distance



      def matchFun(self):
            return lambda life: 1 / self.distance(life.gene)


      def title(self, text):
            self.root.title(text)


      def line(self, order):
            self.canvas.delete("line") 
            for i in range(-1, len(order) -1):  #首尾相连
                  p1 = self.nodes[order[i]]
                  p2 = self.nodes[order[i + 1]]
                  self.canvas.create_line(p1, p2, fill = "#000000", tags = "line")
 


      def bindEvents(self):
            self.root.bind('<F1>', self.new)   #初始化
            self.root.bind('<F2>', self.start) #开始迭代
            self.root.bind('<F3>', self.stop)  #暂停迭代


      def new(self, evt = None):
            self.isRunning = False
            order = range(len(self.citys))
            self.line(order)
            self.ga = GA(aCrossRate =0.9,
                  aMutationRage = 0.01,
                  aLifeCount = self.lifeCount, 
                  aGeneLenght = len(self.citys),
                  dis=self.dis,
                  aMatchFun = self.matchFun())


      def start(self, evt = None):
            self.isRunning = True
            while self.isRunning:
                  self.ga.next()
                  distance = self.distance(self.ga.best.gene)
                  self.line(self.ga.best.gene)
                  self.title(("TSP-gen: {0}  Length: {1}").format(self.ga.generation,distance))
                  print("当前迭代次数：",self.ga.generation," 当前最优解：",distance)
                  self.canvas.update()


      def stop(self, evt = None):
            self.isRunning = False
            #print(self.ga.best.gene)
            best_gene=self.ga.best.gene.copy()
            print(self.distance(self.ga.best.gene))
            print(best_gene)


      def mainloop(self):
            self.root.mainloop()


def main():
      #tsp = TSP()
      #tsp.run(10000)

      tsp = TSP_WIN(Tkinter.Tk())
      tsp.mainloop()


if __name__ == '__main__':
      main()