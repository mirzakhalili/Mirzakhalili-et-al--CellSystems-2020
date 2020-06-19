def find_node_coordinates(fiberD,axon_trajectory):
    """
        Determine the coordinates of axon nodes for a give trajectory.
        Node spacing is determined by the fiber diameter

        Inputs:
            fiberD = um, fiber diameter
            axon_trajectory = n x 3 array containing the line segments describing the axon trajectory

        Outputs:
            array of x,y,z coordinates of nodes with the proper spacing along the provided trajectory

        Assumptions:
            node spacing is less than the distance between points in axon_trajectory
        
    """

    from numpy import array,sqrt,shape,sin,pi

    # specify deltax (i.e. node spacing) based on fiber diameter, try to work into axon class
    if (fiberD==2.0): deltax=117
    if (fiberD==5.7): deltax=500
    if (fiberD==7.3): deltax=750
    if (fiberD==8.7): deltax=1000
    if (fiberD==10.0): deltax=1150
    if (fiberD==11.5): deltax=1250
    if (fiberD==12.8): deltax=1350
    if (fiberD==14.0): deltax=1400
    if (fiberD==15.0): deltax=1450
    if (fiberD==16.0): deltax=1500 

    dx = deltax*1e-6                    #m, convert node spacing to m
    ii,jj = 0,0                         #counters for stepping through points of axon trajectories
    xx,yy,zz = list(),list(),list()     #"interpolated" node locations for NEURON
    P0 = axon_trajectory[ii,:]              #initialize point, P0
    P1 = axon_trajectory[ii+1,:]            #initialize point, P1
    xx.append(P0[0]); yy.append(P0[1]); zz.append(P0[2]) #define initial point of axon, i.e. first node
    while True:
        P = [xx[jj],yy[jj],zz[jj]]
        PP1 = sqrt(sum((P1-P)**2))
        if (PP1 > dx):
            P0P1 = sqrt(sum((P1-P0)**2))
            tt = (P0P1-PP1+dx)/P0P1
            xx.append((1-tt)*P0[0]+tt*P1[0])
            yy.append((1-tt)*P0[1]+tt*P1[1])
            zz.append((1-tt)*P0[2]+tt*P1[2])
            jj+=1
        else:
            ii+=1                               #update P0 and P1
            if (ii == (shape(axon_trajectory)[0]-1)):
                break
            P0 = P1
            P1 = axon_trajectory[ii+1,:]
            P0P1 = sqrt(sum((P1-P0)**2))
            tt = (dx-PP1)/P0P1
            xx.append((1-tt)*P0[0]+tt*P1[0])
            yy.append((1-tt)*P0[1]+tt*P1[1])
            zz.append((1-tt)*P0[2]+tt*P1[2])
            jj+=1
    return array([xx,yy,zz]).T
