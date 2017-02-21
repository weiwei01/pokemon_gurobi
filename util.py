import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import json
import math

def export2json(filename, sol_best):
    coord = []
    for line in open(filename,"r").readlines():
        x=line.strip("\r\n").split(",")
        coord.append({'lat':x[0],'lng':x[1]})

    export_data = []
    for i in range(len(sol_best)):
        export_data.append(coord[ int(sol_best[i]) ])

    file = open("path.json", 'w')
    file.write(json.dumps(export_data))
    file.close()

def distance(points, i, j):
  dx = points[i][0] - points[j][0]
  dy = points[i][1] - points[j][1]
  return math.sqrt(dx*dx + dy*dy)

def getFilename(args):
    # Use the corresponding data file
    if args.file:
      filename = args.file
    elif args.data == 'nctu':
      filename = "data/nctu.csv"
    elif args.data == 'nthu':
      filename = "data/nthu.csv"
    elif args.data == 'thu':
      filename = "data/thu.csv"
    elif args.data == 'ncku':     
      filename = "data/ncku.csv"
    else:
      print("ERROR: undefined data file")


"""
#define pij travel time
p = [[0,4,3],
     [4,0,2],
     [3,2,0]]
print(p)
"""
#i j random travel time
"""
for i in range(n):
  for j in range(n):
    if i == j:
      p[i][j] = 0
    else:
      ijTravelTime = random.randint(1,7)
      p[i][j] = ijTravelTime
      p[j][i] = ijTravelTime
"""


#print travel time matrix
def printTravelTimeMatrix(p,n):
  p1=[[0 for i in range(n+1)] for j in range(n+1)]
  for i in range(n):
    for j in range(n):
      p1[i+1][j+1] = p[i][j]
  for i in range(n):
    for j in range(n):
      if i == 0 and j > 0:
       p1[i][j+1] = j
      elif j == 0 and i > 0:
        p1[i+1][j] = i
  for i in p1:
     print(i)

def printOptimalEdges(selected,n,T):
  print("selected: ")
  times = 0
  for i,j,t in selected:
    print(times,"-->",i,j,t)
    times = times + 1
  result = [[0 for i in range(n*T)]for j in range(n*T)]


def readDataAndConvertToUnit(filename,p,n):
    #資料集
    with open(filename) as f:
        alist = [line.rstrip() for line in f]

    points = []
    for i in range(n):
      #把經緯度放進points
      points.append( (float(alist[i].split(',')[0]), float(alist[i].split(',')[1])))  
      #print('points[{}] is {}'.format(i ,points[i] ))

    #convert coordinate degree distance to unit 
    for i in range(n):
      #print("i: ", i)
      for j in range(n):
        #print("j: ", j)
        if i == j:
          p[i][j] = 0
        else:
          distance_long = int((distance(points, i, j)*110000)/70)
          if distance_long == 0:#if dist too short(less than 1), would be one
            p[i][j] = 1
          else:
            p[i][j] = distance_long
      
"""for i in p:
                  print(i)"""