import numpy as np
import sklearn
import math
from sklearn.neighbors import KDTree

def extractCoordinates(PDGeo,totalNodes, aType):
    coordinates = []
    deltas = []
    if aType == 0 :
        for i in range(totalNodes):
            coordinates.append([PDGeo[i][0], PDGeo[i][1], PDGeo[i][2]])
            deltas.append([PDGeo[i][3], PDGeo[i][4]])

    else:
        for i in range(totalNodes):
            coordinates.append([PDGeo[i][0], PDGeo[i][1], PDGeo[i][2]])
            deltas.append([PDGeo[i][3], PDGeo[i][4],  PDGeo[i][5],  PDGeo[i][6]])
    coordinates = np.array(coordinates)
    deltas = np.array(deltas)
    return coordinates, deltas


def generateNodeFamilies(coordinates, deltas):
    #since in this case all horizons are equal for all nodes but must change later to generalize
    #when horizon variables between nodes
    delta_mag = math.sqrt(deltas[0][1]**2+deltas[0][2]**2+deltas[0][3]**2)
    X = coordinates[:,:3]
    tree = KDTree(X, leaf_size=2)
    nodeFamiliesIdx, dist = tree.query_radius(X, r = delta_mag, sort_results=True, return_distance=True)
    return nodeFamiliesIdx
