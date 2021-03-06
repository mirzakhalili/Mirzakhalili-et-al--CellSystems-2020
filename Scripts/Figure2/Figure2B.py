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

t0=5.25/f1
I1=sin(2*pi*f1*t0 +0)
I2=sin(2*pi*f2*t0 +np.pi)

I = 1. 

x = np.arange(-10e-3, 10e-3+1e-5, 5e-5)
y = np.arange(-5e-3,  5e-3+1e-5, 5e-5)
z = np.arange(-1e-3,  1e-3+1e-5, 1e-4)

X, Y, Z = np.meshgrid(x, y, z)

VS1s=Voltages(X,Y,Z,-5e-3,+5e-3,+0e-3,+I1,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS2s=Voltages(X,Y,Z,+5e-3,+5e-3,+0e-3,-I1,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS3s=Voltages(X,Y,Z,-5e-3,-5e-3,+0e-3,+I2,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS4s=Voltages(X,Y,Z,+5e-3,-5e-3,+0e-3,-I2,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')

V1=VS1s['V']+VS2s['V']

V2=VS3s['V']+VS4s['V']

Venv=np.abs(np.abs(V1+V2)-np.abs(V1-V2))

fig,ax=plt.subplots(num=0,figsize=(5,4),constrained_layout=True)

temp=np.abs(z-0)
indZ=np.argmin(temp)

temp=V2[:,:,indZ]+V1[:,:,indZ]

temp[temp>=200]=200
temp[temp<=-200]=-200
cax=ax.contourf(X[:,:,indZ]*1000,Y[:,:,indZ]*1000,temp,np.arange(-200,201,10),antialiased=True)
cbar=fig.colorbar(cax, pad=0.0,format='%2.0f',location='left',shrink=0.55,ticks=[-200, 0, 200])
cbar.ax.set_title(r'Volts',fontsize=10)
plt.setp(cax.collections, edgecolors='face')

tempX=VS1s['Vx']+VS2s['Vx']+VS3s['Vx']+VS4s['Vx']
tempY=VS1s['Vy']+VS2s['Vy']+VS3s['Vy']+VS4s['Vy']

EX=-tempX[:,:,indZ]
EY=-tempY[:,:,indZ]
Mag=np.sqrt(EX**2+EY**2)
EX=EX/Mag*np.log10(Mag)
EY=EY/Mag*np.log10(Mag)

x = np.arange(-10e-3, 10e-3+1e-5, 5e-5)
y = np.arange(-5e-3,  5e-3+1e-5, 5e-5)
z = np.arange(-1e-3,  1e-3+1e-5, 1e-4)

X, Y, Z = np.meshgrid(x, y, z)
SkipX=10
SkipY=20

XPick1=X[SkipX:int(len(y)/2):SkipX,SkipY:-1:SkipY,indZ]
YPick1=Y[SkipX:int(len(y)/2):SkipX,SkipY:-1:SkipY,indZ]
ExPick1=EX[SkipX:int(len(y)/2):SkipX,SkipY:-1:SkipY]
EyPick1=EY[SkipX:int(len(y)/2):SkipX,SkipY:-1:SkipY]

XPick2=X[int(len(y)/2)+SkipX:-1:SkipX,SkipY:-1:SkipY,indZ]
YPick2=Y[int(len(y)/2)+SkipX:-1:SkipX,SkipY:-1:SkipY,indZ]
ExPick2=EX[int(len(y)/2)+SkipX:-1:SkipX,SkipY:-1:SkipY]
EyPick2=EY[int(len(y)/2)+SkipX:-1:SkipX,SkipY:-1:SkipY]

XPick3=X[int(len(y)/2),int(SkipY*1.5):-1:SkipY,indZ]
YPick3=Y[int(len(y)/2),int(SkipY*1.5):-1:SkipY,indZ]
ExPick3=EX[int(len(y)/2),int(SkipY*1.5):-1:SkipY]
EyPick3=EY[int(len(y)/2),int(SkipY*1.5):-1:SkipY]

XPick1=np.append(XPick1,XPick2)
YPick1=np.append(YPick1,YPick2)

ExPick1=np.append(ExPick1,ExPick2)
EyPick1=np.append(EyPick1,EyPick2)

XPick1=np.append(XPick1,XPick3)
YPick1=np.append(YPick1,YPick3)

ExPick1=np.append(ExPick1,ExPick3)
EyPick1=np.append(EyPick1,EyPick3)
Qax=ax.quiver(XPick1*1000,YPick1*1000,ExPick1,EyPick1,color='w',alpha=0.8,scale=200,pivot='mid',headlength=4.25,zorder=100)

plt.axis('off')
ax.axis('scaled')

plt.xlim([-10,10])

plt.show()