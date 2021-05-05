# Boids!

## Motivation
In 1986, Computer Scientist and Computer Graphics Researchers Craig Reynolds created the famous 'Boids' simulation. Inspired by other artificial life programs, like Conway's Game of Life, Reynolds' Boids program simulated the flocking behavior of birds. Since then, hundreds of programs have emerged both expanding on his origional work, and creating entirely new artificial life simulations.

For this project, I wanted to create my own version of the Boids program - this time to simulate the behavior of flocking fish. Although accurate to Reynolds' origional design, my program also takes some creative liberties to make sure that the simulation is both visually appealing and accurate.


## Running my Simulation

First, make sure that you have all of the requiremnts installed from `requirements.txt`. For most, this can be done using the command `pip install -r requirements.txt` from inside the project directory.

After the requirements are installed, the simulation can be run using `python simulate.py`. This should open up a browser window with the simulation, click the main window to start the simulation.

Simulation parameters like the number of boids, number of predators, and many more can be changed in `config.py`.


## Examples
***GIF framerates are low here, click on image for better view. Download and run codebase for best results!***
#### 300 Boids with 3 Predators
![300 Boids with 3 Predators GIF](/examples/300Boids3Predators.gif)

#### 300 Boids
![300 Boids GIF](/examples/300Boids.gif)

#### 500 Boids
![500 Boids GIF](/examples/500Boids.gif)
