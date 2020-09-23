import sys
sys.path.append('.')
import numpy as np
from functions.Voltages import Voltages
from numpy import sin, cos, pi
import os
import matplotlib.pyplot as plt
plt.rc('font',family='Arial',size=8)

sigmaXX=0.6
sigmaYY=0.083
sigmaZZ=0.083

f1 = 1000+100 # Hz, stimulus frequency
f2 = 1000 # Hz, stimulus frequency

fs = 1000*50*4  # Hz, sampling rate

I = 1.  # current source amplitude in A

x = -7.5e-3
y = 0.0e-3
z = 0

X, Y, Z = np.meshgrid(x, y, z)

VS1s=Voltages(X,Y,Z,-5e-3,+5e-3,+0e-3,+I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS2s=Voltages(X,Y,Z,+5e-3,+5e-3,+0e-3,-I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS3s=Voltages(X,Y,Z,-5e-3,-5e-3,+0e-3,+I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS4s=Voltages(X,Y,Z,+5e-3,-5e-3,+0e-3,-I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')

V1=VS1s['V']+VS2s['V']

V2=VS3s['V']+VS4s['V']


fig,ax=plt.subplots(num=0,figsize=(5,3))
DF=100
f1 = 1000+DF # Hz, stimulus frequency
f2 = 1000 # Hz, stimulus frequency

fs = 1000*50*4  # Hz, sampling rate

N=1
Duration=1/DF*N
dt = 1/fs  # s, time step in simulations
t=np.arange(0,Duration,dt)

A1=np.squeeze(V1)
A2=np.squeeze(V2)

y1= A1*sin(2*pi*f1*t + 0)
y2= A2*sin(2*pi*f2*t + pi)



ax.plot(1000*t,y1,alpha=.95,linewidth=2.0,label=r'Pair$_1$',zorder=1)
ax.plot(1000*t,y2,alpha=.95,linewidth=2.0,label=r'Pair$_2$',zorder=0)
ax.plot(1000*t,y1+y2,alpha=0.95,linewidth=2.,label='Sum',zorder=-1)


ax.legend(bbox_to_anchor=(0.88,0), loc="lower right", 
                bbox_transform=fig.transFigure, ncol=3,frameon=False)

plt.axis('off')

plt.show()