from World import *
from math import *
import random
import time

def random_coordinate(limit=1):
    # choose a random number between -limit and limit
    return random.uniform(-limit, limit)

def teleport(a, x, y):
    # move amoeba a to the given location
    a.x = x
    a.y = y
    a.redraw(a.x, a.y)

def randomize(a, limit=10):
    # choose a random location and move the ameoba there
    x = random_coordinate(limit)
    y = random_coordinate(limit)
    teleport(a, x, y)

def move(a, limit=10):
    # move the amoeba by a random amount
    x = a.x + random_coordinate()
    y = a.y + random_coordinate()
    teleport(a, x, y)

def make_amoeba(world, color='violet'):
    # make an amoeba with the given color and randomize it
    a = Amoeba(world)
    a.color1 = color
    randomize(a)
    return a

def main():
    world = AmoebaWorld()

    # make Amy and Bob Amoeba
    amy = make_amoeba(world, 'pink')
    bob = make_amoeba(world, 'light blue')

    # run the loop 1000 times
    for i in range(1000):

        # move the amoebas
        move(amy)
        move(bob)

        # update the world and wait 0.1 seconds
        world.update()
        time.sleep(0.1)

    # wait for the user to close the window
    world.mainloop()

# after all the function definitions, call main to get things started
main()

