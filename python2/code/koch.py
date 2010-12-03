"""

Solution to the Koch curve exercise.
Think Python: An Introduction to Software Design
Allen B. Downey

"""

from TurtleWorld import *

world = TurtleWorld()
bob = Turtle()
bob.delay = 0

bob.x = -150
bob.y = 90
bob.redraw()

def koch(t, n):
    if n<3:
        fd(t, n)
        return
    m = n/3.0
    koch(t, m)
    lt(t, 60)
    koch(t, m)
    rt(t, 120)
    koch(t, m)
    lt(t, 60)
    koch(t, m)

def snowflake(t, n):
    for i in range(3):
        koch(t, n)
        rt(t, 120)

snowflake(bob, 300)
die(bob)

world.canvas.dump()
world.mainloop()
