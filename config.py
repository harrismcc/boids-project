from vpython import vector

""" Simulation Configuration """

#Boids
NUM_BOIDS = 300
DEBUG_BOID = False
NUM_PREDATORS = 3

#Camera & Scene
SCENE_WIDTH = 1920 #960
SCENE_HEIGHT = 1080 #540
CAMERA_FOLLOW_MODE = False
MAX_FRAMERATE = 45
SIM_LENGTH = 0 #Set to 0 seconds for sim to run forever



""" Boid Configuration """

BOID_CONFIG = {
    'color' : vector(1,0,1),
    'simpleShape' : True,
    'range' : 10.0,
    'speed' : 10.0,
    'size' : 1.0,
    'is_predator' : False,
    'debugMode' : False,
}

PREDATOR_CONFIG = {
    'color' : vector(1,1,0),
    'simpleShape' : True,
    'range' : 11.0,
    'speed' : 9.0,
    'size' : 3.0,
    'is_predator' : True,
    'debugMode' : False,
}
