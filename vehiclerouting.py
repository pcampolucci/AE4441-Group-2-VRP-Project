
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

#from plotter import do_plot

# Get path to current folder
cwd = os.getcwd()
print(cwd)
# Get all instances
full_list = os.listdir(cwd)

instance_name ='/pvrold.xlsx'
#instance_name = '/database/pvr.xlsx'
#instance_name = '/pvr.xlsx'
# Load data for this instance
edges= pd.read_excel(cwd + instance_name, sheet_name='data')
print("edges", edges)

### Model options ###
droneFC= 5
K=100
custumerdemand=1
maxpayload=3
costperkm=0.5
maxdrones=10
maxrange=200
speed=150
takeofftime=2
landingtime=2
unloadingtime=5




startTimeSetUp = time.time()
model = Model()
maxnode = max(edges['From']+1)
#################
### VARIABLES ###
#################

xk = {}
x = {}
for k in range(1,maxdrones+1):
    xk[k] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY,name="xk[%s]" % (k))
    for i in range(0, len(edges)):
        x[edges['From'][i], edges['To'][i],k] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY,name="x[%s,%s,%s]" % (edges['From'][i], edges['To'][i],k))
s = {}
for i in range(1, max(edges['From']+1)):
    for k in range(1, maxdrones + 1):
        s[i,k] = model.addVar(lb=0,ub=K,vtype=GRB.INTEGER,name="s[%s,%s]"%(i,k))
model.update()

###################
### CONSTRAINTS ###
###################
#print(len(edges) - 1)
#print(edges['From'][len(edges) - 1])
#print(range(1, edges['From'][len(edges) - 1]))
for i in range(1, maxnode):
    #print("Node",i)
    idx_this_node_out = np.where(edges['From'] == i)[0]
    idx_this_node_in = np.where(edges['To'] == i)[0]
    thisLHS = LinExpr()
    for k in range(1, maxdrones + 1):
        for j in range(0, len(idx_this_node_out)):
            thisLHS += x[i, edges['To'][idx_this_node_out[j]],k]
            thisLHS -= x[edges['From'][idx_this_node_in[j]], i, k]
        model.addConstr(lhs=thisLHS, sense=GRB.EQUAL, rhs=0,name='node_flow_' + str(i)+"i"+str(k)+"k")
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
    model.addConstr(lhs=thisLHS, sense=GRB.LESS_EQUAL, rhs=maxpayload+1, name='drone_payload_' + str(k))
    model.addConstr(lhs=thisrangeLHS, sense=GRB.LESS_EQUAL, rhs=maxrange, name='drone_range_' + str(k))


thisLHS = LinExpr()
count = 0
for i in range(1, max(edges['From']+1)):
    for j in range (1, max(edges['From']+1)):
        #print(count)
        if i != j & j!=1:
            for k in range(1, maxdrones + 1):
                #can add here an if for impossible edges
                thisLHS= LinExpr()
                thisLHS= s[i,k]-s[j,k]+((edges['Distance'][count])*speed/60+takeofftime+landingtime+unloadingtime)-K*(1-x[i,j,k])#[i+j-1]#+K*(1-x[i,j])#+edges['Distance'][1]

                model.addConstr(lhs=thisLHS, sense = GRB.LESS_EQUAL, rhs=0, name='time_' + str(i)+"i"+str(j)+"j"+str(k)+"k")
            count = count + 1


model.update()
obj = LinExpr()
count=0
for i in range(1, maxnode):
    for j in range(1,maxnode):
        if i != j:
            for k in range(1, maxdrones + 1):
                obj += edges['Distance'][count] * x[i,j,k]*costperkm #+ s[i,k]
            count += 1
for k in range(1,maxdrones+1):
    obj += xk[k]*droneFC



model.setObjective(obj, GRB.MINIMIZE)
model.update()
model.write('model_formulation2.lp')
print("------STARTING OPTIMIZATION--------")
model.optimize()
endTime = time.time()

fullsolution = []
solution = []
for v in model.getVars():
    fullsolution.append([v.varName, v.x])
    if v.x==1:
        solution.append([v.varName])
    #if v.xk==1:
    #    activedrones.append([v.varName])
print(solution)
print(fullsolution)

def solution_to_excel(solution):

    solution_df = pd.DataFrame(columns=["From", "To", "Drone"])

    for edge in solution:
        if str(edge[0][:2]) != 'xk':
            i_clean = edge[0][2:-1].split(",")
            from_node = i_clean[0]
            to_node = i_clean[1]
            drone_id = i_clean[2]
            solution_df.loc[-1] = [from_node, to_node, drone_id]
            solution_df.index += 1
            solution_df = solution_df.sort_index()
            solution_df = solution_df.iloc[::-1]

    solution_df.to_excel(cwd + "\database\solution.xlsx", 'data')


#Comment out because not working

#do_plot()
#solution_to_excel(solution)




