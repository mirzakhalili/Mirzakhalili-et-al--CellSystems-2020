from __future__ import division
from neuron import h
import neuron as nrn
h.load_file("stdrun.hoc")
from numpy import pi,shape,array,ones
from functions.find_node_coordinates import find_node_coordinates

import sys

class Cell(object):
    '''
    A NEURON multi-compartment model
        axon_type:
            'MRG':  mammalian axon, based on McIntyre et al., 2002
    '''

    ##    def __init__(self,axon_trajectory,fiberD,CELL_DIR=None,**kwargs):
    def __init__(self,**kwargs):
    #use of *args allows both DC axons and DR fibers with DC collaterals to be defined
    #see loop below for necessary number of arguments
        """Initialize cell by loading HOC file"""

        self.variables = kwargs #possible variables to define

        #-----------------------------------------------------------------------
        # Cell Parameters
        #-----------------------------------------------------------------------
 
        #Check for directory containing cell model
        if not self.CELL_DIR:
            raise TypeError("No directory specified for loading model axon...")

        #Check for HOC filename of cell model
        if not self.CELL_FILE_NAME:
            raise TypeError("No HOC file specified...")

        #-----------------------------------------------------------------------
        # Import Mechanisms
        #-----------------------------------------------------------------------
        nrn.NRN_NMODL_PATH=self.CELL_DIR
        nrn.load_mechanisms(nrn.NRN_NMODL_PATH)
        #----------------------------------------------------------------------
        # Construct cell
        #-----------------------------------------------------------------------
        self._construct_cell()
        #-----------------------------------------------------------------------
        # Load extracellular mechanisms
        #-----------------------------------------------------------------------
        self._xtra()
        #-----------------------------------------------------------------------
        # Create action potential counters
        #-----------------------------------------------------------------------
        self._ap_counters()

    def __str__(self):
        return "Generic Axon Type"

    def __del__(self):
        pass

    def __info__(self):
        info = str(self)
        info += "\n-Axon Root: %s" % h.secname(sec=self.root)
        info += "\n-Axon Root XYZ: %s" % str(self.retrieve_coordinates(sec=self.root))
        return info

    def _construct_cell(self):
        """ Choose axon type """
        raise "Dummy Axon"

    def _ap_counters(self):
        """ Create action potential counters, esp. useful for threshold
        calculation """

        self.apc = h.APCount(0.5,sec = self.root)
        self.apc.thresh = -20.0     #mV, threshold voltage for AP detection
        self.apc_times = h.Vector()
        self.apc.record(self.apc_times)
        
    def root_section(self):
        return h.SectionRef().root

    def center_3Dcoords(self,sec):
        """
        Returns the 3D coordinates of the center of the currently accessed section

        Requires the 'xtra' mechanism
        """
        x = sec(0.5).x_xtra
        y = sec(0.5).y_xtra
        z = sec(0.5).z_xtra

        return x,y,z

    def get_im(self,sec):
        ''' Dummy function for defining im of a section, to be used in 'build_tree' as 'func'
        '''
        im = sec(0.5).i_membrane
        
        return im

    def build_tree(self, func,segfunc=False):
        """
        func must act on a neuron section
        """
        from numpy import array
        print ("-"*100)
        def append_data(sec, xyzdv, parent_id, connections,func,segfunc):
            """ Append data to xyzdv
            """
            if not segfunc: v=func(sec)
            n = int(h.n3d(sec=sec))
            
            for ii in xrange(1, n):
                x = h.x3d(ii,sec=sec)
                y = h.y3d(ii,sec=sec)
                z = h.z3d(ii,sec=sec)
                d = h.diam3d(ii,sec=sec)
                if 'node' in sec.name() or 'MYSA' in sec.name() :
                    v = 1.0
                else: pass
                if segfunc:
                    if n==1:v=func(sec(0.5))
                    else:v = func(sec(ii/float(n-1)))
                xyzdv.append([x,y,z,d,v])
                child_id = len(xyzdv)-1
                if len(xyzdv)>1:
                    connections.append([child_id, parent_id])
                parent_id = child_id
            
            return xyzdv, connections

        def append_children_data(parent, parent_id, xyzdv, connections, func, segfunc):
            sref = h.SectionRef(sec=parent)
            if sref.child:
                for child in sref.child:
                    xyzdv, connections = append_data(child, xyzdv, parent_id, connections, func, segfunc)
                    xyzdv, connections = append_children_data(parent = child,
                                                              parent_id = len(xyzdv)-1,
                                                              xyzdv = xyzdv,
                                                              connections = connections,
                                                              func = func,
                                                              segfunc = segfunc)
            return xyzdv, connections

        # Find data and connections
        root_section = self.root_section()
        if segfunc:
            if root_section.nseg==1:
                v = func(root_section(0.5))
            else:
                v = func(root_section(0.0))
        else:
            v=func(root_section)
        xyzdv = [[h.x3d(0,sec=root_section),h.y3d(0,sec=root_section),h.z3d(0,sec=root_section),h.diam3d(0,sec=root_section),v]]
        xyzdv, connections = append_data(root_section, xyzdv, 0, [],func,segfunc)
        xyzdv, connections = append_children_data(root_section,len(xyzdv)-1,xyzdv,connections,func,segfunc)
        self.xyzdv = array(xyzdv)
        self.connections = array(connections)

    def display(self, func, segfunc=False, scaling=1, replace=True, clim=None, colormap='jet'):
        ''' Display current cell in mayavi
        '''
        #from neuron import h
        from numpy import array, vstack, float_
        from enthought.mayavi import mlab
        from enthought.mayavi.mlab import pipeline
        if replace:
            try:self.mlab_cell.parent.parent.parent.parent.parent.parent.remove()
            except AttributeError:pass
        ### Turn off vtk warnings # # # # # # # # # # # # # # # # # # # # # # #
        from vtk import vtkObject
        o = vtkObject
        o.GetGlobalWarningDisplay()
        o.SetGlobalWarningDisplay(0) # Turn it off.

        f = mlab.figure(figure=mlab.gcf(),
                        bgcolor=(1,1,1),
                        size=(800,600))

        self.build_tree(func, segfunc)
  ##        xs = self.xyzdv[:,0]
  ##        ys = self.xyzdv[:,1]
  ##        zs = self.xyzdv[:,2]
        xs = float_(self.xyzdv[:,0])
        ys = float_(self.xyzdv[:,1])
        zs = float_(self.xyzdv[:,2])

        # don't want scaling for soma segments
  ##        diams = self.xyzdv[:,3]
        diams = float_(self.xyzdv[:,3])
        #nonsoma = (diams < 15) # non-somatic
        nonsoma = ones(shape(diams))
        diams += diams*nonsoma*(scaling-1)
        #diams = self.xyzdv[:,3] * scaling # larger scaling makes neurons more visible
  ##        data = self.xyzdv[:,4]
        data = float_(self.xyzdv[:,4])
        edges = self.connections

        # Display in mayavi
        pts = pipeline.scalar_scatter(xs, ys, zs, diams/2.0,
                                      name=str(self))
        dataset = pts.mlab_source.dataset
        dataset.point_data.get_array(0).name = 'diameter'
        dataset.lines = vstack(edges)

        array_id = dataset.point_data.add_array(data.T.ravel())
        dataset.point_data.get_array(array_id).name = 'data'
        dataset.point_data.update()

        #### Create tube with diameter data
        src = pipeline.set_active_attribute(pts,
                                            point_scalars='diameter')
        stripper = pipeline.stripper(src)
        tube = pipeline.tube(stripper,
                             tube_sides = 8,
                             tube_radius = 1)
        tube.filter.capping = True
        tube.filter.use_default_normal = False
        tube.filter.vary_radius = 'vary_radius_by_absolute_scalar'
        #tube.filter.radius_factor = 90.0 # just for making movies
        src2 = pipeline.set_active_attribute(tube, point_scalars='data')

        lines = pipeline.surface(src2,colormap = colormap)
        if clim:
            from numpy import array
            lines.parent.scalar_lut_manager.use_default_range = False
            lines.parent.scalar_lut_manager.data_range = array(clim)
        self.mlab_cell = lines

    def draw(self, func, scaling = 1, segfunc=False, clim=None,cmap=None):
        """ Draw cell in matplotlib line plot collection
        """
        from numpy import array, linspace
        from matplotlib.collections import LineCollection
        from matplotlib import pyplot
        self.build_tree(func,segfunc)
        pts   = self.xyzdv[:,:2]
        edges = self.connections
        diam  = self.xyzdv[:,3]
        data  = self.xyzdv[:,4]
        print ("DATA RANGE: ",data.min(),data.max())
        # Define colors
        if not cmap:
            from matplotlib.cm import jet as cmap
        if not clim:
            clim=[data.min(),data.max()]
        a = (data - clim[0])/(clim[1]-clim[0])
        # Define line segments
        segments = []
        for edge in edges:
            segments.append([pts[edge[0],:], pts[edge[1],:]])
        # Build Line Collection
        collection = LineCollection(segments = array(segments),
                                    linewidths = diam*scaling,
                                    colors=cmap(a))
        collection.set_array(data)
        collection.set_clim(clim[0], clim[1])
        pyplot.gca().add_collection(collection,autolim=True)
        pyplot.axis('equal')
        return collection

    def move(self, xyz, move_mlab=False):
        """ Move visualization and cell by a certain amount """
        from neuron import h
        if move_mlab:
            if self.mlab_cell:
                self.mlab_cell.mlab_source.x = self.mlab_cell.mlab_source.x + xyz[0]
                self.mlab_cell.mlab_source.y = self.mlab_cell.mlab_source.y + xyz[1]
                self.mlab_cell.mlab_source.z = self.mlab_cell.mlab_source.z + xyz[2]
        tree = h.SectionList()
        tree.wholetree(sec=self.root)
        for sec in tree:
            for ii in xrange(h.n3d(sec=sec).__int__()):
                x=h.x3d(ii,sec=sec)
                y=h.y3d(ii,sec=sec)
                z=h.z3d(ii,sec=sec)
                d=h.diam3d(ii,sec=sec)
                h.pt3dchange(ii,x+float(xyz[0]),y+float(xyz[1]),z+float(xyz[2]),d)

    def rotate(self,theta):
        """ Rotate neuron coordinates.
            theta = [thetax,thetay,thetaz]
        """
        from neuron import h
        from mytools.rotate_xyz import rotate_xyz

        tree = h.SectionList()
        tree.wholetree(sec=self.root)
        for sec in tree:
            for ii in xrange(h.n3d(sec=sec).__int__()):
                x=h.x3d(ii,sec=sec)
                y=h.y3d(ii,sec=sec)
                z=h.z3d(ii,sec=sec)
                d=h.diam3d(ii,sec=sec)

                xyz_out=rotate_xyz(theta,[x,y,z])
                
                h.pt3dchange(ii,float(xyz_out[0]),float(xyz_out[1]),float(xyz_out[2]),d)

    def retrieve_coordinates(self,sec):
        """
        Returns the 3D coordinates of all points in the currently accessed section.

        Does not calculate the center of each section (see 'center_3Dcoords' above)
  "       """
        xyzds = []
        for ii in xrange(int(h.n3d(sec=sec))):
            xyzds.append([h.x3d(ii,sec=sec),
                          h.y3d(ii,sec=sec),
                          h.z3d(ii,sec=sec),
                          h.diam3d(ii,sec=sec)])
        return xyzds

    def record(self,recording_dict):
        """ add a new recording for section
            recording_dict should be a dictionary
            e.g.
                recording_dict={'node[0](0.5).v':h.node[0](0.5)._ref_v,
                                'node[20](0.5).v':h.node[20](0.5)._ref_v,
                                'node[40](0.5).v':h.node[40](0.5)._ref_v,
                                'stim.intensity':h.stim._ref_intensity}
        """
        self._recordings = {'t':h.Vector()}
        self._recordings['t'].record(h._ref_t)
        for k,v in recording_dict.items():
            self._recordings[k] = h.Vector()
            self._recordings[k].record(v)

    def plot(self,plot_keys,show = False):
        """
        plot(self,plot_keys,show = False)
            plot_keys = strings containing the desired variables to plot,
                        must be in the same form as returned by rec_dict()
            show: if = True, plots results, if = False, does not show plot
        """
        from matplotlib.pyplot import plot,legend,figure,axis
        figure()
        t = self._recordings['t']
        for k in plot_keys:
            if k != 't':
                plot(t,self._recordings[k],label = ("%s.%s" % (self,k)))
        legend()
 ##        axis([0,60,-150,150])
        if show:
            from matplotlib.pyplot import show as shw
            shw()

    def store(self,global_array=False,save=False,filename='sim_results.pkl'):
        """
            store(self,global_array,save,filename)
            Serves two functions:
                1. Place the vectors from 'record' in global arrays
                    - if global_array = True
                2. Save (via pickling) the vectors in a separate file (if 'save' = True)
                    - if save = True
                    (default filename = 'sim_results.pkl')
        """
        import cPickle #import module from serializing data to file
        from numpy import array

        self._nparrays = self._recordings
        for k,v in self._nparrays.items():
            self._nparrays[k] = array(v)

        if global_array:
            self.arrays = self._nparrays
            
        if save:
            output = open(filename,'wb')            
            cPickle.dump(self._nparrays,output,-1)
            output.close()

    def _xtra(self):
        """ Insert xtra mechanism to use for finding the center of each compartment (see interpxyz.hoc),
            and necessary extracellular mechanisms
        """
        for sec in h.allsec():
            sec.insert('xtra')

        #load required xtra files
        h.load_file(1,self.CELL_DIR+"interpxyz.hoc")    #only interpolates sections that have extracellular
        h.load_file(1,self.CELL_DIR+"setpointers.hoc")  #automatically calls grindaway() in interpxyz.hoc

    def set_tstop(self,tstop):
        h.tstop = tstop

    info = property(__info__)

    #make setting and getting variables/attributes scalable
    def set_variable(self,k,v):
        self.variables[k] = v
        #k = key, v = value
        
    def get_variable(self,k):
        return self.variables.get(k,None)

class MRG(Cell):
    '''
        Provide model description here
    '''
    def __init__(self,**kwargs):

        self.variables = kwargs

        if 'axon_trajectory' not in self.variables: raise TypeError('Need to specify axon trajectory!!!')
        if 'fiberD' not in self.variables:          raise TypeError('Need to specify axon diameter!!!') #um, diameter of DR fiber
        if 'CELL_DIR' not in self.variables: raise TypeError('Need to specify path to cell file!!!')
        if 'CELL_FILE_NAME' not in self.variables: raise TypeError('Need to specify the .hoc file name!!!')
        
        self.CELL_DIR = self.variables['CELL_DIR']
        self.CELL_FILE_NAME = self.variables['CELL_FILE_NAME']

        super(MRG,self).__init__(**kwargs)

        self._my_ap_counters()
    def __str__(self):
        return "MRG"

    def get_secs(self):
        ''' Get all neuron sections '''
        secs = [sec for sec in h.node]
        secs.extend([sec for sec in h.MYSA])
        secs.extend([sec for sec in h.FLUT])
        secs.extend([sec for sec in h.STIN])
        return secs
    
    def _construct_cell(self):
        """ mammalian motor axon """

        self.axon_trajectory = self.get_variable('axon_trajectory')
        self.fiberD = self.get_variable('fiberD')

        self.NODE_COORDINATES = find_node_coordinates(self.fiberD,self.axon_trajectory)

        # topological parameters, based on fiberD and NODE_COORDINATES (i.e. axon trajectory)
        self.numberOfStinCompartmentsPerStretch = 6

        self.axonnodes = shape(self.NODE_COORDINATES)[0]
        self.paranodes1 = 2*(self.axonnodes-1)
        self.paranodes2 = 2*(self.axonnodes-1)
        self.axoninter = self.numberOfStinCompartmentsPerStretch*(self.axonnodes-1)
        self.axontotal = self.axonnodes+self.paranodes1+self.paranodes2+self.axoninter

        # define necessary parameters
        h('fiberD = %.1f' % self.fiberD)
        h('numberOfStinCompartmentsPerStretch = %i' % self.numberOfStinCompartmentsPerStretch)
        h('axonnodes = %i' % self.axonnodes)
        h('paranodes1 = %i' % self.paranodes1)
        h('paranodes2 = %i' % self.paranodes2)
        h('axoninter = %i' % self.axoninter)
        h('axontotal = %i' % self.axontotal)

        # load node coordinates into hoc
        h('objref nx')
        h('objref ny')
        h('objref nz')
        h('nx = new Vector(%i)' % self.axonnodes)
        h('ny = new Vector(%i)' % self.axonnodes)
        h('nz = new Vector(%i)' % self.axonnodes)
        for i in range(self.axonnodes):
            h.nx.x[i] = self.NODE_COORDINATES[i,0]
            h.ny.x[i] = self.NODE_COORDINATES[i,1]
            h.nz.x[i] = self.NODE_COORDINATES[i,2]

        h.load_file(1,self.CELL_DIR+self.CELL_FILE_NAME)
        self.root = h.node[0]
    
    def _my_ap_counters(self):

        self.apCounterDict = dict()
        self.apTimesDict = dict()
        for sec in self.get_secs():
            if ('node' in sec.name()):
                name = sec.name()
                self.apCounterDict[name] = h.APCount(0.5, sec=sec)
                self.apCounterDict[name].thresh = -30
                self.apCounterDict[name+'_times'] = h.Vector()
                self.apTimesDict[sec.name()] = h.Vector()
                self.apCounterDict[name].record(self.apCounterDict[name+'_times'])
                self.apCounterDict[name].record(self.apTimesDict[sec.name()])
