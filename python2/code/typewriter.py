"""

Solution to the letter-drawing exercise.
Think Python: An Introduction to Software Design
Allen B. Downey


This file contains code that might be useful for debugging
letter-drawing code.  The file letters.py should contain
functions named draw_a, draw_b, etc.

This program imports the functions from letters.py and uses
them to implement a turtle typewriter.

"""

from letters import *

# the following is the code for the turtle typewriter.
# it uses some features we haven't seen yet.

def teleport(t, x, y):
    """move the turtle to a position in absolute coordinates"""

    # This is an example of a function that breaks the layer
    # of abstraction provided by the Level 0 primitives!
    # It takes advantage of details of the implemention that
    # should probably not be considered 'public'
    t.x = x
    t.y = y
    t.redraw()

def keypress(event):
    # this function gets called when the user presses a key.
    # the following try statement is a hack; don't emulate this.
    try:
        # figure out which function to call, and call it
        func = eval('draw_' + event.char)
    except NameError:
        print "I don't know how to draw an", event.char
        return
    except SyntaxError:
        # this happens when the user presses return
        teleport(bob, -180, bob.y-size*3)
        return

    func(bob, size)
    skip(bob, size/2)

from TurtleWorld import *
world = TurtleWorld()

# create and position the turtle
size = 20
bob = Turtle(world)
bob.delay = 0.01
teleport(bob, -180, 150)

# tell world to call keypress when the user presses a key
world.bind('<Key>', keypress)

world.mainloop()
