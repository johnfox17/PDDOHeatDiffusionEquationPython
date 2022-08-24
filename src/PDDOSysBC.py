import math
import numpy as np
import scipy
import PDDOFunctions

class PDDOSysBC:
    def __init__(self, pDDOOperator,geometry,diffEquation):
        self.SpSysMatBC = SetupODEBC2D(pDDOOperator,geometry,diffEquation)
        self.SysVecBC = SetupODEVecBC2D()


def getSize2D(n1order, n2order):
    if (n1order==2 and n2order==1):
        nsize = 4
    if (n1order==2 and n2order==2):
        nsize = 6
    return nsize

def extractBoundaries(diffEquation, geometry, morder):
    BCidx = []
    if morder==2: #I hard coded it here need to find a way to loop through BCs
        BC1idx = np.where ( geometry.coordinates[:,0]<=diffEquation.BC[0][1])[0]
        BC2idx = np.where ( geometry.coordinates[:,0]>=diffEquation.BC[1][0])[0]
        BC3idx = np.where(geometry.coordinates[:,1]<=diffEquation.BC[2][3])[0]
        BCidx = [BC1idx,BC2idx,BC3idx]
    return BCidx

def SetupODEBC2D(pDDOOperator,geometry,diffEquation):
    n1order = pDDOOperator.n1order
    n2order = pDDOOperator.n2order
    morder = pDDOOperator.morder
    asymFlag = pDDOOperator.asymFlag
    nsize = getSize2D(n1order, n2order)
    BCidx = extractBoundaries(diffEquation, geometry, morder)
    numBC = diffEquation.numBC
    SpSysBCMat = np.zeros((numBC, geometry.totalNodes))
    for iBC in range(numBC):
        #if iBC==3:
        #    currentBCNodes = BCidx[iBC]+
        print(currentBCNodes)
        n1 = diffEquation.BC[iBC][5]
        n2 = diffEquation.BC[iBC][6]
        coef = diffEquation.BC[iBC][7]
        print(n1)
        print(n2)
        print(coef)
        a = input('').split(" ")[0]
        for iCurrentNode in currentBCNodes:
            diffAMat = PDDOFunctions.FormDiffAmat2D(morder, n1order, n2order, iCurrentNode, geometry)
            diffAMat = PDDOFunctions.ApplyConstraintOnAmat2D(asymFlag, n1order, n2order, iCurrentNode, diffAMat, geometry)
            #for iDiff in range(numBC):
            #n1 = diffEquation.BC[iBC][5]
            #n2 = diffEquation.BC[iBC][6]
            #coef = diffEquation.BC[iBC][7]
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
                    #if (math.isnan(gFunVal) != True):
                    SpSysBCMat[iBC][iFamilyMember] += coef*gFunVal*geometry.deltaVolumes[iFamilyMember]/(deltaMag**(n1+n2))
    np.savetxt("C:\\Users\\johnf\\Documents\\Thesis\\PDDOHeatDiffusionEquationPython\\data\\SpSysBCMat.dat",SpSysBCMat,delimiter=",")
    print(SpSysBCMat)
    #print(n2)
    a = input('').split(" ")[0]
    return 0

def SetupODEVecBC2D():
    return 0 
