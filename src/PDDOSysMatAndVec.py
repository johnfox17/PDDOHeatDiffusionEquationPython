import math
import numpy as np
import scipy
import PDDOFunctions

class PDDOSysMatAndVec:
    def __init__(self, pDDOOperator,geometry,diffEquation):
        self.SpSysMat = SetupODEMatrix2D(pDDOOperator, geometry, diffEquation)
        self.SysVec =  SetupODEVec2D(geometry, diffEquation)


def SetupODEMatrix2D(pDDOOperator, geometry, diffEquation):
    n1order = pDDOOperator.n1order
    n2order = pDDOOperator.n2order
    morder = pDDOOperator.morder
    asymFlag = pDDOOperator.asymFlag
    nsize = PDDOFunctions.getSize2D(n1order, n2order)
    coefs = diffEquation.coefs
    SpSysMat = np.zeros((geometry.totalNodes,geometry.totalNodes))
    #global SysVec = np.zeros(geometry.totalNodes)

    for iCurrentNode in range(geometry.totalNodes):
        diffAMat = PDDOFunctions.FormDiffAmat2D(morder, n1order, n2order, iCurrentNode, geometry)
        diffAMat = PDDOFunctions.ApplyConstraintOnAmat2D(asymFlag, n1order, n2order, iCurrentNode, diffAMat, geometry)
        for iDiff in range(pDDOOperator.numDiffOps):
            coef = coefs[iCurrentNode][iDiff]
            n1 = pDDOOperator.diffOps[iDiff][0]
            n2 = pDDOOperator.diffOps[iDiff][1]
            diffBVec2D = PDDOFunctions.FormDiffBVec2D( n1order, n2order, nsize, n1, n2)
            diffBVec2D = PDDOFunctions.ApplyConstraintOnBvec2D(n1order, n2order, iCurrentNode, asymFlag, geometry, diffBVec2D)
            diffAVec = scipy.sparse.linalg.spsolve(diffAMat,diffBVec2D)
            deltaMag = math.sqrt(geometry.deltaCoordinates[iCurrentNode][0]**2+geometry.deltaCoordinates[iCurrentNode][1]**2)
            for iFamilyMember in geometry.nodeFamiliesIdx[iCurrentNode]:
                if iCurrentNode != iFamilyMember:
                    xsi1 = geometry.coordinates[iCurrentNode][0] - geometry.coordinates[iFamilyMember][0]
                    xsi2 = geometry.coordinates[iCurrentNode][1]- geometry.coordinates[iFamilyMember][1]
                    pList = PDDOFunctions.pOperator2D(n1order, n2order, xsi1, xsi2, deltaMag)
                    weights = PDDOFunctions.weights2D(n1order, n2order, nsize, xsi1, xsi2, deltaMag)
                    gFunVal = np.dot(diffAVec,np.multiply(pList,weights[0]))
                    if (math.isnan(gFunVal) != True):
                        SpSysMat[iCurrentNode][iFamilyMember] += coef*gFunVal*geometry.deltaVolumes[iFamilyMember]/(deltaMag**(n1+n2))
        #SysVec[iCurrentNode]= coefs[iCurrentNode][2] ##It's for this case i hardcoded the 2
                    
    return SpSysMat

def SetupODEVec2D(geometry, diffEquation):
    SysVec = np.zeros(geometry.totalNodes)
    coefs = diffEquation.coefs
    for iCurrentNode in range(geometry.totalNodes):
        SysVec[iCurrentNode]= coefs[iCurrentNode][2] ##It's for this case i hardcoded the 2
    return SysVec


