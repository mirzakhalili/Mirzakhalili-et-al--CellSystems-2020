# Importing necessary files

import sys
from neuron import h
from classes.Cell_rdg import MRG
from functions.rec_dict import rec_dict
from functions.Voltages import Voltages
import numpy as np
import os
import matplotlib.pyplot as plt

sys.path.insert(0, "/Applications/NEURON-7.7/nrn/x86_64/bin")
sys.path.insert(0, "/Applications/NEURON-7.7/nrn/lib/python")

def model(Duration,Freq,DFreq,Amps,YY,InjT,InjS):
    fs = 1000*50*4  # Hz, sampling rate

    h.cvode_active(0)  # turn off variable time step
    h.steps_per_ms = fs*1e-3  # steps per ms for NEURON simulation
    h.dt = 1/(fs*1e-3)  # ms, sample spacing
    h.celsius = h.celsius  # temperature at which to run simulation
    h.v_init = -80.  # mV, initial voltage to begin simulations
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

    MySecs=MyCell.get_secs()
    InjSite=InjS
    MySecs = MyCell.get_secs()
    myIClamp = h.IClamp(0.5, sec=MySecs[InjSite])
    myIClamp.delay = 0
    myIClamp.dur = 1e9

    On=InjT

    TimesIClamp=list()
    AmpsIClamp=list()

    TimesIClamp.append(On)
    TimesIClamp.append(On+0.1)
    AmpsIClamp.append(1)
    AmpsIClamp.append(0)
    tIClamp = h.Vector(TimesIClamp)
    SimsIClamp = h.Vector(AmpsIClamp)

    SimsIClamp.play(myIClamp._ref_amp, tIClamp, 0)

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


if __name__ == "__main__":
    
    # Carrier frequency [Hz]
    Carrier= 2000
    # Beat frequency [Hz]
    Beat= 0
    # Applied current [mA]
    Amps=5.4
    # Number of beats
    NB=4
    # Axon distance from midline [mm]
    Y=0
    
    if Beat==0:
        Beat0=5
        print ('Simulating for No-TI')
        print ('The simulation duration is calculated as if the beat frequency was {:0.2f}'.format(Beat0))
        Cycle=1000/Beat0
        Duration=(NB+0.5)*Cycle
    else:
        Cycle=1000/Beat
        Duration=(NB+0.5)*Cycle

    print('Simulating an axon located at {:.2f} mm away from the midline'.format(Y))
    print('Applied current = {:.3f} [mA]'.format(Amps))
    print('Number of beats = {:d}'.format(NB))
    print('Carrier frequency = {:.0f} [Hz] and Beat frequency = {:.0f} [Hz]'.format(Carrier,Beat))

    # The location where the set pulse is sent
    InjSite=0
    # The time that the test pulse is sent
    InjTime=2.5*Cycle
    print('Sending a test pulse at node {:d} and {:.2f} ms'.format(InjSite,InjTime))
    
    MyCell=model(Duration,Carrier,Beat,Amps/1000,Y/1000,InjTime,InjSite)

    Results=MyCell._recordings

    TestSite=100
    T=np.asfarray(Results['t'])
    V1=np.asfarray(Results['node['+str(InjSite)+'](0.5).v'])
    V2=np.asfarray(Results['node['+str(TestSite)+'](0.5).v'])
    plt.subplot(2,1,1)
    plt.plot(T,V1)
    plt.ylabel('Membrane potential [mV]')
    plt.title('Node '+str(InjSite))

    plt.subplot(2,1,2)
    plt.plot(T,V2)
    plt.ylabel('Membrane potential [mV]')
    plt.xlabel('Time [ms]')
    plt.title('Node '+str(TestSite))

    plt.show()
