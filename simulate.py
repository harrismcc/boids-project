from vpython import *
import random
import time
from multiprocessing import Pool, Process


from boid import Boid, Phonebook





scene = canvas(title='Examples of Tetrahedrons',
     width=960, height=540,
     center=vector(0,0,0), background=color.cyan)






#create boids
for i in range(200):
    Boid(simpleShape=True)
centerBoid = Boid(debug=False)#create debug boid
predBoid = Boid(predator=True)
predBoid = Boid(predator=True)
predBoid = Boid(predator=True)

#follow mode?
followMode = False
if followMode:
    scene.camera.follow(centerBoid.model) 
    centerBoid.visualModel.opacity = 0.1


#test texture

b = sphere( pos=vec(-1,2,0), radius=80,
      texture={'file':'texture.png'} ) 


def updateFunc(boid, dt):
    boid.update(dt)


RATE = 45
dt = 1.0/(1.0 * RATE)
scene.autoscale = False 
currentTime = time.time()
scene.range = 10
rates = []


start = time.time()
simLength = 0 # in seconds

#main game loop
scene.waitfor('click') #start loop on click
while (time.time() - start) < simLength or simLength == 0:
    rate(RATE) #set rate

    #scene.waitfor('keyup')  #step frame by frame

    #calculate frame rate
    newTime = time.time()
    diff = newTime - currentTime
    if (diff == 0): diff = 0.0001
    currentTime = newTime #update current time
    scene.caption = str( round(1.0 / diff) ) #add frame rate to scene caption
    rates.append(round(1.0 / diff))

    #update neighbor map
    centerBoid.phonebook.updateNeighbors()



    if followMode:
        avgPos = -centerBoid.direction + scene.camera.axis
        avgPos.mag = 1
        scene.camera.axis = avgPos




    #update all boids
    for boid in centerBoid.phonebook.getAllBoids():
        boid.update(dt)



print("Sim done")

print("Average framerate: ", sum(rates) / len(rates))








