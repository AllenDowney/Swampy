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

def make_amoeba(world, name='', color1='violet'):
    # make an amoeba with the given color and randomize it
    a = Amoeba(world)
    a.name = name
    a.color1 = color1
    a.spouse = None
    a.juvenile = False
    randomize(a)
    return a

def check_collisions(a, world):
    for other in world.animals:
        if other is a: continue
        d = distance(a, other)
        if d < 1.0:
            collide(a, other, world)
            
def collide(a, b, world):
    print a.name, 'and', b.name, 'collided.'
    
    if a.juvenile or b.juvenile: return
    
    if are_married(a, b):
        c = make_amoeba(world, 'baby', 'yellow')
        c.size = a.size / 2
        c.juvenile = True
        c.crush = a
    
    if a.spouse == None and b.spouse == None:
        marry(a, b)
    
def marry(a, b):
    print a.name, 'and', b.name, 'are married.'
    a.spouse = b
    a.color2 = 'purple'
    b.spouse = a
    b.color2 = 'purple'

def are_married(a, b):
    try:
        return a.spouse is b and b.spouse is a
    except:
        return False

def main(n=200):
    world = AmoebaWorld()

    # make Amy and Bob Amoeba
    amy = make_amoeba(world, 'amy', 'pink')
    bob = make_amoeba(world, 'bob', 'light blue')
    pat = make_amoeba(world, 'pat', 'chartreuse')

    amy.crush = bob
    bob.crush = pat
    pat.crush = amy
    
    # run the loop n times
    for i in range(n):

        # move the amoebas
        for amoeba in world.animals:
            move(amoeba)
            nudge(amoeba, amoeba.crush)
            check_collisions(amoeba, world)

        # update the world and wait 0.1 seconds
        world.update()
        time.sleep(0.1)

    # wait for the user to close the window
    world.mainloop()

# after all the function definitions, call main to get things started
main()

