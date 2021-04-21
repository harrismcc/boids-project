"""
This file handles the neighbor calculations for the simulation. By offloading the calculation to a central process instead
of each boid, optimizations can be made more easily.
"""
from vpython import *
import math
import numpy as np
from sklearn.neighbors import KDTree
import boid.vector_shader as vs





class Phonebook:
    """The phonebook is the datastructure that allows boids to search for their neighbors"""
    def __init__(self):
        
        
        self.allBoids = {} #mapping of boid id to boid
        self.predatorPos = {}

        self.nn_map = {}


        self.neighborsMap = {} #maps boid id to all of it's neighbors
        self.updateNeighbors()

        self.cordMap = {} #Maps (x, y, z) -> boidId[]
        self.boidCordMap = {}



    def registerBoid(self, boid):
        if (boid.id not in self.allBoids.keys()):
            self.allBoids[boid.id] = boid
        else:
            raise Exception("Boid already in Phonebook")


    def getBoid(self, id):
        return self.allBoids[id]


    def getAllBoids(self):
        """returns a list of all boids"""
        out = []
        for key in self.allBoids.keys():
            out.append(self.allBoids[key])
        return out

    def getVisibleNeighbors(self, boidId):
        return self.neighborsMap[boidId]

    def getVisibleNeighborsOld(self, boidId):
        """
        gets all visible neighbors of the current boid

        This runs in O(n) time where n is the number of neighbors
        But realistically the entire neighbor operation is O(n^2) because each
        boid does this for all n neighbors. Maybe there is a way to optimise this?

        TODO: Could this be optimized by adapting a grid system?
        """

        currentBoid = self.getBoid(boidId)
        if (currentBoid is None):
            return []


        
        if (boidId in self.neighborsMap.keys()):
            #no need to recalculate
            return self.neighborsMap[boidId]
        else:
            visNeighbors = []
            for key in self.allBoids.keys():
                
                boid = self.getBoid(key)

                

                point1 = vs.vector_to_numpy(currentBoid.model.pos)
                point2 = vs.vector_to_numpy(boid.model.pos)


                #get Distance
                dist = vs.get_distance(point1, point2)

                if dist < currentBoid.sightRange:
                    #our boid CAN see this one
                    visNeighbors.append(boid)

                else:
                    #our boid CANT see this one
                    pass
           

            return visNeighbors
            


    def idsToBoids(self, idList):
        """Converts a list of id's to a list of boids"""
        return [self.getBoid(key) for key in idList]
    
    def vector_to_list(self, vector):
        return [vector.x, vector.y, vector.z]


    def list_to_vector(self, list):
        return vector(list[0], list[1], list[2])

    def updateKDTree(self):

        self.nn_map = {} #reset the nn_map

        points = []
        ids = []
        for boid in self.getAllBoids():
            points.append( self.vector_to_list(boid.model.pos) )
            ids.append(boid.id)
            

        
        
        if points == []: return

        tree = KDTree(points, leaf_size=4)
        all_nn_indices = tree.query_radius(points, r=3)  # NNs within distance of 1.5 of point


        for i, nn_indices in enumerate(all_nn_indices):

            currentId = ids[i]
            posList = [points[idx] for idx in nn_indices]
            idList = [ids[idx] for idx in nn_indices]

            self.nn_map[currentId] = {
                'idList' : idList,
                'posList' : posList
            }         
            

        

                
        


    def updateNeighbors(self):
        """For all boids in the scene, update the neighbors map to contain their visible neighbors"""
        

        self.updateKDTree() #test the kdTree

        for key in self.allBoids.keys():

            neighbors = self.idsToBoids(self.nn_map[key]["idList"])
            self.neighborsMap[key] = neighbors
      

                #update neighbors old
                #self.neighborsMap[key] = self.getVisibleNeighbors(key)




