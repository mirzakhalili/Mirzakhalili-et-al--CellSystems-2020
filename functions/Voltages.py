import numpy as np
def Voltages(X,Y,Z,X0,Y0,Z0,I,SigmaXX,SigmaYY,SigmaZZ,*args):

    Dx=X-X0
    Dy=Y-Y0
    Dz=Z-Z0
    
    Sigma=np.sqrt(SigmaXX*SigmaYY*SigmaZZ)
    R2=(1.0/SigmaXX)*Dx**2+(1.0/SigmaYY)*Dy**2+(1.0/SigmaZZ)*Dz**2
    R1=np.sqrt(R2)
    if args:
        pass
    else:
        args={'V','Vx','Vy','Vz','Vxx','Vyy','Vzz','Vxy','Vxz','Vzz'}
    
    dict={key: [] for key in args}

    if 'V' in args:
        V=I/(4*np.pi*Sigma)/R1
        dict['V']=V

    if 'Vx' or 'Vy' or 'Vz' in args:
        R3=R1**3
        if 'Vx' in args:
            Vx=I/(4*np.pi*Sigma)*-Dx/R3/SigmaXX
            dict['Vx']=Vx
        if 'Vy' in args:
            Vy=I/(4*np.pi*Sigma)*-Dy/R3/SigmaYY
            dict['Vy']=Vy
        if 'Vz' in args:
            Vz=I/(4*np.pi*Sigma)*-Dz/R3/SigmaZZ
            dict['Vz']=Vz
    if 'Vxx' or 'Vyy' or 'Vzz' or 'Vxy' or 'Vxz' or 'Vyz':
        R5=R1**5
        if 'Vxx' in args:
            Vxx=I/(4*np.pi*Sigma)*(3*Dx**2-SigmaXX*R2)/R5/SigmaXX/SigmaXX
            dict['Vxx']=Vxx
        if 'Vyy' in args:
            Vyy=I/(4*np.pi*Sigma)*(3*Dy**2-SigmaYY*R2)/R5/SigmaYY/SigmaYY
            dict['Vyy']=Vyy
        if 'Vzz' in args:
            Vzz=I/(4*np.pi*Sigma)*(3*Dz**2-SigmaZZ*R2)/R5/SigmaZZ/SigmaZZ
            dict['Vzz']=Vzz
        if 'Vxy' in args:
            Vxy=I/(4*np.pi*Sigma)*(3*Dx*Dy   )/R5/SigmaXX/SigmaYY
            dict['Vxy']=Vxy
        if 'Vxz' in args:
            Vxz=I/(4*np.pi*Sigma)*(3*Dx*Dz   )/R5/SigmaXX/SigmaZZ
            dict['Vxz']=Vxz
        if 'Vyz' in args:
            Vyz=I/(4*np.pi*Sigma)*(3*Dy*Dz   )/R5/SigmaYY/SigmaZZ
            dict['Vyz']=Vyz
    return dict