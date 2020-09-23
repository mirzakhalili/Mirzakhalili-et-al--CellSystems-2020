import sys
from neuron import h
from scipy.signal import find_peaks
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt

h.load_file('stdrun.hoc')


f1 = 1000+20# Hz, stimulus frequency
f2 = 1000 # Hz, stimulus frequency

fs = 1000*50  # Hz, sampling rate
N=4

Cycle=1/(f1-f2)*1000
# variable = {'v','m_newaxnode','mp_newaxnode','h_newaxnode','s_newaxnode','inap_newaxnode','ina_newaxnode','ik_newaxnode','il_newaxnode'}
fname='E:\HPC\TI\Results\D87\Sym\LongRuns\SubThreshold\Vs,1000.00,20.00-TI.p'
with open(fname, 'rb') as fp:
    MyCell = pickle.load(fp)

fig,ax=plt.subplots(num=0)

X = MyCell['t']
X=np.asarray(X.to_python())

Y1=MyCell['node[45](0.5).ina_newaxnode']
Y1=np.asarray(Y1.to_python())
plt.plot(X,Y1,alpha=0.95,linewidth=0.35)

Y2=MyCell['node[45](0.5).inap_newaxnode']
Y2=np.asarray(Y2.to_python())
plt.plot(X,Y2,alpha=0.95,linewidth=0.35)

Y3=MyCell['node[45](0.5).ik_newaxnode']
Y3=np.asarray(Y3.to_python())
plt.plot(X,Y3,alpha=0.95,linewidth=0.35)

Y4=MyCell['node[45](0.5).il_newaxnode']
Y4=np.asarray(Y4.to_python())
plt.plot(X,Y4,alpha=0.95,linewidth=0.35)
plt.plot(X,Y1+Y2+Y3+Y4,alpha=0.95,linewidth=0.35)

ax.set_frame_on(False)
plt.xticks([])
plt.yticks([])
plt.xlim([(N-1.5)*Cycle,(N-0.5)*Cycle])
plt.show()