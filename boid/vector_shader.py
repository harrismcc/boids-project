from vpython import *
import numpy as np




def vector_to_numpy(vector):
    return np.array((vector.x, vector.y, vector.z), dtype=np.single)


def numpy_to_vector(array):
    return vector(array[0], array[1], array[2])

def get_distance(point1, point2):

    # subtracting vector
    temp = point1 - point2
    
    # doing dot product
    # for finding
    # sum of the squares
    sum_sq = np.dot(temp.T, temp)
    
    # Doing squareroot and
    # return Euclidean distance
    return np.sqrt(sum_sq)

def getAvgDirectionOfVectors(vectorArray):
    '''finds the average of a numpy array'''
    return np.mean(vectorArray, axis=0)



