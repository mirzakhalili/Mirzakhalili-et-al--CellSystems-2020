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

f1 = 1000+100 
f2 = 1000 

fs = 1000*50*4  

I = 1.  

x = 7.5e-3
y = -1e-3
z = 0

X, Y, Z = np.meshgrid(x, y, z)

VS1s=Voltages(X,Y,Z,-5e-3,+5e-3,+0e-3,+I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS2s=Voltages(X,Y,Z,+5e-3,+5e-3,+0e-3,-I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS3s=Voltages(X,Y,Z,-5e-3,-5e-3,+0e-3,+I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS4s=Voltages(X,Y,Z,+5e-3,-5e-3,+0e-3,-I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')

V1=VS1s['V']+VS2s['V']

V2=VS3s['V']+VS4s['V']

fig,ax=plt.subplots(num=0,figsize=(4,3))

f1 = 1000+100 
f2 = 1000 

fs = 1000*50*4  

N=2
Phase=0.

time_duration = (N+(0+Phase)/2.0)/(f1-f2) 
stim_duration = (N+(0+Phase)/2.0)/(f1-f2)  

dt = 1/fs  
t=np.arange(0,time_duration,dt)

A1=np.squeeze(V1)
A2=np.squeeze(V2)

y1= A1*sin(2*pi*f1*t + 0)
y2= A2*sin(2*pi*f2*t + pi)

y3=np.sqrt(A1**2+A2**2+2*A1*A2*cos(2*pi*(f1-f2)*t-pi))

ax.plot(1000*t,y3,alpha=1.0,linewidth=2,label='Envelope')
ax.plot(1000*t,y1+y2,alpha=0.95,linewidth=2,label='Sum',zorder=-100)

ax.legend(bbox_to_anchor=(0.88,0), loc="lower right", 
                bbox_transform=fig.transFigure, ncol=3,frameon=False)

plt.axis('off')

plt.show()