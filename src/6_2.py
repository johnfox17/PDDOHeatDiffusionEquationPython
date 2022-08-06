import numpy as np
import PDDODefinitions
import loadInputs
import geometry
import PDDO

#The objective of this function is to count all the rows of our system
#of equations:
#1. One row for each node and its family members
#2. One row of each BC of a specific node
def getSysMatSize(PDDOOperator, Geometry):
    nwk = 0
    #Row for each node
    for iCurrentNode in range(np.size(Geometry.nodeFamiliesIdx)):
        nwk +=np.size(Geometry.nodeFamiliesIdx[iCurrentNode])-1
    
    print(nwk)
    print(Geometry.totalNodes)
    a = input('').split(" ")[0]
    return

def main():
    #loading input files
    PDDOOperator, PDGeo, totalNodes = loadInputs.inputForPDDO()
    #extracting coordinates and deltas of nodes
    Geometry = geometry.extractCoordinates(PDGeo,totalNodes, PDDOOperator.aType)
    #creating node families
    Geometry.nodeFamiliesIdx = geometry.generateNodeFamilies(Geometry)
    #Extract Boundaries
    Geometry.boundaries = geometry.extractBoundaries(PDDOOperator, Geometry)
    #get size of system of equations
    aux2 = getSysMatSize(PDDOOperator, Geometry)
    #Extract differential equation coefficients
    coefs =  geometry.extractDiffCoef(PDGeo, totalNodes);
    #TODO
    aux = PDDO.SetupODEMatrixVector2D(PDDOOperator, Geometry, coefs)

    #print(nodeFamiliesIdx[0])
    #inputForPDDO()
    #generateNodeFamilies()
    #for i in range(totalNodes):
    #    print(nodeFamiliesIdx[i])
    #    a = input('').split(" ")[0]
    #PDGeomPath = '../data/PDgeom3D.dat'
    #[nodeNum, PDGeo] = loadPDGeom3D(PDGeomPath) 
    #print(nodeNum)
    #print(PDGeo[0])
    #np.savetxt("/home/doctajfox/Documents/Thesis_Research/PDDOHeatDiffusionEquationPython/data/PDGeo5.dat",PDGeo,delimiter=",")



if __name__ == "__main__":
    main()




