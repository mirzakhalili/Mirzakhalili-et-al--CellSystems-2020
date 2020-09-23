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
N=4

Cycle=1/(f1-f2)*1000

fname='.\SubThreshold\Vs,1000.00,20.00-TI.p'
with open(fname, 'rb') as fp:
    MyCell = pickle.load(fp)


MyV=MyCell['node[45](0.5).v']
MyT = MyCell['t']
MyT=np.asarray(MyT.to_python())
MyV=np.asarray(MyV.to_python())


fig,ax=plt.subplots(num=0)
plt.plot(MyT,MyV,alpha=0.95,linewidth=0.35)

vv=[]
peaks, _ = find_peaks(MyV,distance=fs/1000)
vv.append(MyV[peaks[0]-1])
for i in range(1,len(peaks)):
    temp=np.mean(MyV[peaks[i-1]:peaks[i]])
    vv.append(temp)
plt.plot(MyT[peaks],vv,linewidth=1,alpha=0.75)

ax.set_frame_on(False)
plt.xticks([])
plt.yticks([])
plt.xlim([(N-2.5)*Cycle,(N-0.5)*Cycle])
plt.ylim([-95,-65])
plt.show()