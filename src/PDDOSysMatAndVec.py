import math
import numpy as np
import scipy

class PDDOSysMatAndVec:
    def __init__(self, pDDOOperator,geometry,diffEquation):
        self.SpSysMat = SetupODEMatrix2D(pDDOOperator, geometry, diffEquation)
        self.SysVec =  SetupODEVec2D(geometry, diffEquation)


def ApplyConstraintOnBvec2D(n1order, n2order, iCurrentNode, pDDOOperator, geometry, diffBVec2D):
    tol = 1e-5              
    if(n1order >= 1 and n2order>=1):
        if(pDDOOperator.asymFlag == 1 and geometry.coordinates[iCurrentNode][1] < tol ):
            diffBVec2D[1] = 0.0
        if(pDDOOperator.asymFlag == 2 and geometry.coordinates[iCurrentNode][2] < tol ):
            diffBVec2D[2] = 0.0
    
    return diffBVec2D

def FormDiffBVec2D( n1order, n2order, nsize, n1, n2):
    blist = [0.0]*nsize
    fn1 = 1
    fn2 = 1
    if n1!=0:
        fn1=fn1*n1
    if n2!=0:
        fn2=fn2*n2
    coef = fn1*fn2
    iterm = 0
    if( n1order >=0 and n2order >= 0 ):
        iterm = iterm 
        if( n1 == 0 and n2 == 0 ):
            m = iterm
        
        if( n1order >= 1 ):
            iterm = iterm + 1
            if( n1 == 1 and n2 == 0 ):
                m = iterm
        
        if( n2order >= 1 ):
            iterm = iterm + 1
            if( n1 == 0 and n2 == 1 ): 
                m = iterm
        
        if( n1order >= 2 ):
            iterm = iterm + 1
            if( n1 == 2 and n2 == 0 ):
                m = iterm
        blist[m] = coef
    return blist


def ApplyConstraintOnAmat2D(asymFlag, n1order, n2order, iCurrentNode, diffAMat, geometry):
    tol = 0.003
    if(n1order >= 1 and n2order>=1 ):
        if(asymFlag == 1 and geometry.coordinates[iCurrentNode][1] < tol):
            diffAMat[:,1] = 0.0
            diffAMat[1,:] = 0.0
            diffAMat[1,1] = 1.0
        if(asymFlag == 2 and geometry.coordinates[iCurrentNode][2] < tol ):
            diffAMat[:,2] = 0.0
            diffAMat[2,:] = 0.0
            diffAMat[2,2] = 1.0
    
    return diffAMat 


def getSize2D(n1order, n2order):
    if (n1order==2 and n2order==1):
        nsize = 4
    if (n1order==2 and n2order==2):
        nsize = 6
    return nsize
def weights2D(n1order, n2order, nsize, xsi1, xsi2, deltaMag):
    xsiMag = math.sqrt(xsi1**2+xsi2**2)
    wt = math.exp(-4*(xsiMag/deltaMag)**2)
    if (n1order==2 and n2order==1):
        weights = np.full((1,nsize),wt)
    if (n1order==2 and n2order==2):
        weights = np.full((1,nsize),wt)
    return weights
def pOperator2D(n1order, n2order, xsi1, xsi2, deltaMag):
    xsi1p = xsi1/deltaMag
    xsi2p = xsi2/deltaMag
    if (n1order==2 and n2order==1):
        pList = np.array([1.0, xsi1p, xsi2p, xsi2p**2])
    if (n1order==2 and n2order==2):
        pList = np.array([1.0, xsi1p, xsi2p, xsi1p**2, xsi1p*xsi2p, xsi2p**2])
    return pList

def FormDiffAmat2D(morder, n1order, n2order, iCurrentNode, geometry):
    deltaMag = math.sqrt(geometry.deltaCoordinates[iCurrentNode][0]**2+geometry.deltaCoordinates[iCurrentNode][1]**2)
    nsize = getSize2D(n1order, n2order)
    diffAmat2D = np.zeros((nsize,nsize))
    for iFamilyMember in geometry.nodeFamiliesIdx[iCurrentNode]:
        if iCurrentNode != iFamilyMember:
            xsi1 = geometry.coordinates[iCurrentNode][0] - geometry.coordinates[iFamilyMember][0]
            xsi2 = geometry.coordinates[iCurrentNode][1]- geometry.coordinates[iFamilyMember][1]
            pList = pOperator2D(n1order, n2order, xsi1, xsi2, deltaMag)
            weights = weights2D(n1order, n2order, nsize, xsi1, xsi2, deltaMag)
            diffAmat2D+=weights*np.outer(pList,pList)*geometry.deltaVolumes[iFamilyMember]

    return diffAmat2D 


def SetupODEMatrix2D(pDDOOperator, geometry, diffEquation):
    n1order = pDDOOperator.n1order
    n2order = pDDOOperator.n2order
    morder = pDDOOperator.morder
    asymFlag = pDDOOperator.asymFlag
    nsize = getSize2D(n1order, n2order)
    coefs = diffEquation.coefs
    SpSysMat = np.zeros((geometry.totalNodes,geometry.totalNodes))
    #global SysVec = np.zeros(geometry.totalNodes)

    for iCurrentNode in range(geometry.totalNodes):
        diffAMat = FormDiffAmat2D(morder, n1order, n2order, iCurrentNode, geometry)
        diffAMat = ApplyConstraintOnAmat2D(asymFlag, n1order, n2order, iCurrentNode, diffAMat, geometry)
        for iDiff in range(pDDOOperator.numDiffOps):
            coef = coefs[iCurrentNode][iDiff]
            n1 = pDDOOperator.diffOps[iDiff][0]
            n2 = pDDOOperator.diffOps[iDiff][1]
            diffBVec2D = FormDiffBVec2D( n1order, n2order, nsize, n1, n2)
            diffBVec2D = ApplyConstraintOnBvec2D(n1order, n2order, iCurrentNode, pDDOOperator, geometry, diffBVec2D)
            diffAVec = scipy.sparse.linalg.spsolve(diffAMat,diffBVec2D)
            deltaMag = math.sqrt(geometry.deltaCoordinates[iCurrentNode][0]**2+geometry.deltaCoordinates[iCurrentNode][1]**2)
            for iFamilyMember in geometry.nodeFamiliesIdx[iCurrentNode]:
                if iCurrentNode != iFamilyMember:
                    xsi1 = geometry.coordinates[iCurrentNode][0] - geometry.coordinates[iFamilyMember][0]
                    xsi2 = geometry.coordinates[iCurrentNode][1]- geometry.coordinates[iFamilyMember][1]
                    pList = pOperator2D(n1order, n2order, xsi1, xsi2, deltaMag)
                    weights = weights2D(n1order, n2order, nsize, xsi1, xsi2, deltaMag)
                    gFunVal = np.dot(diffAVec,np.multiply(pList,weights[0]))
                    #if (math.isnan(gFunVal) != True):
                    SpSysMat[iNode][iFamilyMember] += coef*gFunVal*geometry.deltaVolumes[iFamilyMember]/(deltaMag**(n1+n2))
        #SysVec[iCurrentNode]= coefs[iCurrentNode][2] ##It's for this case i hardcoded the 2
                    
    return SpSysMat

def SetupODEVec2D(geometry, diffEquation):
    numberNodes = np.size(geometry.nodeFamiliesIdx)
    SysVec = np.zeros(numberNodes)
    coefs = diffEquation.coefs
    for iCurrentNode in range(numberNodes):
        SysVec[iCurrentNode]= coefs[iCurrentNode][2] ##It's for this case i hardcoded the 2
    return SysVec


