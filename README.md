# Mirzakhalili-et-al--CellSystems-2020

You need NEURON software and Python to run the simulations. 
You need to use NEURON to compile the files included in “cells” to run the simulations.
The other essential files are included in “functions” and “classes” folder.
Please download all the files and folders and put them in the same folder.

## ThresholdCalculation.py:

This code can be run to calculate the activation threshold for a given carrier and beat frequency.  
## AxonActivity.py:

This code performs the simulation for a given carrier and beat frequency. You should also provide the applied current and the axon distance from the midline. Note that setting the beat frequency equal 0 can be used to perform No-TI stimulation.

## BlockTest.py:
This code is similar to AxonActivity.py. Two additional options are added to check for block. You need to define the node number and the time at the test pulse is applied. The membrane potential will be plotted at the injection site as well as a user-specified test site.
