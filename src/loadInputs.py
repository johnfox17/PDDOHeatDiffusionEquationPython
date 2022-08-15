import numpy as np
import sklearn
from sklearn.neighbors import KDTree
import PDDODefinitions

inputsPath = "../inputs/"

def extractDiffCoef(PDGeo, totalNodes):
    coef = []
    for i in range(totalNodes):
        coef.append([PDGeo[i][7], PDGeo[i][8], PDGeo[i][9]])
    return np.array(coef)


def extractCoordinates(PDGeo,totalNodes, aType):
    Geometry =  PDDODefinitions.Geometry()
    coordinates = []
    deltaVolumes = []
    deltaCoordinates = []
    if aType == 0 :
        for i in range(totalNodes):
            coordinates.append([PDGeo[i][0], PDGeo[i][1], PDGeo[i][2]])
            deltaVolumes.append(PDGeo[i][3])
            deltaCoordinates.append(PDGeo[i][4])
    else:
         for i in range(totalNodes):
            coordinates.append([PDGeo[i][0], PDGeo[i][1], PDGeo[i][2]])
            deltaVolumes.append(PDGeo[i][3])
            deltaCoordinates.append([PDGeo[i][4],  PDGeo[i][5],  PDGeo[i][6]])
            Geometry.totalNodes = totalNodes
            Geometry.coordinates = np.array(coordinates)
            Geometry.deltaVolumes = np.array(deltaVolumes)
            Geometry.deltaCoordinates = np.array(deltaCoordinates)
    return Geometry

def loadPDGeoInput(pDDOOperator):
    PDGeoInput = str(inputsPath + "PDgeom2D.dat")
    with open(PDGeoInput, newline='\n') as fp:
        PDGeo = []
        totalNodes = int(fp.readline())
        for i in range(totalNodes):
            line = list(map(float,fp.readline().split()))
            PDGeo.append(line)
    PDGeo = np.array(PDGeo)
    Geometry = extractCoordinates(PDGeo,totalNodes, pDDOOperator.aType)
    return Geometry, PDGeo

def inputForPDDO():
    PDoprInput = inputsPath + "PDopr.inp"
    pDDOoperator = PDDODefinitions.PDDOOperator()
    diffEquation = PDDODefinitions.DiffEquation()

    with open(PDoprInput) as fp:
        line = fp.readline() #file name
        PDGeoFileName = fp.readline() #file name
        line = fp.readline() #atype, morder, n1order, n2order, n3order, timeFlag, ftype
        line = fp.readline().split()
        pDDOoperator.aType = int(line[0])
        pDDOoperator.morder = int(line[1])
        pDDOoperator.n1order = int(line[2])
        pDDOoperator.n2order = int(line[3])
        pDDOoperator.n3order = int(line[4])
        pDDOoperator.asymFlag = int(line[5])
        line = fp.readline() #number of diff. operators
        pDDOoperator.numDiffOps = int(fp.readline())
        line = fp.readline() #n1
        if pDDOoperator.numDiffOps > 0:
            numberDiffOperators = []
            for i in range(pDDOoperator.numDiffOps):
                line = fp.readline().split()
                numberDiffOperators.append(list(map(int,line)))
            pDDOoperator.diffOps = numberDiffOperators
        line = fp.readline() #num of bc
        diffEquation.numBC = int(fp.readline())
        BC = []
        if diffEquation.numBC > 0:
            for i in range(diffEquation.numBC):
                aux = []
                line = fp.readline() #bc1: xmin, xmax, ymin, ymax, num_diff_ops \ n1(1), n2(1), coef(1), ..., val
                line = fp.readline().split()
                for j in range(len(line)):
                    aux.append(float(line[j].replace("d","e")))
                line = fp.readline().split()
                for j in range(len(line)):
                    aux.append(float(line[j].replace("d","e")))
                BC.append(aux)
            diffEquation.BC = BC
        line = fp.readline() #nout
        pDDOoperator.nout = int(fp.readline())
        if pDDOoperator.nout>0:
            line = fp.readline() #n1
            numOut = []
            for i in range(pDDOoperator.nout):
                line = fp.readline().split()
                numOut.append(list(map(int,line)))
            pDDOoperator.numOut = numOut
        geometry, PDGeo = loadPDGeoInput(pDDOoperator)
        diffEquation.coefs =  extractDiffCoef(PDGeo, geometry.totalNodes);
        return pDDOoperator, geometry, diffEquation 
