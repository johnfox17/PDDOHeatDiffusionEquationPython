import math
import numpy as np
def bOperator2D( n1order, n2order, nsize, n1, n2):
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


def ApplyConstraintOnAmat2D(asymFlag, n1order, n2order, iCurrentNode, diffAMat, Geometry):
    tol = 0.003
    if(n1order >= 1 and n2order>=1 ):
        if(asymFlag == 1 and Geometry.coordinates[iCurrentNode][1] < tol):
            diffAMat[:,1] = 0.0
            diffAMat[1,:] = 0.0
            diffAMat[1,1] = 1.0
        if(asymFlag == 2 and Geometry.coordinates[iCurrentNode][2] < tol ):
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

def FormDiffAmat2D(morder, n1order, n2order, iCurrentNode, Geometry):
    deltaMag = math.sqrt(Geometry.deltaCoordinates[iCurrentNode][0]**2+Geometry.deltaCoordinates[iCurrentNode][1]**2)
    nsize = getSize2D(n1order, n2order)
    DiffAmat2D = np.zeros((nsize,nsize))
    for iFamilyMember in Geometry.nodeFamiliesIdx[iCurrentNode]:
        if iCurrentNode != iFamilyMember:
            xsi1 = Geometry.coordinates[iCurrentNode][0] - Geometry.coordinates[iFamilyMember][0]
            xsi2 = Geometry.coordinates[iCurrentNode][1]- Geometry.coordinates[iFamilyMember][1]
            pList = pOperator2D(n1order, n2order, xsi1, xsi2, deltaMag)
            weights = weights2D(n1order, n2order, nsize, xsi1, xsi2, deltaMag)
            DiffAmat2D+=weights*np.outer(pList,pList)*Geometry.deltaVolumes[iFamilyMember]

    return DiffAmat2D 

def inverse2(nsize, DiffAmat2D, DiffAmatInv2D, k, rcond):
    return 0 
def SetupODEMatrixVector2D(PDDOOperator, Geometry, coefs):
    n1order = PDDOOperator.n1order
    n2order = PDDOOperator.n2order
    morder = PDDOOperator.morder
    asymFlag = PDDOOperator.asymFlag
    nsize = getSize2D(n1order, n2order)
    for iCurrentNode in range(Geometry.totalNodes):
        diffAMat = FormDiffAmat2D(morder, n1order, n2order, iCurrentNode, Geometry)
        diffAMat = ApplyConstraintOnAmat2D(asymFlag, n1order, n2order, iCurrentNode, diffAMat, Geometry)
        coefsCurrentNode = coefs[iCurrentNode]
        for iDiff in range(PDDOOperator.numDiffOps):
            n1 = PDDOOperator.diffOps[iDiff][0]
            n2 = PDDOOperator.diffOps[iDiff][1]
            coef = coefsCurrentNode[iDiff]
            #diffBVec = FormDiffBVec2D(n1order, n2order, nsize)
            diffBVec = bOperator2D( n1order, n2order, nsize, n1, n2)
            print(diffBVec)
            print(n1,n2)
            a = input('').split(" ")[0]
    return 0

