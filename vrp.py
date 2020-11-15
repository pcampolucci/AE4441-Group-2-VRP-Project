
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

DEBUG = False

# Get path to current folder
cwd = os.getcwd()
print(cwd)
# Get all instances
full_list = os.listdir(cwd)

def optimise(base_id=[1,2]):

    ####-----MAC---------####

    instance_name = '/database/variables.xlsx'

    # Load data for this instance
    edges = pd.read_excel(cwd + instance_name, sheet_name='data')
    print("edges", edges)

    ###------Model options------###
    # droneFC=5            # Drone fixed cost
    # K=300                # Time upperbound
    # custumerdemand=1     # Number of blood bags required by the hospitals
    # maxpayload=5         # Maximum numbers of blood bags the drone can carry
    # costperkm=0.5        # Run cost of drone [€/km]
    # maxdrones=10         # Maximum number of drones
    # maxrange=800         # Maximum range of the drone [km]
    # speed=150            # Cruise speed of the drone [km/h]
    # takeofftime=2        # Time to complete take-off [min]
    # landingtime=2        # Time to complete landing [min]
    # unloadingtime=5      # Time to unload payload [min]
    # depots = base_id     # Number and Name of depots (base) - Must be in ascending order
    # priorityweight = 1   # Weighting factor of the priority objective
    #
    droneFC=1            # Drone fixed cost
    K=1000                # Time upperbound
    custumerdemand=1     # Number of blood bags required by the hospitals
    maxpayload=4        # Maximum numbers of blood bags the drone can carry
    costperkm=1        # Run cost of drone [€/km]
    maxdrones=5         # Maximum number of drones
    maxrange=11         # Maximum range of the drone [km]
    speed=1            # Cruise speed of the drone [km/h]
    takeofftime=0        # Time to complete take-off [min]
    landingtime=0        # Time to complete landing [min]
    unloadingtime=0      # Time to unload payload [min]
    depots = base_id     # Number and Name of depots (base) - Must be in ascending order
    priorityweight = 0   # Weighting factor of the priority objective

    startTimeSetUp = time.time()
    model = Model()
    maxnode = max(edges['From']+1)
    ####################-----VARIABLES-----####################

    ######---Generate drone and edges variables xk and x------######
    xk = {}
    x = {}
    for k in range(1,maxdrones+1):
        for base in depots:
            xk[k,base] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY,name="xk[%s,%s]" % (k,base))
        for i in range(0, len(edges)):
            x[edges['From'][i], edges['To'][i],k] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY,name="x[%s,%s,%s]" % (edges['From'][i], edges['To'][i],k))

    ######---Generate time variable s ------######
    s = {}
    for i in range(1, max(edges['From']+1)):
        for k in range(1, maxdrones + 1):
            s[i,k] = model.addVar(lb=0,ub=K,vtype=GRB.CONTINUOUS,name="s[%s,%s]"%(i,k))
    model.update()

    ###################### CONSTRAINTS ######################

    ####----Flow and Travelling salesman constraint-----#######
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
        thisLHS = LinExpr()
        if i > max(depots):
            for j in range(0, len(idx_this_node_out)):
                for k in range(1, maxdrones + 1):
                    thisLHS += x[i, edges['To'][idx_this_node_out[j]],k]
            model.addConstr(lhs=thisLHS, sense=GRB.EQUAL, rhs=1, name='node_out_' + str(i))

    ####----Drone payload and range constraint----#####
    for k in range(1, maxdrones + 1):
        thisLHS = LinExpr()
        thisrangeLHS = LinExpr()
        count=0
        for i in range(1, max(edges['From'] + 1)):
            for j in range(1, max(edges['From'] + 1)):
                if j != i:
                    thisLHS+= x[i,j,k]
                    thisrangeLHS+= x[i,j,k]*edges['Distance'][count]*(1 + edges['DeltaV'][count]/speed)
                    count += 1
        thisLHS = thisLHS*custumerdemand
        model.addConstr(lhs=thisLHS, sense=GRB.LESS_EQUAL, rhs=maxpayload+1, name='drone_payload_' + str(k))
        model.addConstr(lhs=thisrangeLHS, sense=GRB.LESS_EQUAL, rhs=maxrange, name='drone_range_' + str(k))

    ####----Multi base constraint----######
    for k in range(1, maxdrones + 1):
        thisLHS1 = LinExpr()
        thisLHS2 = LinExpr()
        thisLHSunique = LinExpr()
        for base in depots:
            for i in range(max(depots)+1, max(edges['From'] + 1)):
                thisLHS1 += x[base, i, k]
                thisLHS2 += x[i, base, k]
            thisLHS1 -= xk[k,base]
            thisLHS2 -= xk[k,base]
            model.addConstr(lhs=thisLHS1, sense=GRB.EQUAL, rhs=0, name='drone'+ str(k)+'out_base_' + str(base))
            model.addConstr(lhs=thisLHS2, sense=GRB.EQUAL, rhs=0, name='drone'+ str(k)+'in_base_' + str(base))
            thisLHSunique += xk[k,base]
        model.addConstr(lhs=thisLHSunique, sense=GRB.LESS_EQUAL, rhs=1, name='drone' + str(k) + 'only_in_one_base_')

    ####----Time constraints to avoid inner loops-----####
    thisLHS = LinExpr()
    count = 0
    for i in range(1, max(edges['From']+1)):
        for j in range (1, max(edges['From']+1)):
            #print(count)
            if i != j & j not in depots:
                for k in range(1, maxdrones + 1):
                    #can add here an if for impossible edges
                    thisLHS= LinExpr()
                    thisLHS= s[i,k]-s[j,k]+((edges['Distance'][count])/(speed+edges['DeltaV'][count])*60+takeofftime+landingtime+unloadingtime)-K*(1-x[i,j,k])#[i+j-1]#+K*(1-x[i,j])#+edges['Distance'][1]
                    model.addConstr(lhs=thisLHS, sense = GRB.LESS_EQUAL, rhs=0, name='time_' + str(i)+"i"+str(j)+"j"+str(k)+"k")
                count = count + 1
    model.update()

    #####----Object function setting-----#####
    obj = LinExpr()
    count=0
    for i in range(1, maxnode):
        for j in range(1,maxnode):
            if i != j:
                for k in range(1, maxdrones + 1):
                    obj += edges['Distance'][count] * x[i,j,k]*costperkm #+ s[i,k]
                count += 1
    for k in range(1,maxdrones+1):
        for i in range(max(depots)+1,maxnode):
            obj += s[i,k]*edges['Priority'][np.where(edges['From']== i)[0][1]]*priorityweight
        for base in depots:
            obj += xk[k,base]*droneFC

    model.setObjective(obj, GRB.MINIMIZE)
    model.update()
    model.write('LPSolve\model_formulation2.lp')

    ####-----Start of optimization process-----#####
    print("------STARTING OPTIMIZATION--------")
    model.optimize()
    endTime = time.time()

    fullsolution = []
    solution = []
    for v in model.getVars():
        fullsolution.append([v.varName, v.x])
        if v.x!=0:
            solution.append([v.varName])
    print(solution)

    return solution

######-----Post ptocessing of solution------######
def solution_to_excel(ismac,solution):

    solution_df = pd.DataFrame(columns=["From", "To", "Drone"])
    if ismac:
        solution_path = "/database/solution.xlsx"
    else:
        solution_path = "\database\solution.xlsx"


    for edge in solution:
        if str(edge[0][:2]) != 'xk':
            if str(edge[0][:1]) != 's':
                i_clean = edge[0][2:-1].split(",")
                from_node = i_clean[0]
                to_node = i_clean[1]
                drone_id = i_clean[2]
                solution_df.loc[-1] = [from_node, to_node, drone_id]
                solution_df.index += 1
                solution_df = solution_df.sort_index()
                solution_df = solution_df.iloc[::-1]

    solution_df.to_excel(cwd + solution_path, 'data')
    #print(f"Solution written to {cwd + solution_path}")


if DEBUG:
    debug_solution = optimise()
    solution_to_excel(debug_solution)

#######-------Archive---------##########

#Variables:

# xij = {}
# for i in range(1,maxnode):
#     for j in range(1,maxnode):
#         if i != j:
#             xij[i,j] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY, name="xij[%s,%s]"%(i,j))

#Constraints:
  # if len(idx_this_node_in) > 0:
    #     for j in range(0, len(idx_this_node_in)):
    #         for k in range(1, maxdrones + 1):
    #             thisLHS -= x[edges['From'][idx_this_node_in[j]], i,k]
    # model.addConstr(lhs=thisLHS, sense=GRB.EQUAL, rhs=0,
    #                     name='node_flow_' + str(i))

#Objective Function:

# for i in range(1, maxnode):
#     for j in range(1,maxnode):
#         if i != j:
#             obj += edges['Distance'][count] * xij[i,j]*costperkm #+ s[i,k]
#             count += 1
# for k in range(1,maxdrones+1):
#     obj += xk[k]*droneFC

#print(len(edges) - 1)
#print(edges['From'][len(edges) - 1])
#print(range(1, edges['From'][len(edges) - 1]))