import numpy as np
import PDDODefinitions
import loadInputs
import geometry




def main():
    #loading input files
    PDDOoperator, PDGeo, totalNodes = loadInputs.inputForPDDO()
    #extracting coordinates and deltas of nodes
    coordinates, deltas = geometry.extractCoordinates(PDGeo,totalNodes, PDDOoperator.aType)
    #creating node families
    nodeFamiliesIdx = geometry.generateNodeFamilies(coordinates, deltas)
    #TODO
    #SetupODEMatrixVector2D

    print(nodeFamiliesIdx[0])
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




