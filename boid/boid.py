from vpython import *
import random
import numpy as np
import time


import boid.vector_shader as vs
from boid.neighbors import Phonebook


class Boid:

    phonebook = Phonebook()

    def __init__(self, configObject):

        

        self.predator = configObject['is_predator']
        self.debug = configObject['debugMode']
        self.id = id(self) #each boid has a unique id

        #add self to phonebook
        self.phonebook.registerBoid(self)

        startingPos = vector.random()
        startingPos.mag = 5
        #create vpython models
       
        self.model = cone(pos=startingPos, axis=vector(0.1,0,0), radius=0.1, opacity=0.0)
        
        
        #construct the visual model
        color=configObject['color']

        if configObject['simpleShape']:
            self.visualModel = ellipsoid(pos=startingPos, length=1, height=0.5, width=0.2, shininess=1.0, color=color)
        else:
            head = ellipsoid(pos=startingPos, length=1, height=0.5, width=0.2, shininess=1.0, color=color) 
            tail = cone(pos=startingPos - vector(0.75, 0, 0 ), axis=vector(0.5,0,0), size=vector(0.5, 0.5, 0.1), shininess=1.0, color=color)
            self.visualModel = compound([head, tail])


        self.model.vel = vector(0,0,0)
        self.direction = vector(0,0,0)
        self.targetDirection = vector(0,0,0) #Direction that the boid WANTS to be moving
        self.addRandomTargetDirection() #Add some starting randomness


        #adjust boid properties
        self.range = configObject['range']
        self.speed = configObject['speed']
        self.visualModel.size.mag = configObject['size']

        #neighbor stuff
        self.sightRange = 4 #how far can this boid see?
        #self.neighbors = self.phonebook.getVisibleNeighbors(self.id)
        self.neighbors = [self]

        #debug stuff
        if self.debug:


            attach_trail(self.model)
            self.debugTargetPointer = arrow(pos=vector(0,2,1), axis=vector(1,0,0), shaftwidth=0.2)
            #self.debugDirectionPointer = arrow(pos=vector(0,2,1), axis=vector(1,0,0), shaftwidth=0)

            self.debugNeighborsPointer = arrow(pos=vector(0,2,1), axis=vector(1,0,0), shaftwidth=0.2)

            self.debugVisSphere = sphere(pos=vector(0,0,0), radius=self.sightRange, opacity=0.2)
        


    def update(self, dt):
        """
        The update() function is called each frame to update the position of the boid.
        """

        #Bypass this update if predator mode
        if self.predator:
            self.updatePredator(dt)
            return

        #update neighbors
        self.neighbors = self.phonebook.getVisibleNeighbors(self.id)

        #Bias direction based on randomness
        if True:
            self.addRandomTargetDirection()


        #Bias direction towards the directions of the neighbors
        if True: 
            avgNeighborDirection = self.getAvgNeighborDirection()
            self.targetDirection = self.adjustDirection(avgNeighborDirection, 0.05) #set direction to that of neighbors

        
        #Bias direction towards the center of the neighbors
        if True:
            center = self.getNeighborCenter()
            towardsCenter = norm(center - self.model.pos) #vector pointing towards the center
            self.targetDirection = self.adjustDirection(towardsCenter , 0.1)
            


        #Bias direction away from closest neighbor
        if True:
            for neighbor in self.neighbors:
                dist = mag( self.model.pos - neighbor.model.pos )

                if (dist < 1.5):
                    towardsNeighbor = norm(neighbor.model.pos - self.model.pos) #vector pointing towards neighbor
                    self.targetDirection = self.adjustDirection(-towardsNeighbor, (1.5 - dist)/2) #adjust position away from the neighbor, with strength inversly proportional to the distance

        
        
        #Bias direction if boid is outside of range. Bias target direction heavily back towards the center
        if True:
            dist = mag( self.model.pos - vector(0,0,0) ) #distance from center
            biasAmount = (dist - self.range) * 0.1
            if (dist > self.range):

                centerVector = -norm( self.model.pos ) #vector pointing towards origin is just the inverse of the normalized pos
                self.targetDirection = self.adjustDirection(centerVector, biasAmount) #set direction twards center

        
        #Bias direction away from predator
        if True:

            for key in self.phonebook.predatorPos:
                currentPos = self.phonebook.predatorPos[key]
                point1 = vs.vector_to_numpy(self.model.pos)
                point2 = vs.vector_to_numpy(currentPos)
                dist = vs.get_distance(point1, point2)
                if dist < 5.0:
                    away = -norm(currentPos  - self.model.pos) #Vector pointing away from predator
                    if self.debug: arrow(pos=self.model.pos, axis=away, shaftwidth=0.2)
                    self.targetDirection = self.adjustDirection(away , 1.0)









        ##### Apply behaviors to direction and velocity #####

        #set velocity based on target direction
        self.model.vel = rotate(self.targetDirection, angle=0) #rotate velocity based on target direction
        self.model.vel.mag = self.speed #make sure the boid keeps speed

        #set direction
        newPos = self.model.pos + self.model.vel*dt 
        self.direction = norm(self.model.pos - newPos)
        #update position
        self.model.pos = newPos
        #rotate to face direction
        self.model.rotate(angle=0, axis=self.direction)



        #update visual model
        self.visualModel.pos = self.model.pos
        self.visualModel.axis = norm(self.model.vel)
        #self.visualModel.axis.mag = 0.5


        #debug stuff
        if self.debug:
            self.debugTargetPointer.pos = self.model.pos
            self.debugTargetPointer.axis = self.targetDirection

            self.debugNeighborsPointer.pos = self.model.pos
            self.debugNeighborsPointer.axis = self.getAvgNeighborDirection()


            #update vis sphere
            self.debugVisSphere.pos = self.model.pos


    def updatePredator(self, dt):
        """An update function just for predators"""
        
        
        
        #update predator pos for all to see
        self.phonebook.predatorPos[self.id] = self.model.pos

        #Bias direction based on randomness
        if True:
            self.addRandomTargetDirection()

        #Bias direction towards nearest neighbor
        if True:

            nearestDist = 9999
            nearestPos = self.model.pos
            for neighbor in self.phonebook.getAllBoids():
                point1 = vs.vector_to_numpy(self.model.pos)
                point2 = vs.vector_to_numpy(neighbor.model.pos)
                dist = vs.get_distance(point1, point2)

                if dist < nearestDist and dist > 0 and neighbor.predator == False:
                    nearestDist = dist
                    nearestPos = neighbor.model.pos


            targetVector = norm(nearestPos - self.model.pos)
            self.targetDirection = self.adjustDirection( targetVector  , 0.2)


        #Bias direction if boid is outside of range. Bias target direction heavily back towards the center
        if True:
            dist = mag( self.model.pos - vector(0,0,0) ) #distance from center
            biasAmount = (dist - self.range) * 0.1
            if (dist > self.range):

                centerVector = -norm( self.model.pos ) #vector pointing towards origin is just the inverse of the normalized pos
                self.targetDirection = self.adjustDirection(centerVector, biasAmount) #set direction twards center

                


        ##### Apply behaviors to direction and velocity #####
        #set velocity based on target direction
        self.model.vel = rotate(self.targetDirection, angle=0) #rotate velocity based on target direction
        self.model.vel.mag = self.speed #make sure the boid keeps speed

        #set direction
        newPos = self.model.pos + self.model.vel*dt 
        self.direction = norm(self.model.pos - newPos)
        #update position
        self.model.pos = newPos
        #rotate to face direction
        self.model.rotate(angle=0, axis=self.direction)



        #update visual model
        self.visualModel.pos = self.model.pos
        self.visualModel.axis = norm(self.model.vel)
        #self.visualModel.axis.mag = 0.5


    def adjustDirection(self, target, maxChange):
        """
        Adjust direction towards a target without exceeding the max change
        """
        target.mag = maxChange #scale down the target
        newDirection = norm( self.targetDirection + target ) #add a bit of the neighbor target to my target
        return newDirection
        

    def addRandomTargetDirection(self):
        """
        Adds a random movement to the target direction, scaled down to 0.1 (10%)
        """
        randomChange = vector.random()

        #1 in 10 change of big change
        if random.randint(1, 11) == 1:
            randomChange.mag = 0.5 #scale down the amount of change
        else:
            randomChange.mag = 0.1 #scale down the amount of change

        self.targetDirection = norm( self.targetDirection + randomChange ) #slightly randomize direction



    def getAvgNeighborDirection(self):
        """
        Finds the average direction of all the neighbors
        """


        '''
        directionArray = np.empty([0, 3])
        for neighbor in self.neighbors:
            directionArray = np.vstack([ directionArray , vs.vector_to_numpy(neighbor.direction) ])

        avg = vs.getAvgDirectionOfVectors(directionArray)

        return vs.numpy_to_vector(avg)

        '''

        sumDirection = vector(0,0,0)
        sumMagnitude = 0
        count = 0


        for neighbor in self.neighbors:
            sumDirection += neighbor.direction
            sumMagnitude += neighbor.model.vel.mag
            count += 1

        averageMag = sumMagnitude / count

        sumDirection.mag = -averageMag

        return sumDirection



    def getNeighborCenter(self):

        sumVector = vector(0,0,0)
        for neighbor in self.neighbors:
            sumVector += neighbor.model.pos


        x = sumVector.x / len(self.neighbors)
        y = sumVector.y / len(self.neighbors)
        z = sumVector.z / len(self.neighbors)

        return vector(x,y,z)
            



        


