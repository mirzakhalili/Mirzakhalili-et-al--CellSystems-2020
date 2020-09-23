import sys
sys.path.append('.')
import numpy as np
from functions.Voltages import Voltages
from numpy import sin, cos, pi
import os
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

x = 5e-3
y = 0.0e-3
z = 0
sigmaXX=0.6
sigmaYY=0.083
sigmaZZ=0.083
I=4e-3

X, Y, Z = np.meshgrid(x, y, z)

VS1s=Voltages(X,Y,Z,-5e-3,+5e-3,+0e-3,+I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS2s=Voltages(X,Y,Z,+5e-3,+5e-3,+0e-3,-I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS3s=Voltages(X,Y,Z,-5e-3,-5e-3,+0e-3,+I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS4s=Voltages(X,Y,Z,+5e-3,-5e-3,+0e-3,-I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')

V1=VS1s['V']+VS2s['V']

V2=VS3s['V']+VS4s['V']


fig,ax=plt.subplots(num=0)

f1 = 1000+20
f2 = 1000 

fs = 1000*50*4

N=4
Phase=0.

time_duration = (N+(0+Phase)/2.0)/(f1-f2)
stim_duration = (N+(0+Phase)/2.0)/(f1-f2)

dt = 1/fs
t=np.arange(0,time_duration,dt)

A1=np.squeeze(V1)
A2=np.squeeze(V2)

y1= A1*sin(2*pi*f1*t + 0)
y2= A2*sin(2*pi*f2*t + 0)
yS=y1+y2
cutoff=1000
order=8

yFA = butter_lowpass_filter(np.abs(yS), cutoff, fs, order)


ax.plot(1000*t,yFA,alpha=1,linewidth=2,label='Low-Pass(|Sum|)')



ax.set_frame_on(False)
plt.xticks([])
plt.yticks([])
Cycle=1000/(f1-f2)
plt.xlim([(N-2.5)*Cycle,(N-0.5)*Cycle])

plt.show()