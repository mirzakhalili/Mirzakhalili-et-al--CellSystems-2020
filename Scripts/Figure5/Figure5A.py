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

I1=1
I2=1

I = 1

x = np.arange(-10e-3, 10e-3+1e-5, 5e-5)
y = np.arange(-5e-3,  5e-3+1e-5, 5e-5)
z = np.arange(-1e-3,  1e-3+1e-5, 1e-4)

X, Y, Z = np.meshgrid(x, y, z)

VS1s=Voltages(X,Y,Z,-5e-3,+5e-3,+0e-3,+I1,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS2s=Voltages(X,Y,Z,+5e-3,+5e-3,+0e-3,-I1,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS3s=Voltages(X,Y,Z,-5e-3,-5e-3,+0e-3,+I2,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS4s=Voltages(X,Y,Z,+5e-3,-5e-3,+0e-3,-I2,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')

V1=VS1s['Vxx']+VS2s['Vxx']

V2=VS3s['Vxx']+VS4s['Vxx']

Venv=np.abs(np.abs(V1+V2)-np.abs(V1-V2))

fig,ax=plt.subplots(num=0,constrained_layout=True)

temp=np.abs(z-0)
indZ=np.argmin(temp)


temp=Venv[:,:,indZ]
temp=temp/np.max(temp)

cax=ax.contourf(X[:,:,indZ]*1000,Y[:,:,indZ]*1000,temp,np.arange(0,1.01,0.1),antialiased=True)
cbar=fig.colorbar(cax, pad=0.0,format='%2.0f',location='left',shrink=0.55,ticks=[0,1])


plt.setp(cax.collections, edgecolors='face')



plt.axis('off')
ax.axis('scaled')
plt.xlim([-10,10])
plt.show()