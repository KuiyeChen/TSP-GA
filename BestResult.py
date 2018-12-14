import tkinter as Tkinter
import numpy as np
import math

width,height=1000,1000
city_num=130
root = Tkinter.Tk()
canvas= Tkinter.Canvas(root,bg='white',width=1000,height=1000)
canvas.pack(expand = Tkinter.YES, fill = Tkinter.BOTH)
root.title("最优解")

citys = np.loadtxt('data/city130.txt',skiprows=6,usecols=(1,2),comments='EOF')
# for i in range(city_num):
#       for j in range(2):
#             citys[i][j]=round(citys[i][j],2)

#坐标变换
minX, minY = citys[0][0], citys[0][1]
maxX, maxY = minX, minY
for city in citys[1:]:
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
xoffset = 30
yoffset = 30
ww = width - 2 * xoffset
hh = height - 2 * yoffset
xx = ww / float(w)
yy = hh / float(h)
r = 2
nodes = []
nodes2 = []
for city in citys:
      x = (city[0] - minX ) * xx + xoffset
      y = hh - (city[1] - minY) * yy + yoffset
      nodes.append((x, y))
      node = canvas.create_oval(x - r, y -r, x + r, y + r,
            fill = "#ff0000",
            outline = "#000000",
            tags = "node",)
      nodes2.append(node)

order = np.loadtxt('data/tour_section.txt',dtype=int)

for i in range(city_num):
    p1 = nodes[order[i]]
    p2 = nodes[order[i+1]]
    canvas.create_line(p1, p2, fill="#000000", tags="line")

distance = 0.0
for i in range(city_num):
      index1, index2 = order[i], order[i + 1]
      city1, city2 = citys[index1], citys[index2]
      distance +=math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
print (distance)

root.mainloop()