"""
author: tmldeponti
"""
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import os
import math





# Get path to current folder
cwd = os.getcwd()
print(cwd)
# Get all instances
full_list = os.listdir(cwd)
colors = ['red','blue','orange','green','pink','purple']

xc = [0,1]
yc = [0,1]
ids = [1,2]
r = 0.3
[x0,y0]=[0,0]

plt.plot(xc[0],yc[0],'s',color='black')
plt.plot(xc[1],yc[1],'o',color='black',fillstyle='none')
#plt.annotate(s=ids,xy=[xc,yc],textcoords="offset points",xytext=(0,10), ha='center')
for i in range(max(ids)):
    plt.annotate(s=ids[i],xy=[xc[i],yc[i]],textcoords="offset points",xytext=(xc[i]*4*-1+6,yc[i]*3+8), ha='center',fontsize=15,weight='bold')
lenghtwind=0.7
anglehorizon=-90
dxc= lenghtwind * np.cos(anglehorizon*np.pi/180.)
dyc= lenghtwind * np.sin(anglehorizon*np.pi/180.)
print(dxc,dyc)
plt.arrow(xc[1],yc[1],dxc,dyc,color=colors[1],width=0.01,shape='full',length_includes_head=True,head_width=0.05)
plt.annotate(s="wind",xy=[(xc[1]+dxc)+0.1,(yc[1]+dyc)+0.3],textcoords="offset points",xytext=[(xc[1]+dxc)+2,(yc[1]+dyc)+2], ha='center',fontsize=15,weight='bold',color=colors[1])
plt.plot(xc,yc,linestyle= '--', color = 'black')

angleroute = np.arctan((yc[1]-yc[0])/(xc[1]-xc[0]))
lengpar= lenghtwind * np.sin(angleroute)
lengperp= lenghtwind * np.cos(angleroute)
dxcpar= lengpar * np.sin(angleroute+np.pi)
dycpar= lengpar * np.cos(angleroute+np.pi)
dxcperp= lengpar * np.cos(angleroute-0.5*np.pi)
dycperp= lengpar * np.sin(angleroute-0.5*np.pi)
alpha = np.linspace(0,angleroute,1000)
x1 = r * np.cos(alpha)+x0
x2 = r * np.sin(alpha)+y0
r2 = r+0.05
x12 = r2 * np.cos(alpha)+x0
x22 = r2 * np.sin(alpha)+y0
plt.arrow(xc[1],yc[1],dxcpar,dycpar,color=colors[0],width=0.01,shape='full',length_includes_head=True,head_width=0.05)
plt.arrow(xc[1],yc[1],dxcperp,dycperp,color=colors[0],width=0.01,shape='full',length_includes_head=True,head_width=0.05)
plt.annotate(s="wind$\perp$",xy=[(xc[1]+dxcperp),(yc[1]+dycperp)],textcoords="offset points",xytext=[(xc[1]+dxcperp),(yc[1]+dycperp)+30], ha='center',fontsize=15,weight='bold',color=colors[0])
plt.annotate(s="wind$\parallel$",xy=[(xc[1]+dxcpar),(yc[1]+dycpar)],textcoords="offset points",xytext=[(xc[1]+dxcpar)+2,(yc[1]+dycpar)+30], ha='center',fontsize=15,weight='bold',color=colors[0])
plt.plot(x1,x2,color=colors[0])
plt.plot(x12,x22,color=colors[0])
plt.annotate(s=r'$\alpha$',xy=[0.43,0.17],textcoords="offset points",xytext=[0.35,0.17], ha='center',fontsize=22,weight='bold',color=colors[0])


plt.xlabel("x [km]")
plt.ylabel("y [km]")
plt.xlim(0, 1.5)
plt.ylim(0, 1.5)
plt.gca().set_aspect('equal',adjustable='box')
#plt.xlim(-5.5, 5.5)
#plt.ylim(-4, 4)
plt.grid(b=None, which='major', axis='both')
plt.show()
