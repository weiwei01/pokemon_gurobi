
from gurobipy import *
import random
import math
from util import *
from args import *

model = Model('Maximum Pickup Routing')


############import and print distance############
# Get arguments
args = parse_args()
#Time T
T = int(args.time)
#Given n location i = 1 ~ n
n = int(args.number)
#award on i location
a = [random.randint(2,6) for i in range(n)]
print("award list\n",a)
#delay time on i location
d = [5 for i in range(n)]
print("delay list\n",d)
#Pij(Point i_j travel time)
p = [[0 for i in range(n)] for j in range(n)]

#filename = getFilename(args)
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
elif args.data == 'demo':     
  filename = "data/demo.csv"
else:
  print("ERROR: undefined data file")

print("number: "+ args.number)
print("filename: ",filename)
readDataAndConvertToUnit(filename,p,n)
print("travel time matrix\n")
printTravelTimeMatrix(p,n)
#####################modeling####################
sides = {}
for i in range(n):
    sides.update({(0,i,0):(1)})
#print("0: ", sides)
def updateListFun(sides):  
  updateList = {}
  for side in sides:
    i = side[0]
    j = side[1]
    t = side[2]
    if i == j:
      for k in range(n):
        if t + 5 < T :
          updateList.update({(j,k,t+5):(1)})
    else:
      for k in range(n):
        if t + p[i][j] < T :
          updateList.update({(j,k,t+p[i][j]):(1)})
  sides.update(updateList)
  return len(sides)
sideLength = 0
print("len(sides)" ,"--------------->",len(sides))

for i in range(T):
  if sideLength == updateListFun(sides):
    break
  else:
    sideLength = updateListFun(sides)
  print("length" ,"--------------->",sideLength)
  print("loopN ","--------------->",i)
  #print(sides)

delList = {}
for side in sides:
  i = side[0]
  j = side[1]
  t = side[2]
  if i == j and t + 5 > T:
    delList.update({(i,j,t):(1)})
  elif t+p[i][j] >T:
    delList.update({(i,j,t):(1)})
     
#print("delList: ", delList)
for delname in delList:
  del sides[delname]

#print("5: ",sides)
selectedSides = sorted(sides, key=lambda selectedT: selectedT[2])
#print("sorted: ", selectedSides)

edges = sides

vertices = {}
for edge in edges:
  i = edge[0]
  j = edge[1]
  t = edge[2]  
  vertices.update({(i,t):(1)})
  if t+p[i][j] < T:
    vertices.update({(j,t+p[i][j]):(1)})
#print("vertices: ", vertices)
#################################################
y = {} # Binary variables for collect location and time
x = {} # Binary variable for location i and j and time t


for vertex in vertices:
  i = vertex [0]
  t = vertex[1]
  #print("vertex i, t: ",i,t)
  y[vertex] = model.addVar(vtype=GRB.BINARY, name="y" + str(i) + "_" + str(t))


"""for i in range(n):
    for t in range(T):
        y[i,t] = model.addVar(vtype=GRB.BINARY, name="y" + str(i) + "_" + str(t))"""


for edge in edges:
  i = edge[0]
  j = edge[1]
  t = edge[2]  
  x[edge] = model.addVar(vtype=GRB.BINARY, name="x" + str(i) + "_" + str(j)+ "_" + str(t))

"""
for i in range(n):
    for j in range(n):
        for t in range(T):
               x[i,j,t] = model.addVar(vtype=GRB.BINARY, name="x" + str(i) + "_" + str(j)+ "_" + str(t))
"""


#constraint - flow constraint

model.addConstr(quicksum(x[edge]for edge in edges if edge[0] == 0 and edge[2] == 0) == 1, name = "start")
model.addConstr(quicksum(x[edge]for edge in edges if edge[2] + p[edge[0]][edge[1]] == T-1 and edge[1] == 0) == 1, name = "leave")

#model.addConstr(quicksum(x[0,i,0]   for i in range(n)) == 1)
#model.addConstr(quicksum(x[i,0,T-1] for i in range(n) if i != 0)  == 1)
#model.addConstr(quicksum(x[i,j,0]   for i in range(n) for j in range(n) if i != 0) == 0)
#model.addConstr(quicksum(x[i,j,T-1] for i in range(n) for j in range(n) if j != 0) == 0)
#model.addConstr(quicksum(y[i,0]     for i in range(n)) == 1)
#model.addConstr(quicksum(y[i,T-1]   for i in range(n)) == 1)
for t in range(T):
  model.addConstr(quicksum(x[edge]for edge in edges if edge[2] == t) <= 1, name = "time")
"""
for t in range(T):
  model.addConstr(quicksum(y[i,t] for i in range(n)) <= 1)
"""


#for i in range(n):
# if i != 0:
#  model.addConstr(quicksum(y[i,t]for t in range(1,p[0][i]))==0)

#model.addConstr(quicksum(y[0,t]for t in range(1,5)) == 0)
#model.addConstr(quicksum(y[1,t]for t in range(1,p[0][1]))==0)
#model.addConstr(quicksum(y[2,t]for t in range(1,p[0][2]))==0)

"""for edge in edges:
  i = edge[0]
  j = edge[1]
  k = edge[2]
  if k != 0 and k != T-1:
    model.addConstr(quicksum(x[edge1] for edge1 in edges if edge1[0] == j and edge1[2]  == k + p[j][i])-
                    quicksum(x[edge2] for edge2 in edges if edge2[1] == j and edge2[2]  == k) == 0, name="conser"+str(edge))
"""


# constraints - flow conservation
edgeIn   = { v:[] for v in vertices }
edgeOut  = { v:[] for v in vertices }
for edge in edges:
  u = edge[0]
  v = edge[1]
  w = edge[2]
  if w + p[u][v] < T :
    edgeIn[v, w + p[u][v]] = edgeIn[v, w + p[u][v]] + [x[edge]]
    edgeOut[u,w] = edgeOut[u,w] + [x[edge]]

#print("edgeIn", edgeIn)
#print("edgeOut", edgeOut)
delEdgeInOutList = {}
for edgeInItem in edgeIn:
  i = edgeInItem[0]
  j = edgeInItem[1]
  if j == 0:
    delEdgeInOutList.update({(i,j):(1)})
  elif j == T-1:
    delEdgeInOutList.update({(i,j):(1)})
     
#print("delEdgeInOutList: ", delEdgeInOutList)
for delname in delEdgeInOutList:
  del edgeIn[delname]
  del edgeOut[delname]

for v in edgeIn:
  model.addConstr(quicksum(edgeIn[v]) - quicksum(edgeOut[v]) == 0, name= "conser"+str(v))



"""
for i in range(n):
  for t in range(T):
    if t != 0 and t + p[i][j] < T-1 and t < T-1:
      model.addConstr(quicksum(x[j,i,t+p[j][i]] for j in range(n) if t+p[j][i]<T) -
                       quicksum(x[i,j,t] for j in range(n)) == 0)
"""


"""
#constrained - bag
model.addConstr(quicksum(quicksum(a[i]*y[i,t]for t in range(T))for i in range(n))>=capacity)
"""
#constraint

#if didn't go to i point, then no collect i point

for vertex in vertices:
  if vertex[1] != 0:
    model.addConstr(y[vertex] <= quicksum(x[edge]for edge in edges if edge[0] != edge[1] and edge[1] == vertex[0] and edge[2] == vertex[1]-p[edge[0]][edge[1]]) , name="pass"+str(vertex))

"""for j in range(n):
  for t in range(T):
    #if t != 0:
        model.addConstr(y[j,t] <= quicksum(x[i,j,t-p[i][j]]for i in range(n) if t-p[i][j]>=0))"""

#constraint
#if collect, then cant collect before delay time end
for vertex in vertices:
  model.addConstr(y[vertex] <= 1 - quicksum(y[vertex1] for vertex1 in vertices if vertex[0] == vertex1[0] and vertex1[1] < vertex[1]+d[vertex[0]]-1 and vertex1[1] > vertex[1] ), name="delay"+str(vertex))

"""for i in range(n):
    for t in range(T):
      #if t + d[i] < T:
          model.addConstr(y[i,t] <= 1-quicksum(y[i,s] for s in range(t+1,t+d[i]) if s < T))
"""
model.addConstr(quicksum((a[edge[0]] * y[edge]) for edge in vertices)<=250)
#model.addConstr(quicksum((a[edge[0]] * y[edge]) for edge in vertices)<=260)




model.update()


#Objective
obj =  quicksum((a[edge[0]] * y[edge]) for edge in vertices)
model.setObjective(obj, GRB.MAXIMIZE)




#model optimize and debug
"""model.optimize()
model.write("max.sol") 
model.write("max.lp") 
print('Optimal reward: %g' % model.objVal)"""


"""if model.status == GRB.Status.INF_OR_UNBD: 
# Turn presolve off to determine whether model is infeasible 
# or unbounded 
  model.setParam(GRB.Param.Presolve, 0) 
  model.optimize()
  model.computeIIS() 
  model.write("model.ilp")  
  model.write("max.lp") 
  model.write("max.sol")"""

"""if model.status == GRB.Status.OPTIMAL: 
  print('Optimal reward: %g' % model.objVal) 
  model.write("max.lp") 
  model.write("max.sol") 
  exit(0) 
elif model.status == GRB.Status.INFEASIBLE: 
  print('Optimization was stopped with status %d' % model.status) 
  model.computeIIS() 
  model.write("model.ilp")
  exit(0)
elif model.status != GRB.Status.INFEASIBLE: 
  print('Optimization was stopped with status %d' % model.status) 
  model.optimize()
  model.write("max.lp") 
  model.write("max.sol")"""

model.optimize()
status = model.status
print("model status: ", model.status)
if status == gurobipy.GRB.status.INF_OR_UNBD or status == gurobipy.GRB.status.INFEASIBLE or status == gurobipy.GRB.status.UNBOUNDED:
  print('The model cannot be solved because it is infeasible or unbounded!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
  model.computeIIS() 
  model.write("max.ilp")
if status == gurobipy.GRB.status.OPTIMAL:
  print('Optimization was stopped with status %s' % (str(status)))
  print('Optimal reward: %g' % model.objVal)
  model.write("max.lp") 
  model.write("max.sol")



#print solution
#print x
solution = model.getAttr("x", x)
#print("solution: ", solution)
selected = [(i,j,t) for i,j,t in edges if solution[i,j,t] > 0.5]
#print("selected  ", selected)
#Sorting X Edge
selectedEdge = sorted(selected, key=lambda selectedT: selectedT[2])
print("sorted: ", selectedEdge)
printOptimalEdges(selectedEdge,n,T)
#print('Optimal tour: %s' % str(subtour(selected)))



#print Y
solution = model.getAttr("x", y)
selected = [(i,t) for i,t in vertices  if solution[i,t] > 0.5]

print("y selected: ", selected)

#Sorting Y Point
print("sorted: ",sorted(selected, key=lambda student: student[1]))
yresult = sorted(selected, key=lambda student: student[1])

#Routing Points
arrange = [[0 for i in range(2)]for j in range(len(yresult))]
arrList = []
for i in range(T):
  if i < len(yresult):
    arrList.append(yresult[i][0])
  #print(yresult[i][0]) 
  #print(arrList)

for i in range(len(arrList)):
  if i == 0:
    arrange[0][0] = arrList[i]
  else:
    arrange[i-1][1] = arrList[i]
    arrange[i][0] = arrList[i]
print ("routing point: ", arrange)
export2json(filename, arrList)
print ("export2json success")







