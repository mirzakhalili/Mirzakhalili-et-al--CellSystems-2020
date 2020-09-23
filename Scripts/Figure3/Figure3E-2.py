import sys
from neuron import h
from scipy.signal import find_peaks
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt

h.load_file('stdrun.hoc')

f1 = 1000+20
f2 = 1000 

fs = 1000*50  # Hz, sampling rate
N=100

Cycle=1/(f1-f2)*1000

fname='.\SubThreshold\Vs,1000.00,20.00-TI.p'
with open(fname, 'rb') as fp:
    MyCell = pickle.load(fp)


MyV=MyCell['node[45](0.5).v']
MyT = MyCell['t']
MyTT=np.asarray(MyT.to_python())
MyVT=np.asarray(MyV.to_python())

fname='.\SubThreshold\Vs,1000.00,20.00-Passive.p'
with open(fname, 'rb') as fp:
    MyCell = pickle.load(fp)


MyV=MyCell['node[45](0.5).v']
MyT = MyCell['t']
MyTP=np.asarray(MyT.to_python())
MyVP=np.asarray(MyV.to_python())


Mask = np.ones(len(MyTT), dtype=bool)
Mask[MyTT<2.5*Cycle]=False
Mask[MyTT>N*Cycle+0.5*Cycle]=False
MyTT=MyTT[Mask]
MyVT=MyVT[Mask]
L=len(MyTT)
freqs = fs*np.arange(0,L/2+1)/L
pT = np.abs(np.fft.fft(MyVT)/L)
pT=2*pT[0:int(L/2)+2]

Mask = np.ones(len(MyTP), dtype=bool)
Mask[MyTP<2.5*Cycle]=False
Mask[MyTP>N*Cycle+0.5*Cycle]=False
MyTP=MyTP[Mask]
MyVP=MyVP[Mask]

L=len(MyTP)
freqs = fs*np.arange(0,L/2+2)/L
pP = np.abs(np.fft.fft(MyVP)/L)
pP=2*pP[0:int(L/2)+2]



fig,ax=plt.subplots(num=0)

Norm=pT[np.argmin(np.abs(freqs-1000))]

labels=['20','1000','1020']

PP=[pT[freqs==20][0]/Norm,pT[freqs==1000][0]/Norm,pT[freqs==1020][0]/Norm]


x = np.arange(len(labels))
width = 0.5

rects2 = ax.bar(x , PP, width)

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