import sys
sys.path.append('.')
from neuron import h
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
from functions.Voltages import Voltages
from classes.Cell_rdg import MRG

MyTraj = np.array([[-50e-3, 0, 0], [51e-3, 0, 0]])
MyPath = os.getcwd() + '/'
CELL_DIR = MyPath+'cells/'
CELL_FILE_NAME = 'NewMRGaxon_for_Python.hoc'
MyD = 8.7
MyCell = MRG(axon_trajectory=MyTraj, fiberD=MyD,
             CELL_FILE_NAME=CELL_FILE_NAME, CELL_DIR=CELL_DIR)

MyPoints = list()
for sec in MyCell.get_secs():
    if ("node" in sec.name()):
        MyPoints.append(MyCell.center_3Dcoords(sec))

MyPoints = np.array(MyPoints)*1e-6 

NumNodes=len(MyPoints[:,0])
AllAPT=[]
AllAPL=[]
APTs=np.empty(0)
APLs=np.empty(0)

Ns=10

for F in range (1,51,1):
    for f2 in [1000,2000,4000]:
        for Ns in [10]:
            f1=f2+F
            NN=0
            APTs=np.empty(0)
            APLs=np.empty(0,dtype=int)
            fname='./Ths/APs,{:.2f},{:.2f},{:.0f}.p'.format(f2,F,Ns)
            with open(fname, 'rb') as fp:
                data = pickle.load(fp)
            for key in data:
                if 'node' in key:
                    temp=data[key].to_python()
                    if len(temp)>0:    
                        APTs=np.append(APTs,temp)
                        APLs=np.append(APLs,int(key[5:-1])*np.ones([len(temp),1]))

            if len(data['node[90]'].to_python())>0:

                Ind_APTs=np.argsort(APTs)

                S_APTs=APTs[Ind_APTs]
                S_APLs=APLs[Ind_APTs]
                S_APTsCopy=S_APTs
                S_APLsCopy=S_APLs
                APCount=0
                while len(S_APTs)>3:
                    CandidateT=S_APTs[0]
                    CandidateL=S_APLs[0]
                    S_APTs=np.delete(S_APTs,0)
                    S_APLs=np.delete(S_APLs,0)
                    Cycle=1/(f1-f2)*1000
                    if CandidateT>Cycle/2+NN*Cycle:
                
                        RightNode=CandidateL+1
                        
                        if RightNode<NumNodes-1:

                            indR=np.where(S_APLsCopy==RightNode)[0]

                            indRC=indR[np.argmin(np.abs(CandidateT-S_APTsCopy[indR]))]
                            RightTime=S_APTsCopy[indRC]
                            
                        else:
                            RightTime=-1

                        LeftNode=CandidateL-1

                        if LeftNode>0:

                            indL=np.where(S_APLsCopy==LeftNode)[0]

                            # Used[indL]+=1
                            indLC=indL[np.argmin(np.abs(CandidateT-S_APTsCopy[indL]))]
                            LeftTime=S_APTsCopy[indLC]
                            try:
                                S_APTs=np.delete(S_APTs,[indLC])
                                S_APLs=np.delete(S_APLs,[indLC])
                            except:
                                pass
                            
                        else:
                            LeftTime=-1


                        PassR=False
                        PassL=False
                        
                        if RightTime>CandidateT:

                            PassR=True
                            
                        elif RightTime==CandidateT:

                            indR2=np.where(S_APLsCopy==RightNode+1)[0]

                            RightTime2=S_APTsCopy[indR2[np.argmin(np.abs(CandidateT-S_APTsCopy[indR2]))]]

                            if LeftTime<RightTime2:

                                PassR=True
                            elif LeftTime==RightTime2:
                                PassR=True
                                CandidateL=CandidateL+0.5
                        if LeftTime>CandidateT:

                            PassL=True

                        elif LeftTime==CandidateT:

                            indL2=np.where(S_APLsCopy==LeftNode-1)[0]

                            LeftTime2=S_APTsCopy[indL2[np.argmin(np.abs(CandidateT-S_APTsCopy[indL2]))]]

                            if RightTime<LeftTime2:

                                PassL=True
                            elif LeftTime2==RightTime:
                                PassL=True
                                CandidateL=CandidateL-0.49

                        if PassR==True and PassL==True:
                            try:
                                S_APTs=np.delete(S_APTs,[indLC])
                                S_APLs=np.delete(S_APLs,[indLC])
                            except:
                                pass
                            try:
                                S_APTs=np.delete(S_APTs,[indRC])
                                S_APLs=np.delete(S_APLs,[indRC])
                            except:
                                pass

                            NN=NN+0
                            AllAPT.append(CandidateT)
                            AllAPL.append(CandidateL)
                            APCount+=1


            else:
                print(f1,f2,'No AP?')



dX=np.abs(MyPoints[1,0]-MyPoints[0,0])
Flat=-50+np.asfarray(AllAPL)*dX*1000
Bins=np.arange(MyPoints[0,0]-dX/2,MyPoints[-1,0]+dX,dX)*1000
fig,ax=plt.subplots(num=0)
n, x, _ = ax.hist(Flat,bins=Bins,histtype='bar', density=True,visible=True,color='r',alpha=0.95,linewidth=.3,align='mid',edgecolor='k')
plt.xlabel('Axon nodes x-coordinate [mm]')
plt.title(r'$AM_A$')
plt.yticks([0,0.4])
sigmaXX=0.6
sigmaYY=0.083
sigmaZZ=0.083

I = 1


VS1=Voltages(MyPoints[:,0],MyPoints[:,1],MyPoints[:,2],-5e-3,+5e-3,+0e-3,+I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS2=Voltages(MyPoints[:,0],MyPoints[:,1],MyPoints[:,2],+5e-3,+5e-3,+0e-3,-I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS3=Voltages(MyPoints[:,0],MyPoints[:,1],MyPoints[:,2],-5e-3,-5e-3,+0e-3,+I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')
VS4=Voltages(MyPoints[:,0],MyPoints[:,1],MyPoints[:,2],+5e-3,-5e-3,+0e-3,-I,sigmaXX,sigmaYY,sigmaZZ,'V','Vx','Vy','Vxx','Vyy','Vxy')

V1=VS1['V']+VS2['V']
V2=VS3['V']+VS4['V']

Vx1=VS1['Vx']+VS2['Vx']
Vx2=VS3['Vx']+VS4['Vx']

Vy1=VS1['Vy']+VS2['Vy']
Vy2=VS3['Vy']+VS4['Vy']

Vxx1=VS1['Vxx']+VS2['Vxx']
Vxx2=VS3['Vxx']+VS4['Vxx']

Vyy1=VS1['Vyy']+VS2['Vyy']
Vyy2=VS3['Vyy']+VS4['Vyy']

Vxy1=VS1['Vxy']+VS2['Vxy']
Vxy2=VS3['Vxy']+VS4['Vxy']

Venv=np.abs(np.abs(V1+V2)-np.abs(V1-V2))
Vxenv=np.abs(np.abs(Vx1+Vx2)-np.abs(Vx1-Vx2))
Vyenv=np.abs(np.abs(Vy1+Vy2)-np.abs(Vy1-Vy2))
Vxxenv=np.abs(np.abs(Vxx1+Vxx2)-np.abs(Vxx1-Vxx2))
Vyyenv=np.abs(np.abs(Vyy1+Vyy2)-np.abs(Vyy1-Vyy2))
Vxyenv=np.abs(np.abs(Vxy1+Vxy2)-np.abs(Vxy1-Vxy2))
ax.set_ylabel('y',color='r')

ax.patch.set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color('r')
plt.ylabel('Firing probability',labelpad=-0)
ax.yaxis.label.set_color('r')
ax.tick_params(axis='y', colors='r')
plt.xlim([-50,50])

ax2 = ax.twinx()
ax2.plot(MyPoints[:,0]*1000,Vxxenv/np.max(Vxxenv),alpha=0.95,linewidth=1,color='b',label=r'$AM_{A}$',linestyle='-')
ax2.set_ylabel('y',color='b')
plt.ylabel('|Normalized AM|',labelpad=-0)
ax2.spines["top"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2.spines["right"].set_color('b')
ax2.yaxis.label.set_color('b')
ax2.tick_params(axis='y', colors='b')
plt.ylim([0,1.01])
plt.xlim([-50,50])
plt.xticks([-50,-25,-5,0,5,25,50])
ax2.set_xticklabels(labels=[-50,-25,-5,0,5,25,50],ha='center')
plt.yticks([0,1])
plt.show()