"""
author: tmldeponti
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def simpleplot():
    # Get path to current folder
    cwd = os.getcwd()
    print(cwd)
    # Get all instances
    full_list = os.listdir(cwd)
    ####-----MAC---------####
    instance_name = '/database/variables.xlsx'
    # Load data for this instance
    edges = pd.read_excel(cwd + instance_name, sheet_name='data')
    print("edges", edges)
    instance_name = '/database/solution.xlsx'
    sol = pd.read_excel(cwd + instance_name, sheet_name='data')
    print("solution", sol)
    instance_name = '/database/validation.xlsx'
    coord = pd.read_excel(cwd + instance_name, sheet_name='Sheet1')
    xc = coord['lat'][:]*111
    yc = coord['long'][:]*111
    ids = coord['id']
    #coord['lat'][:]=coord['lat'][:]*111
    #coord['long'][:]=coord['long'][:]*111
    print("coord",coord)
    print("coord", xc,yc)
    colors = ['red','blue','orange','green','pink','purple']

    plt.plot(xc[np.where(coord['type']=='base')[0]],yc[np.where(coord['type']=='base')[0]],'s',color='black')
    plt.plot(xc[np.where(coord['type']=='hospital')[0]],yc[np.where(coord['type']=='hospital')[0]],'o',color='black',fillstyle='none')
    #plt.annotate(s=ids,xy=[xc,yc],textcoords="offset points",xytext=(0,10), ha='center')
    for i in range(max(ids)):
        plt.annotate(s=ids[i],xy=[xc[i],yc[i]],textcoords="offset points",xytext=(-15,5), ha='center',fontsize=15,weight='bold')
    for j in range(0,len(sol)):
        x1=float(xc[np.where(coord['id']==sol['From'][j])[0]])
        print('x1',x1)
        y1=float(yc[np.where(coord['id']==sol['From'][j])[0]])
        print('y1', y1)
        x2=float(xc[np.where(coord['id']==sol['To'][j])[0]])
        print('x2', x2)
        y2=float(yc[np.where(coord['id']==sol['To'][j])[0]])
        print('y2', y2)
        print('values',x1,y1,x2-x1,y2-y1)
        plt.arrow(x1,y1,x2-x1,y2-y1,color=colors[sol['Drone'][j]],width=0.01,shape='full',length_includes_head=True,head_width=0.1)
        dis=round(float(edges['Distance'][(edges['From']==sol['From'][j])&(edges['To']==sol['To'][j])]),2)
        dis="("+str(dis)+")"
        plt.annotate(s=dis,xy=[(x2+x1)/2-0.3,(y2+y1)/2],textcoords="offset points",xytext=(0,5), ha='center')
    plt.xlabel("x [km]")
    plt.ylabel("y [km]")
    plt.xlim(-5.5, 1.2)
    plt.ylim(-1.2, 1.2)
    plt.grid(b=None, which='major', axis='both')
    plt.show()

