import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
sys.path.append('.')
import numpy as np
import os
import time
import pickle


cmap = plt.cm.get_cmap('Blues_r')
Factor=1.2
ColorS='k'
ColorB='tab:red'
ColorP=cmap(0.5)
ColorT=cmap(0.8)
MaxAP=10*10*5

fig,ax=plt.subplots(num=0)

f2 = 2000 # Hz, stimulus frequency
F=5
f1 = f2+F  # Hz, stimulus frequency

# N0=10
N=10
Phase=1
delay = 20.0e-3  # s, delay for starting stimulation, allows the neuron simulation to "settle"

Cycle=1/(f1-f2)*1000

ZZ=0e-3

Scale=1


Y=np.arange(-4e-3,4.1e-3,0.1e-3)

H=0.1
W=0.4
dX=1.5*W
XPT=np.arange(3)*dX-W/2

Freq=2000
DFreq=5
for YY in Y:
    fname='./APs,{:.2f},{:.2f},{:.0f},{:.6f}.p'.format(Freq,DFreq,10,YY*1000)
    with open(fname, 'rb') as fp:
        data = pickle.load(fp)

    APTs=[]
    MaxAPCount=0
    for key in data:
        if 'node' in key:
            temp=data[key].to_python()
            if len(temp)>MaxAPCount:
                MaxAPCount=len(temp)
            APTs.append(temp)
    
    Node0=APTs[-1]
    Node0 = np.asarray(Node0)
    Mask = np.ones(len(Node0), dtype=bool)
    Mask[Node0<Cycle/2+Cycle]=False
    Mask[Node0>N*Cycle+Cycle/2-Cycle]=False
    Node0=Node0[Mask]

    if len(Node0)==0:
        
        fname='./APs,{:.2f},{:.2f},{:.0f},{:.6f}.p'.format(Freq,DFreq,10,YY*1000)

        with open(fname, 'rb') as fp:
            data = pickle.load(fp)

        APTs=[]
        MaxAPCount=0
        for key in data:
            if 'node' in key:
                temp=data[key].to_python()
                if len(temp)>MaxAPCount:
                    MaxAPCount=len(temp)
                APTs.append(temp)
        
        Node0=APTs[99]
        Node0 = np.asarray(Node0)
        Mask = np.ones(len(Node0), dtype=bool)
        Mask[Node0<2.5*Cycle]=False
        Mask[Node0>3.5*Cycle]=False
        Node0=Node0[Mask]
        if len(Node0)==0:
            #Block
            rect = Rectangle((XPT[0],YY*1000-H/2), width=W, height=H,alpha=1.0,fill=True,color=ColorB,linewidth=0)
            ax.add_patch(rect)
            # rect.set_edgecolor("black")
        else:
            #Silent
            rect = Rectangle((XPT[0],YY*1000-H/2), width=W, height=H,alpha=1.0,fill=True,color=ColorS,linewidth=0)
            ax.add_patch(rect)
            # rect.set_edgecolor("black")


    else:
        Rate=len(Node0)/2/Factor/MaxAP+1/2/Factor
        if Rate>1/Factor:
            Rate=1/Factor

        rect = Rectangle((XPT[0],YY*1000-H/2), width=W, height=H,alpha=1.0,fill=True,color=cmap(Rate),linewidth=0)
        ax.add_patch(rect)

rect = Rectangle((XPT[0],-4-H/2), width=W, height=8+H,alpha=1.0,fill=False,linewidth=0.75)
rect.set_edgecolor("black")
ax.add_patch(rect)
ax.axis('scaled')
ax.set_frame_on(False)

ax.xaxis.set_ticks_position('none') 
ax.set_ylabel('Axon distance from midline [mm]',fontsize=10)
ax.tick_params(axis='x', pad=-10)
plt.xticks([])
plt.yticks([-4,-3,-2,-1,0,1,2,3,4])
plt.show()