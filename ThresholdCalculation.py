# Importing necessary files

import sys
from neuron import h
from classes.Cell_rdg import MRG
from functions.rec_dict import rec_dict
from functions.Voltages import Voltages
import numpy as np
import os

sys.path.insert(0, "/Applications/NEURON-7.7/nrn/x86_64/bin")
sys.path.insert(0, "/Applications/NEURON-7.7/nrn/lib/python")

def model(Duration,Freq,DFreq,Amps):
    fs = 1000*50*4  # Hz, sampling rate

    h.cvode_active(0)  # turn off variable time step
    h.steps_per_ms = fs*1e-3  # steps per ms for NEURON simulation
    h.dt = 1/(fs*1e-3)  # ms, sample spacing
    h.celsius = h.celsius  # temperature at which to run simulation
    h.v_init = -80.  # mV, initial voltage to begin simulations
    YY=.0e-3
    ZZ=0
    MyTraj = np.array([[-50e-3,YY,ZZ], [+51e-3,YY,ZZ]])
    
    MyPath = os.getcwd() + '/'
    CELL_DIR = MyPath+'cells/'
    CELL_FILE_NAME = 'NewMRGaxon_for_Python.hoc'
    MyD = 8.7
    MyCell = MRG(axon_trajectory=MyTraj, fiberD=MyD,
                CELL_FILE_NAME=CELL_FILE_NAME, CELL_DIR=CELL_DIR)

    I = 1.  # current source amplitude in A

    # find xyz coordinates of center of each axon compartment
    nrn_xyz = list()
    for sec in MyCell.get_secs():
        nrn_xyz.append(MyCell.center_3Dcoords(sec))

    nrn_xyz = np.array(nrn_xyz)*1e-6  # m, convert from um to m

    sigmaXX=0.6
    sigmaYY=0.083
    sigmaZZ=0.083

    VS1=Voltages(nrn_xyz[:,0],nrn_xyz[:,1],nrn_xyz[:,2],-5e-3,+5e-3,+0e-3,+I,sigmaXX,sigmaYY,sigmaZZ,'V')['V']
    VS2=Voltages(nrn_xyz[:,0],nrn_xyz[:,1],nrn_xyz[:,2],+5e-3,+5e-3,+0e-3,-I,sigmaXX,sigmaYY,sigmaZZ,'V')['V']
    VS3=Voltages(nrn_xyz[:,0],nrn_xyz[:,1],nrn_xyz[:,2],-5e-3,-5e-3,+0e-3,+I,sigmaXX,sigmaYY,sigmaZZ,'V')['V']
    VS4=Voltages(nrn_xyz[:,0],nrn_xyz[:,1],nrn_xyz[:,2],+5e-3,-5e-3,+0e-3,-I,sigmaXX,sigmaYY,sigmaZZ,'V')['V']

    V1 = VS1+VS2  # voltage of first pair
    V2 = VS3+VS4  # voltage of second pair

    recordingDict = dict()
    location = 0.5
    variable = {'v'}
    iSec=0
    # MyPoints = list()
    for Sec in MyCell.get_secs():
        Sec.rx1_xtra=V1[iSec]
        Sec.rx2_xtra=V2[iSec]
        iSec=iSec+1
        if ("node" in Sec.name()):
            for vars in variable:
                rec_dict(recordingDict, Sec, location, vars)

    MyCell.record(recordingDict)

    h.load_file("stdrun.hoc")
    h.init()
    h.finitialize(h.v_init)
    h.fcurrent()

    h.tstop = Duration
    Times=np.arange(0,h.tstop+h.dt,h.dt)
    Sim1=Amps*np.sin(2*np.pi*Freq/1000.0*Times)
    Sim2=Amps*np.sin(2*np.pi*(Freq+DFreq)/1000.0*Times)

    t = h.Vector(Times)
    Stim1=h.Vector(Sim1*1e-3)
    Stim2=h.Vector(Sim2*1e-3)
    Stim1.play(h._ref_is1_xtra, t, 0)
    Stim2.play(h._ref_is2_xtra, t, 0)

    h.run()
    return MyCell

def Target(nTarget,Cycle, APTimes):
    Found=False
    APTimes = np.asarray(APTimes.to_python())
    Mask = np.ones(len(APTimes), dtype=bool)
    Mask[APTimes<Cycle/2]=False
    APTimes=APTimes[Mask]
    if len(APTimes) < nTarget:
        Found = False
    else:
        Tcheck=APTimes[0]
        NFound=1
        for i in range(len(APTimes)):
            if APTimes[i]-Tcheck>Cycle/2:
                NFound=NFound+1
                Tcheck=APTimes[i]
            if NFound==nTarget:
                Found=True
                break
    return(Found)

def Trial(N,Freq,DFreq,Amps):
    if DFreq==0:
        DFreq0=10
        Cycle=1000/DFreq0
    else:
        Cycle=1000/DFreq
    Duration=(N+0.5)*Cycle
    MyCell=model(Duration,Freq,DFreq,Amps)
    APTimes=MyCell.apc_times
    Found=Target(N,Cycle, APTimes)
    AllAPTs=MyCell.apTimesDict.copy()
    return Found,AllAPTs

def Threshold(xL,xR,N,Freq,DFreq):
    ii = 0
    delta = 1e-3
    Found=False
    Found,_=Trial(N,Freq,DFreq,xL)
    while ii < 20:
        if Found == False:
            Check = True
            break
        else:
            xR = xL
            xL=xL*0.5
            ii = ii+1
            Found,_=Trial(N,Freq,DFreq,xL)
            Check = False
    if Check == True:
        while ii < 20:
            Found,AllAPTs=Trial(N,Freq,DFreq,xR)
            if Found == True:
                break
            else:
                xL = xR
                xR = xR*2.0
                Found,AllAPTs=Trial(N,Freq,DFreq,xR)
                ii = ii+1
    Del = (xR-xL)/xR
    xM = 0.5*(xR+xL)
    ii = 0
    while Del > delta:
        xM = 0.5*(xR+xL)
        Found,AllAPTs=Trial(N,Freq,DFreq,xM)
        if Found == True:
            xR = xM
        else:
            xL = xM
        Del = (xR-xL)/xR
        ii = ii+1
    xM = 0.5*(xR+xL)
    return xL, xR

if __name__ == "__main__":
    
    # Carrier frequency [Hz]
    Carrier= 2000
    # Beat frequency [Hz]
    Beat= 100
    # lower and upper limits for the start of the search
    Lower,Upper=0.008,0.009
    # Number of beats
    NB=10
    
    print('Calculating the activation threshold for:')
    print('Carrier frequency = {:.0f} [Hz] and Beat frequency = {:.0f} [Hz]'.format(Carrier,Beat))
    Lower, Upper=Threshold(Lower,Upper,NB,Carrier,Beat)
    print('The activation threshold for {:d} beats is between:'.format(NB))
    print('{:.3f} mA and {:.3f} mA'.format(Lower*1e3,Upper*1e3) )
