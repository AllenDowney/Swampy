"""

Solution to Exercise x.x
Think Python: An Introduction to Software Design
Allen B. Downey

"""

from TurtleWorld import *
from polygon import *

def petal(t, r, angle):
    """Use the Turtle (t) to draw a petal using two arcs
    with the radius (r) and angle.
    """
    for i in range(2):
        arc(t, r, angle)
        lt(t, 180-angle)

def flower(t, n, r, angle):
    """Use the Turtle (t) to draw a flower with (n) petals,
    each with the radius (r) and angle.
    """
    for i in range(n):
        petal(t, r, angle)
        lt(t, 360.0/n)

def move(t, length):
    """Move Turtle (t) forward (length) units without leaving a trail.
    Leaves the pen down.
    """
    pu(t)
    fd(t, length)
    pd(t)

world = TurtleWorld()
bob = Turtle()
bob.delay = 0.01

# draw a sequence of three flowers, as shown in the book.
move(bob, -100)
flower(bob, 7, 60.0, 60.0)

move(bob, 100)
flower(bob, 10, 40.0, 80.0)

move(bob, 100)
flower(bob, 20, 140.0, 20.0)

die(bob)

# dump the contents of the campus to the file canvas.eps
world.canvas.dump()

wait_for_user()
