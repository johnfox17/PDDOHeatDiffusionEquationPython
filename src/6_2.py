import numpy as np
import PDDODefinitions
import loadInputs
import Geometry
import PDDO

#The objective of this function is to count all the rows of our system
#of equations:
#1. One row for each node and its family members
#2. One row of each BC of a specific node
def getSysMatSize(numBC, totalNodes):
    rows = totalNodes + numBC
    columns = totalNodes + numBC
    return rows, columns

def main():
    #loading input files
    #PDDOOperator, PDGeo, totalNodes = loadInputs.inputForPDDO()
    pDDOOperator, geometry, diffEquation = loadInputs.inputForPDDO() 
    #creating node families
    geometry.nodeFamiliesIdx = geometry.generateNodeFamilies(geometry)
    #get size of system of equations
    diffEquation.rows, diffEquation.columns = getSysMatSize(diffEquation.numBC, geometry.totalNodes)
    #Extract differential equation coefficients
    #coefs =  geometry.extractDiffCoef(PDGeo, totalNodes);
    #for i in range(10):
    #    print(coefs[0])
    #    a = input('').split(" ")[0]
    #TODO
    #aux = PDDO.SetupODEMatrixVector2D(PDDOOperator, Geometry, coefs)

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




