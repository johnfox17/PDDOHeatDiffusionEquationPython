import numpy as np
import sklearn
import math
from sklearn.neighbors import KDTree
import PDDODefinitions


def generateNodeFamilies(geometry):
    #since in this case all horizons are equal for all nodes but must change later to generalize
    #when horizon variables between nodes
    delta_mag = math.sqrt(geometry.deltaCoordinates[0][0]**2+geometry.deltaCoordinates[0][1]**2+geometry.deltaCoordinates[0][2]**2)
    X = geometry.coordinates[:,:3]
    tree = KDTree(X, leaf_size=2)
    nodeFamiliesIdx, dist = tree.query_radius(X, r = delta_mag, sort_results=True, return_distance=True)
    asymFam = True
    eliminateBottomNodes = True
    nodeFamilies = []
    if asymFam == True:
        for iCurrentNode in range(geometry.totalNodes):
            idx= np.where(geometry.coordinates[nodeFamiliesIdx[iCurrentNode]][:,1]<=geometry.coordinates[iCurrentNode][1])
            nodeFamilies.append(nodeFamiliesIdx[iCurrentNode][idx])
    else:
        nodeFamilies = nodeFamiliesIdx

    return nodeFamilies



