import time, random
from math import *
from World import *

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

def make_amoeba(world, color='violet'):
    # make an amoeba with the given color and randomize it
    a = Amoeba(world)
    a.color1 = color
    randomize(a)
    return a

def distance(a, b):
    # compute the distance between amoebas
    dx = a.x - b.x
    dy = a.y - b.y
    return sqrt(dx*dx + dy*dy)

def bound(x, limit):
    # make sure that x is between -limit and +limit
    if x > limit: x = limit
    if x < -limit: x = -limit
    return x

def move(a, limit=10):
    # move the amoeba by a random amount
    x = a.x + random_coordinate(1)
    y = a.y + random_coordinate(1)

    x = bound(x, limit)
    y = bound(y, limit)
    teleport(a, x, y)

def nudge(a, b, fraction=0.02):
    # move a just a little bit closer to b
    dx = a.x - b.x
    a.x -= dx * fraction
    dy = a.y - b.y
    a.y -= dy * fraction

def main(n=1000):
    world = AmoebaWorld()

    # make Amy and Bob Amoeba
    amy = make_amoeba(world, 'pink')
    bob = make_amoeba(world, 'light blue')

    # run the loop n times
    for i in range(n):

        # move the amoebas
        move(amy)
        move(bob)

        nudge(amy, bob)
        nudge(bob, amy)

        d = distance(amy, bob)
        if d<1.0:
            mate(amy, bob, world, n-i)

        # update the world and wait 0.1 seconds
        world.update()
        time.sleep(0.1)

    # wait for the user to close the window
    world.mainloop()


def mate(amy, bob, world, n):
    # merge the amoebas into one big amoeba
    bob.undraw()
    amy.color1='violet'
    amy.size *= 2**0.333

    # finish the loop
    for i in range(n):
        move(amy)
        world.update()
        time.sleep(0.1)


# after all the function definitions, call main to get things started
main()

