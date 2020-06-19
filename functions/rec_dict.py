from neuron import h

def rec_dict(recording_dict,sec,location,variable):
    """
    rec_dict(recording_dict,sec,location,variable)
        recording_dict = the name of the dictionary to append
        sec = the neuron section object
        location = the location within the section (0 <= location <= 1)
        variable = independent or state variable to be recorded (e.g. vm, i_membrane)

    Defines the dictionary of variables to be recorded during the simulation
        Outputs the dictionary in the form:
            self.recording_dict = {sec.variable : h.sec(location)._ref_variable}
    """
    
    recording_dict[sec.name()+'('+str(location)+').'+str(variable)] = \
        eval('h.'+sec.name()+'('+str(location)+')'+'._ref_'+str(variable))

    return recording_dict