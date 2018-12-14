import math
import numpy as np

citys = np.loadtxt('data/city_location.txt')
for i in range(len(citys)):
      for j in range(2):
            citys[i][j]=round(citys[i][j])

dis=[[0 for x in range(len(citys))] for y in range(len(citys))]
for i in range(len(citys)):
    for j in range(len(citys)):
        dis[i][j]=math.sqrt((citys[i][0]-citys[j][0])**2+(citys[i][1]-citys[j][1])**2)
