
# -*- coding: utf-8 -*-
"""
@author: tdeponti
"""
# Loading packages that are used in the code
import numpy as np
import os
import pandas as pd
import time
from gurobipy import Model,GRB,LinExpr
import pickle
from copy import deepcopy

# Get path to current folder
cwd = os.getcwd()
print(cwd)
# Get all instances
full_list           = os.listdir(cwd)

# instance name
instance_name = 'pvr.xlsx'
# Load data for this instance
edges= pd.read_excel(os.path.join(cwd,instance_name),sheet_name='data')
print("edges",edges)
### Model options ###
droneFC= 5
K=100
custumerdemand=1
maxpayload=3
costperkm=0.5
maxdrones=10
maxrange=15


startTimeSetUp = time.time()
model = Model()
#################
### VARIABLES ###
#################
xk = {}
for k in range(1,maxdrones+1):
    xk[k] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY,name="xk[%s]" % (k))
x = {}
for k in range(1,maxdrones+1):
    for i in range(0, len(edges)):
        x[edges['From'][i], edges['To'][i],k] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY,name="x[%s,%s,%s]" % (edges['From'][i], edges['To'][i],k))

s = {}
for i in range(1, max(edges['From']+1)):
    for k in range(1, maxdrones + 1):
        s[i,k] = model.addVar(lb=0,ub=100,vtype=GRB.INTEGER, name="s[%s,%s]"%(i,k))
model.update()

###################
### CONSTRAINTS ###
###################
print(len(edges) - 1)
print(edges['From'][len(edges) - 1])
print(range(1, edges['From'][len(edges) - 1]))
#for i in range(1, edges['From'][len(edges) - 1]):

for i in range(1, max(edges['From']+1)):
    print("Node",i)
    idx_this_node_out = np.where(edges['From'] == i)[0]
    idx_this_node_in = np.where(edges['To'] == i)[0]

    thisLHS = LinExpr()
    if len(idx_this_node_out) > 0:
        for k in range(1, maxdrones + 1):
            for j in range(0, len(idx_this_node_out)):
                thisLHS += x[i, edges['To'][idx_this_node_out[j]],k]
                thisLHS -= x[edges['From'][idx_this_node_in[j]], i, k]
            model.addConstr(lhs=thisLHS, sense=GRB.EQUAL, rhs=0,name='node_flow_' + str(i)+str(k))
    # if len(idx_this_node_in) > 0:
    #     for j in range(0, len(idx_this_node_in)):
    #         for k in range(1, maxdrones + 1):
    #             thisLHS -= x[edges['From'][idx_this_node_in[j]], i,k]
    # model.addConstr(lhs=thisLHS, sense=GRB.EQUAL, rhs=0,
    #                     name='node_flow_' + str(i))
    thisLHS = LinExpr()
    if i > 1:
        for j in range(0, len(idx_this_node_out)):
            for k in range(1, maxdrones + 1):
                thisLHS += x[i, edges['To'][idx_this_node_out[j]],k]
        model.addConstr(lhs=thisLHS, sense=GRB.EQUAL, rhs=1, name='node_out_' + str(i))


for k in range(1, maxdrones + 1):
    thisLHS1 = LinExpr()
    thisLHS2 = LinExpr()
    thisLHS = LinExpr()
    thisrangeLHS = LinExpr()
    count=0
    for i in range(1, max(edges['From'] + 1)):
        if i != 1:
            thisLHS1+= x[1,i,k]
            thisLHS2+= x[i,1,k]
        for j in range(1, max(edges['From'] + 1)):
            if j != i:
                thisLHS+= x[i,j,k]
                thisrangeLHS+= x[i,j,k]*edges['Distance'][count]
                count+= 1
    thisLHS = thisLHS*custumerdemand
    thisLHS1 -= xk[k]
    thisLHS2 -= xk[k]
    model.addConstr(lhs=thisLHS1, sense=GRB.EQUAL, rhs=0, name='drone_out_' + str(k))
    model.addConstr(lhs=thisLHS2, sense=GRB.EQUAL, rhs=0, name='drone_in_' + str(k))
    model.addConstr(lhs=thisLHS, sense=GRB.LESS_EQUAL, rhs=maxpayload, name='drone_payload_' + str(k))
    model.addConstr(lhs=thisrangeLHS, sense=GRB.LESS_EQUAL, rhs=maxrange, name='drone_range_' + str(k))







thisLHS = LinExpr()
count = 0
for i in range(1, max(edges['From']+1)):
    for j in range (1, max(edges['From']+1)):
        print(count)
        if i != j & j!=1:
            for k in range(1, maxdrones + 1):
                #can add here an if for impossible edges
                thisLHS= LinExpr()
                thisLHS= s[i,k]-s[j,k]+edges['Distance'][count]-K*(1-x[i,j,k])#[i+j-1]#+K*(1-x[i,j])#+edges['Distance'][1]

                model.addConstr(lhs=thisLHS, sense = GRB.LESS_EQUAL, rhs=0, name='time_' + str(i)+str(j)+str(k))
            count = count + 1


model.update()
obj = LinExpr()

for i in range(0, len(edges)):
    for k in range(1, maxdrones + 1):
        obj += edges['Distance'][i] * x[edges['From'][i], edges['To'][i],k]*costperkm
for k in range(1,maxdrones+1):
    obj += xk[k]*droneFC



model.setObjective(obj, GRB.MINIMIZE)
model.update()
model.write('model_formulation2.lp')

model.optimize()
endTime = time.time()

solution = []
activedrones =[]

for v in model.getVars():
    if v.x==1:
        solution.append([v.varName])
    #if v.xk==1:
    #    activedrones.append([v.varName])
print(activedrones)
print(solution)

route_complete = False


# while route_complete is False:
#     # Connections from current node
#     idx_this_node_out = np.where(edges['From'] == current_node)[0]
#     # print(idx_this_node_out)
#     for i in range(0, len(idx_this_node_out)):
#         if x[current_node, edges['To'][idx_this_node_out[i]]].x >= 0.99:
#             path.append(edges['To'][idx_this_node_out[i]])
#             current_node = edges['To'][idx_this_node_out[i]]
#
#             if current_node == sinko:
#             #if current_node == 1:
#                 route_complete = True
#                 break
#             else:
#                 break
#     print("running...")
#
# print(path)



