from vpython import *
import random
import time
from multiprocessing import Pool, Process, freeze_support


from boid import Boid, Phonebook
from config import *



#Create Scene
scene = canvas(title='Boids Simulation',
     width=SCENE_WIDTH, height=SCENE_HEIGHT,
     center=vector(0,0,0), background=color.cyan)



#create boids
for i in range(NUM_BOIDS):
    Boid(BOID_CONFIG,)
centerBoid = Boid(BOID_CONFIG)#create debug/center boid

for i in range(NUM_PREDATORS):
    predBoid = Boid(PREDATOR_CONFIG)


#follow mode?
if CAMERA_FOLLOW_MODE:
    scene.camera.follow(centerBoid.model) 
    centerBoid.visualModel.opacity = 0.1


#test texture

b = sphere( pos=vec(-1,2,0), radius=80,
      texture={'file':'texture.png'} ) 


#Create UI Elements

def update_value(attr, value, centerBoid):
    for boid in centerBoid.phonebook.getAllBoids():
        setattr(boid, attr, value)

def speed_slider(s):
    #Update speed
    update_value('speed', s.value, s.centerBoid)


scene.append_to_caption('\n\n')
scene.append_to_caption('Boid Speed:')
slider( bind=speed_slider, min=0.0, max=15.0, step=0.5, value=BOID_CONFIG['speed'], centerBoid=centerBoid )
scene.append_to_caption('\n\n')
def B(b):
    predBoid = Boid(PREDATOR_CONFIG)
button( bind=B, text='Add Predator!' )
scene.append_to_caption('\n\n')


RATE = MAX_FRAMERATE
dt = 1.0/(1.0 * RATE)
scene.autoscale = False 
currentTime = time.time()
scene.range = 10
rates = []


start = time.time()
simLength = SIM_LENGTH # in seconds


#main game loop
scene.waitfor('click') #start loop on click
while (time.time() - start) < simLength or simLength == 0:
    rate(RATE) #set rate


    #calculate frame rate
    newTime = time.time()
    diff = newTime - currentTime
    if (diff == 0): diff = 0.0001
    currentTime = newTime #update current time
    #scene.caption = str( round(1.0 / diff) ) #add frame rate to scene caption
    rates.append(round(1.0 / diff))

    #update neighbor map
    centerBoid.phonebook.updateNeighbors()



    if CAMERA_FOLLOW_MODE:
        avgPos = -centerBoid.direction + scene.camera.axis
        avgPos.mag = 1
        scene.camera.axis = avgPos



    #update all boids
    for boid in centerBoid.phonebook.getAllBoids():
        boid.update(dt)



print("Sim done")
print("Average framerate: ", sum(rates) / len(rates))








