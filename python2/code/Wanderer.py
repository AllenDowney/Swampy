#!/usr/bin/python

# import everything we need from World.py...
from TurtleWorld import *

# and everything from the random module
from random import *

# a Wanderer is a kind of turtle
class Wanderer(Turtle):

    # this is the function that creates new turtles.
    # the first parameter is the new turtle itself,
    # which is provided automatically when we invoke
    # Wanderer()
    def __init__(self, world, speed=1, clumsiness=60):
        Turtle.__init__(self, world)
        self.delay = 0
        # speed is the distance the Wanderer moves per step
        self.speed = speed
        # clumsiness determines the ability of the Wanderer to
        # track a straight line
        self.clumsiness = clumsiness
        # turtles start out facing in a random direction
        self.rt(randint(0,360))

    # distance is a function that can be invoked on a Wanderer
    # it is supposed to return the distance to the origin
    def distance(self):
        # change the following line to compute distance correctly
        return self.x + self.y

    # step is invoked whenever the turtle is supposed to move
    def step(self):
        # here is how to invoke a function on a Wanderer
        d = self.distance()
        
        # choose a random direction and turn
        dir = randint(0,self.clumsiness) - randint(0,self.clumsiness)
        self.rt(dir)
        
        # move forward according to the speed attribute
        self.fd(self.speed)

# create a new TurtleWorld
world = TurtleWorld()

# add the Run, Stop, Step and Clear buttons
world.setup_run()

# make three Wanderers with different speed and clumsiness attributes
for i in range(1,4):
    Wanderer(world, i, i*45)

# tell world to start processing events (button presses, etc)
world.mainloop()

