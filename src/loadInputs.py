import numpy as np
import sklearn
from sklearn.neighbors import KDTree
import PDDODefinitions

inputsPath = "../inputs/"

def loadPDGeoInput():
    PDGeoInput = str(inputsPath + "PDgeom2D.dat")
    with open(PDGeoInput, newline='\n') as fp:
        PDGeo = []
        totalNodes = int(fp.readline())
        for i in range(totalNodes):
            line = list(map(float,fp.readline().split()))
            PDGeo.append(line)
    PDGeo = np.array(PDGeo)
    return PDGeo, totalNodes

def inputForPDDO():
    PDoprInput = inputsPath + "PDopr.inp"
    PDDOoperator = PDDODefinitions.PDDOOperator() 
    with open(PDoprInput) as fp:
        line = fp.readline() #file name
        PDGeoFileName = fp.readline() #file name
        line = fp.readline() #atype, morder, n1order, n2order, n3order, timeFlag, ftype
        line = fp.readline().split()
        PDDOoperator.aType = int(line[0])
        PDDOoperator.morder = int(line[1])
        PDDOoperator.n1order = int(line[2])
        PDDOoperator.n2order = int(line[3])
        PDDOoperator.n3order = int(line[4])
        PDDOoperator.nskip = int(line[5])
        line = fp.readline() #number of diff. operators
        PDDOoperator.numDiffOps = int(fp.readline())
        line = fp.readline() #n1
        if PDDOoperator.numDiffOps > 0:
            numberDiffOperators = []
            for i in range(PDDOoperator.numDiffOps):
                line = fp.readline().split()
                numberDiffOperators.append(list(map(int,line)))
            PDDOoperator.diffOps = numberDiffOperators
        line = fp.readline() #num of bc
        PDDOoperator.numBC = int(fp.readline())
        BC = []
        if PDDOoperator.numBC > 0:
            for i in range(PDDOoperator.numBC):
                aux = []
                line = fp.readline() #bc1: xmin, xmax, ymin, ymax, num_diff_ops \ n1(1), n2(1), coef(1), ..., val
                line = fp.readline().split()
                for j in range(len(line)):
                    aux.append(float(line[j].replace("d","e")))
                line = fp.readline().split()
                for j in range(len(line)):
                    aux.append(float(line[j].replace("d","e")))
                BC.append(aux)
            PDDOoperator.BC = BC
        line = fp.readline() #nout
        PDDOoperator.nout = int(fp.readline())
        if PDDOoperator.nout>0:
            line = fp.readline() #n1
            numOut = []
            for i in range(PDDOoperator.nout):
                line = fp.readline().split()
                numOut.append(list(map(int,line)))
            PDDOoperator.numOut = numOut
        PDGeo, totalNodes = loadPDGeoInput()
        return PDDOoperator, PDGeo, totalNodes 
