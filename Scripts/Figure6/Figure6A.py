import sys
import matplotlib.pyplot as plt
import numpy as np
import time
import pickle

fig,ax=plt.subplots(num=0)
plt.xlabel('Time [ms]')
Y1=np.arange(-4.0e-3,0,0.1e-3)
Y2=np.arange(0,4.01e-3,0.1e-3)
Y=np.append(Y1,Y2)
for YY in Y:
    ZZ=0
    fname='./APs,{:.2f},{:.2f},{:.0f},{:.6f}.p'.format(2000,5,10,YY*1000)
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

    temp=APTs[0]
    plt.plot(temp,np.ones(len(temp))*YY*1000,'.',color='c',markersize=1.5)
    
    plt.ylabel('Axon distance from midline [mm]')
Ymax=4.1
Ymin=-4.1
plt.ylim(Ymin,Ymax)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.xticks([0,600,1200,1800])
plt.yticks([-4,-3,-2,-1,0,1,2,3,4])
plt.show()