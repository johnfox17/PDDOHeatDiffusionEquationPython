import math
import numpy as np
import scipy

class PDDOBC:
    def __init__(self, pDDOOperator,geometry,diffEquation):
        self.SpSysMatBC = SetupODEBC2D()
        self.SysVecBC = SetupODEVecBC2D()


def extractBoundaries(PDDOOperator, Geometry):
    morder = PDDOOperator.morder
    BCidx = []
    if morder==2: #I hard coded it here need to find a way to loop through BCs
        BC1idx = np.where ( Geometry.coordinates[:,0]<=PDDOOperator.BC[0][1])[0]
        BC2idx = np.where ( Geometry.coordinates[:,0]>=PDDOOperator.BC[1][0])[0]
        BC3idx = np.where(Geometry.coordinates[:,1]<=PDDOOperator.BC[2][3])[0]
        BCidx = [BC1idx,BC2idx,BC3idx]
    return BCidx

def SetupODEBC2D():
    

    return 0

def SetupODEVecBC2D():
    return 0 
