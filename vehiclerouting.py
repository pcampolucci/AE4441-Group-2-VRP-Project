# -*- coding: utf-8 -*-
"""
Title: Drone Routing
Author: Tomaso De Ponti, Pietro Campolucci, Enerko Rodriguez Plaza
"""

# Importing packages
import numpy as np
import os
import pandas as pd
import time
from gurobipy import Model, GRB, LinExpr
import pickle
from copy import deepcopy

# Add debugging option
DEBUG = True

# Get path to current folder
cwd = os.getcwd()
print(cwd)
# Get all instances
full_list = os.listdir(cwd)

# instance name
instance_name = 'database/pvr.xlsx'
# Load data for this instance
edges = pd.read_excel(os.path.join(cwd,instance_name),sheet_name='data')
print("edges",edges)
### Model options ###
droneFC= 5
K=100

startTimeSetUp = time.time()
model = Model()
#################
### VARIABLES ###
#################
x = {}
for i in range(0, len(edges)):
    x[edges['From'][i], edges['To'][i]] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY,name="x[%s,%s]" % (edges['From'][i], edges['To'][i]))
print(x)
s = {}
for i in range(1, max(edges['From']+1)):
    s[i] = model.addVar(lb=0,ub=100,vtype=GRB.INTEGER, name="s[%s]"%i)
model.update()

###################
### CONSTRAINTS ###
###################

source = 100
sink   = 25
sinko   = 1
print(len(edges) - 1)
print(edges['From'][len(edges) - 1])
print(range(1, edges['From'][len(edges) - 1]))
#for i in range(1, edges['From'][len(edges) - 1]):
for i in range(1, max(edges['From']+1)):
    print("Node",i)
    idx_this_node_out = np.where(edges['From'] == i)[0]
    idx_this_node_in = np.where(edges['To'] == i)[0]
    print("idx_this_node_out",idx_this_node_out)
    print("idx_this_node_in", idx_this_node_in)
    if i != source and i != sink:
        thisLHS = LinExpr()
        if len(idx_this_node_out) > 0:
            for j in range(0, len(idx_this_node_out)):
                thisLHS += x[i, edges['To'][idx_this_node_out[j]]]

        if len(idx_this_node_in) > 0:
            for j in range(0, len(idx_this_node_in)):
                thisLHS -= x[edges['From'][idx_this_node_in[j]], i]
        model.addConstr(lhs=thisLHS, sense=GRB.EQUAL, rhs=0,
                        name='node_flow_' + str(i))
    if i is source:
        thisLHS = LinExpr()
        if len(idx_this_node_out) > 0:
            for j in range(0, len(idx_this_node_out)):
                thisLHS += x[i, edges['To'][idx_this_node_out[j]]]
        model.addConstr(lhs=thisLHS, sense=GRB.EQUAL, rhs=1,name='node_' + str(i) + '_source_out')

        thisLHS = LinExpr()
        if len(idx_this_node_in) > 0:
            for j in range(0, len(idx_this_node_in)):
                thisLHS += x[edges['From'][idx_this_node_in[j]], i]
            model.addConstr(lhs=thisLHS, sense=GRB.EQUAL, rhs=1,name='node_' + str(i) + '_source_in')

    if i is sink:
        thisLHS = LinExpr()
        if len(idx_this_node_in) > 0:
            for j in range(0, len(idx_this_node_in)):
                thisLHS += x[edges['From'][idx_this_node_in[j]], i]
            model.addConstr(lhs=thisLHS, sense=GRB.EQUAL, rhs=1,
                                name='node_' + str(i) + '_sink_in')
        thisLHS = LinExpr()
        if len(idx_this_node_out) > 0:
            for j in range(0, len(idx_this_node_out)):
                thisLHS += x[i, edges['To'][idx_this_node_out[j]]]
            model.addConstr(lhs=thisLHS, sense=GRB.EQUAL, rhs=0,
                                name='node_' + str(i) + '_sink_out')

    thisLHS = LinExpr()
    if len(idx_this_node_out) > 0:
        for j in range(0, len(idx_this_node_out)):
            thisLHS += x[i, edges['To'][idx_this_node_out[j]]]
        model.addConstr(lhs=thisLHS, sense=GRB.EQUAL, rhs=1, name='node_out_' + str(i))
    thisLHS = LinExpr()
    # if len(idx_this_node_in) > 0:
    #     for j in range(0, len(idx_this_node_in)):
    #         thisLHS += x[edges['From'][idx_this_node_in[j]], i]
    #     model.addConstr(lhs=thisLHS, sense=GRB.EQUAL, rhs=1, name='node_in_' + str(i))
count = 0
for i in range(1, max(edges['From']+1)):
    for j in range (1, max(edges['From']+1)):
        print(count)
        if i != j & j!=1:
            #can add here an if for impossible edges
            thisLHS= LinExpr()
            thisLHS= s[i]-s[j]+edges['Distance'][count]-K*(1-x[i,j])#[i+j-1]#+K*(1-x[i,j])#+edges['Distance'][1]
            print(thisLHS)
            print("i",i)
            print("j",j)
            model.addConstr(lhs=thisLHS, sense = GRB.LESS_EQUAL, rhs=0, name='time_' + str(i)+str(j))
            count = count + 1


model.update()
obj = LinExpr()

for i in range(0, len(edges)):
    obj += edges['Distance'][i] * x[edges['From'][i], edges['To'][i]]

model.setObjective(obj, GRB.MINIMIZE)
model.update()
model.write('LPSolve/model_formulation2.lp')

model.optimize()
endTime = time.time()

solution = []

for v in model.getVars():
    if v.x==1:
        solution.append([v.varName])
print(solution)
route_complete = False
current_node = source
path = [source]

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



