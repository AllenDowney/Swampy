#!/usr/bin/python

# import everything we need...
from math import *
from random import *
from TurtleWorld import *
from polygon import *
 
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
        return sqrt(self.x**2 + self.y**2)

    # step is invoked whenever the turtle is supposed to move
    def step(self):
        # here is how to invoke a function on a Wanderer
        d = self.distance()
        
        # choose a random direction and turn
        dir = rand_turn(self.clumsiness)
        self.rt(dir)
        
        # move forward according to the speed attribute
        self.fd(self.speed)

        if self.distance() > self.boundary:
            out_of_bounds(self)

def rand_turn(clumsiness):
# choose a random value between -clumsiness and +clumsiness,
# with a tendency toward the middle
    return randint(0,clumsiness) - randint(0,clumsiness)

def out_of_bounds(t):
    # which way is toward the center?
    away = atan2(t.y, t.x) * 180 / pi
    toward = (away + 180) % 360

    # choose two possible headings
    d1 = t.heading + rand_turn(t.clumsiness)
    d2 = t.heading + rand_turn(t.clumsiness)

    # choose the one that is more toward the center
    diff1 = angle_sub(toward, d1)
    diff2 = angle_sub(toward, d2)

    if diff1 < diff2:
        t.heading = d1
    else:
        t.heading = d2

def angle_sub(a1, a2):
# compute the difference between two angles
    a1 = a1%360
    a2 = a2%360
    if a1 < a2:
        a1, a2 = a2, a1
    d = min(a1 - a2, a2 - a1 + 360)
    return d

# create a new TurtleWorld
world = TurtleWorld()

# draw a circle
r = 100
bob = Turtle(world)
bob.delay = 0.001
bob.pu()
bob.fd(r)
bob.lt()
bob.pd()
circle(bob, r)
bob.die()

# add the Run, Stop, Step and Clear buttons
world.setup_run()

# make three Wanderers with different speed and clumsiness attributes
for i in range(1,4):
    w = Wanderer(world, i, i*45)
    w.boundary = r

# tell world to start processing events (button presses, etc)
world.run()
world.mainloop()

