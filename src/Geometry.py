import numpy as np
import sklearn
import math
from sklearn.neighbors import KDTree
import PDDODefinitions


def generateNodeFamilies(Geometry):
    #since in this case all horizons are equal for all nodes but must change later to generalize
    #when horizon variables between nodes
    delta_mag = math.sqrt(Geometry.deltaCoordinates[0][0]**2+Geometry.deltaCoordinates[0][1]**2+Geometry.deltaCoordinates[0][2]**2)
    X = Geometry.coordinates[:,:3]
    tree = KDTree(X, leaf_size=2)
    nodeFamiliesIdx, dist = tree.query_radius(X, r = delta_mag, sort_results=True, return_distance=True)
    
    asymFam = True
    nodeFamilies = []
    if asymFam == True:
        for iCurrentNode in range(Geometry.totalNodes):
            idx= np.where(Geometry.coordinates[nodeFamiliesIdx[iCurrentNode]][:,1]<=Geometry.coordinates[iCurrentNode][1])
            nodeFamilies.append(nodeFamiliesIdx[iCurrentNode][idx])
    else:
        nodeFamilie = nodeFamiliesIdx
    return nodeFamilies

def extractBoundaries(PDDOOperator, Geometry):
    morder = PDDOOperator.morder
    BCidx = []
    if morder==2: #I hard coded it here need to find a way to loop through BCs
        BC1idx = np.where ( Geometry.coordinates[:,0]<=PDDOOperator.BC[0][1])[0]
        BC2idx = np.where ( Geometry.coordinates[:,0]>=PDDOOperator.BC[1][0])[0]
        BC3idx = np.where(Geometry.coordinates[:,1]<=PDDOOperator.BC[2][3])[0]
        BCidx = [BC1idx,BC2idx,BC3idx]
    return BCidx
