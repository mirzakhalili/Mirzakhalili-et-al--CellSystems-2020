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

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

fig,ax=plt.subplots(num=0)

f1 = 1000+20
f2 = 1000 

fs = 1000*50*4  

N=100
Phase=0.

time_duration = (N+(0+Phase)/2.0)/(f1-f2)  
stim_duration = (N+(0+Phase)/2.0)/(f1-f2)  

dt = 1/fs  
t=np.arange(0,time_duration,dt)

A1=1
A2=1

y1= A1*sin(2*pi*f1*t + 0)
y2= A2*sin(2*pi*f2*t + 0)
yS=y1+y2

cutoff=1000
order=8
b, a = butter_lowpass(cutoff, fs, order)
yFA = butter_lowpass_filter(np.abs(yS), cutoff, fs, order)



L=len(t)
freqs = fs*np.arange(0,L/2+1)/L
pS = np.abs(np.fft.fft(yS)/L)
pS=2*pS[0:int(L/2)+1]



pFA = np.abs(np.fft.fft(yFA)/L)
pFA=2*pFA[0:int(L/2)+1]



labels=['20','1000','1020']
PS=[pS[freqs==20][0]/np.max(pS),pS[freqs==1000][0]/np.max(pS),pS[freqs==1020][0]/np.max(pS)]
PFA=[pFA[freqs==20][0]/np.max(pS),pFA[freqs==1000][0]/np.max(pS),pFA[freqs==1020][0]/np.max(pS)]


x = np.arange(len(labels)) 
width = 0.5  

rects2 = ax.bar(x , PFA, width)

plt.xlabel('Frequency [Hz]')


ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.yticks([0,1])
ax.set_xticklabels([0,1])
ax.set_xticks(x)
ax.set_xticklabels(labels)

plt.ylabel('|Normalized power|',labelpad =2)
plt.ylim([0,1])
ax.xaxis.set_ticks_position('none') 

plt.show()