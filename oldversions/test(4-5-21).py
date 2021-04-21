from vpython import *
import random
import time

class Boid:
    def __init__(self, allBoids, debug=False):

        self.debug = debug

        #create vpython models
        self.model = cone(pos=vector.random(), axis=vector(0.1,0,0), radius=0.1, opacity=0.0)
        self.visualModel = cone(pos=vector.random(), axis=vector(0.5,0,0), radius=0.25)
        self.model.vel = vector(0,0,0)
        self.direction = vector(0,0,0)
        self.targetDirection = vector(0,0,0) #Direction that the boid WANTS to be moving

        #TODO: these should probably be passed into this class
        self.range = 10 #how far from the center can it travel
        self.speed = 5.0

        #neighbor stuff
        self.allBoids = allBoids
        self.sightRange = 5 #how far can this boid see?
        self.neighbors = self.getVisibleNeighbors()


        #debug stuff
        if self.debug:
            attach_trail(self.model)
            self.debugTargetPointer = arrow(pos=vector(0,2,1), axis=vector(1,0,0), shaftwidth=0.2)
            #self.debugDirectionPointer = arrow(pos=vector(0,2,1), axis=vector(1,0,0), shaftwidth=0)

            self.debugNeighborsPointer = arrow(pos=vector(0,2,1), axis=vector(1,0,0), shaftwidth=0.2, color=color.red)

            self.debugVisSphere = sphere(pos=vector(0,0,0), radius=self.sightRange, opacity=0.2)
        


    def update(self, dt, allBoids):
        """
        The update() function is called each frame to update the position of the boid.
        """

        #update neighbors
        self.allBoids = allBoids
        self.neighbors = self.getVisibleNeighbors()
        #self.neighbors = [self] #disable neighbor behavior entirely

        #Bias direction based on randomness
        if True:
            self.addRandomTargetDirection()


        #Bias direction towards the directions of the neighbors
        if True: 
            avgNeighborDirection = self.getAvgNeighborDirection()
            self.targetDirection = self.adjustDirection(avgNeighborDirection, 0.05) #set direction to that of neighbors


        #Bias direction away from closest neighbor
        if True:
            for neighbor in self.neighbors:
                dist = mag( self.model.pos - neighbor.model.pos )

                if (dist < 0.5):
                    towardsNeighbor = norm(neighbor.model.pos - self.model.pos) #vector pointing towards neighbor
                    self.targetDirection = self.adjustDirection(-towardsNeighbor, 0.5) #adjust position away from the neighbor

        
        
        #Bias direction if boid is outside of range. Bias target direction heavily back towards the center
        if True:
            dist = mag( self.model.pos - vector(0,0,0) ) #distance from center
            if (dist > self.range):

                centerVector = -norm( self.model.pos ) #vector pointing towards origin is just the inverse of the normalized pos
                self.targetDirection = self.adjustDirection(centerVector, 0.2) #set direction twards center


        #Bias movement direction towards the CENTER of the neighbors
        if True:
            positionSum = vector(0,0,0)
            for neighbor in self.neighbors:
                positionSum += neighbor.model.pos
            positionSum = norm(self.model.pos - positionSum)

            if self.debug:
                #arrow(pos=self.model.pos, axis=positionSum, shaftwidth=0.2, color=color.blue)
                pass






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
        self.visualModel.axis.mag = 0.5


        #debug stuff
        if self.debug:
            self.debugTargetPointer.pos = self.model.pos
            self.debugTargetPointer.axis = self.targetDirection

            self.debugNeighborsPointer.pos = self.model.pos
            self.debugNeighborsPointer.axis = self.getAvgNeighborDirection()


            #update vis sphere
            self.debugVisSphere.pos = self.model.pos

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
        randomChange.mag = 0.1 #scale down the amount of change

        self.targetDirection = norm( self.targetDirection + randomChange ) #slightly randomize direction


    def getVisibleNeighbors(self):
        """
        gets all visible neighbors of the current boid

        This runs in O(n) time where n is the number of neighbors
        But realistically the entire neighbor operation is O(n^2) because each
        boid does this for all n neighbors. Maybe there is a way to optimise this?

        TODO: Could this be optimized by adapting a grid system?
        """


        visNeighbors = []

        for boid in self.allBoids:
            #get distance
            dist = mag( self.model.pos - boid.model.pos )
            if dist < self.sightRange:
                #our boid CAN see this one
                visNeighbors.append(boid)

            else:
                #our boid CANT see this one
                pass

        return visNeighbors


    def getAvgNeighborDirection(self):
        """
        Finds the average direction of all the neighbors
        """
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




scene = canvas(title='Examples of Tetrahedrons',
     width=960, height=540,
     center=vector(0,0,0), background=color.cyan)
    


allBoids = []

#create boids
for i in range(0):
    allBoids.append(Boid(allBoids))
allBoids.append(Boid(allBoids, debug=True))#create debug boid



#create bounding box





RATE = 60
dt = 1.0/(1.0 * RATE)
scene.autoscale = False 
currentTime = time.time()
scene.range = 10

#main game loop
scene.waitfor('click') #start loop on click
while True:
    rate(RATE) #set rate

    #scene.waitfor('keyup')  #step frame by frame

    #calculate frame rate
    newTime = time.time()
    diff = newTime - currentTime
    if (diff == 0): diff = 0.0001
    currentTime = newTime #update current time
    scene.caption = str( round(1.0 / diff) ) #add frame rate to scene caption


    #update all boids
    for boid in allBoids:
        boid.update(dt, allBoids)








