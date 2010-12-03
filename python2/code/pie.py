"""

Solution to an exercise from
Think Python: An Introduction to Software Design
Allen B. Downey

"""

from TurtleWorld import *

def draw_pie(t, n, r):
    """use Turtle (t) to draw a polypie and then move forward.
    (n) is the number of segments in the pie.
    (r) is the spoke length.
    """
    polypie(t, n, r)
    pu(t)
    fd(t, r*2 + 10)
    pd(t)
    
def polypie(t, n, r):
    """use Turtle (t) to draw a pie with (n) triangular slices with
    spoke length (r).  (n) must be greater than 2.
    (t) ends at the starting position, orientation.
    """
    theta = 360.0 / n
    for i in range(n):
        isosceles(t, r, theta/2)
        lt(t, theta)

def isosceles(t, r, theta):
    """use Turtle (t) to draw an isosceles triangle with leg length
    (r) and peak angle (theta) in degrees.  (t) starts and ends
    at the peak, facing the middle of the base.
    (t) ends at the starting position, orientation.
    """
    y = r * math.sin(theta*math.pi/180)

    rt(t, theta)
    fd(t, r)
    lt(t, 90+theta)
    fd(t, 2*y)
    lt(t, 90+theta)
    fd(t, r)
    lt(t, 180-theta)

# create the world and bob
world = TurtleWorld()
bob = Turtle()
pu(bob)
bk(bob, 130)
pd(bob)

# draw polypies with various number of sides
size = 40
draw_pie(bob, 5, size)
draw_pie(bob, 6, size)
draw_pie(bob, 7, size)
die(bob)

# dump the contents of the campus to the file canvas.eps
world.canvas.dump()

wait_for_user()

