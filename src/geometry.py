import numpy as np
import sklearn
import math
from sklearn.neighbors import KDTree
import PDDODefinitions

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


def generateNodeFamilies(Geometry):
    #since in this case all horizons are equal for all nodes but must change later to generalize
    #when horizon variables between nodes
    delta_mag = math.sqrt(Geometry.deltaCoordinates[0][0]**2+Geometry.deltaCoordinates[0][1]**2+Geometry.deltaCoordinates[0][2]**2)
    X = Geometry.coordinates[:,:3]
    tree = KDTree(X, leaf_size=2)
    nodeFamiliesIdx, dist = tree.query_radius(X, r = delta_mag, sort_results=True, return_distance=True)
    return nodeFamiliesIdx

def extractBoundaries(PDDOOperator, Geometry):
    morder = PDDOOperator.morder
    BCidx = []
    if morder==2: #I hard coded it here need to find a way to loop through BCs
        BC1idx = np.where ( Geometry.coordinates[:,0]<=PDDOOperator.BC[0][1])[0]
        BC2idx = np.where ( Geometry.coordinates[:,0]>=PDDOOperator.BC[1][0])[0]
        BC3idx = np.where(Geometry.coordinates[:,1]<=PDDOOperator.BC[2][3])[0]
        BCidx = [BC1idx,BC2idx,BC3idx]
    return BCidx
