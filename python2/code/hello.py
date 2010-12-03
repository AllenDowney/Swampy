# Homework 1 Solutions
# Software Design
# Allen Downey

# LEVEL 0 PRIMITIVES are provided by World.py.
# They include fd, bk, lt, rt, pu and pd

# LEVEL 1 PRIMITIVES are simple combinations of Level 0 primitives.
# They have no pre- or post-conditions.

def fdrt(t, n, angle=90):
    """forward and right"""
    fd(t, n)
    rt(t, angle)

def fdlt(t, n, angle=90):
    """forward and left"""
    fd(t, n)
    lt(t, angle)

def fdbk(t, n):
    """forward and back, ending at the original position"""
    fd(t, n)
    bk(t, n)

def ltbk(t, n, angle=90):
    """left turn and back up"""
    lt(t, angle)
    bk(t, n)

def skip(t, n):
    """lift the pen and move"""
    pu(t)
    fd(t, n)
    pd(t)


# LEVEL 2 PRIMITIVES use primitives from Levels 0 and 1
# to draw posts (vertical elements) and beams (horizontal elements)
# Level 2 primitives ALWAYS return the turtle to the original
# location and direction.

def post(t, n):
    """make a vertical line and return to the original position"""
    lt(t)
    fdbk(t, n)
    rt(t)

def beam(t, n, height):
    """make a horizontal line at the given height and return.
    This one is ugly, but I never actually use it."""
    lt(t)
    skip(t, n*height)
    rt(t)
    fdbk(t, n)
    lt(t)
    skip(t, -n * height)
    rt(t)

def hangman(t, n, height):
    """make a vertical line to the given height and a horizontal line
    at the given height and then return.
    This is efficient to implement, and turns out to be useful, but
    it's not so semantically clean."""
    lt(t)
    fdrt(t, n * height)
    fdbk(t, n)
    ltbk(t, n * height)
    rt(t)

def diagonal(t, x, y):
    """make a diagonal line to the given x, y offsets and return"""
    from math import atan2, sqrt, pi
    angle = atan2(y, x) * 180 / pi
    lt(t, angle)
    dist = sqrt(x**2 + y**2)
    fdbk(t, dist)
    rt(t, angle)

# The letter-drawing functions all have the precondition
# that the turtle is in the lower-left corner of the letter,
# and postcondition that the turtle is in the lower-right
# corner, facing in the direction it started in.

def draw_a(t, n):
    hangman(t, n, 2)
    hangman(t, n, 1)
    skip(t, n)
    post(t, 2*n)

def draw_c(t, n):
    hangman(t, n, 2)
    fd(t, n)

def draw_e(t, n):
    hangman(t, n, 2)
    hangman(t, n, 1)
    fd(t, n)

def draw_f(t, n):
    hangman(t, n, 2)
    hangman(t, n, 1)
    skip(t, n)

def draw_h(t, n):
    post(t, 2*n)
    hangman(t, n, 1)
    skip(t, n)
    post(t, 2*n)

def draw_l(t, n):
    post(t, 2*n)
    fd(t, n)

def draw_o(t, n):
    hangman(t, n, 2)
    fd(t, n)
    post(t, 2*n)

def draw_(t, n):
    # draw a space (!?)
    skip(t, n)

def draw_n(t, n):
    post(t, 2*n)
    skip(t, n)
    diagonal(t, -n, 2*n)
    post(t, 2*n)

def draw_m(t, n):
    post(t, 2*n)
    skip(t, n)
    diagonal(t, -n, 2*n)
    diagonal(t, n, 2*n)
    skip(t, n)
    post(t, 2*n)


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
        func(bob, size)
        skip(bob, size/2)
    except NameError:
        print "I don't know how to draw an", event.char
    except SyntaxError:
        # this happens when the user presses return
        teleport(bob, -180, bob.y-size*3)

# create and position the turtle
size = 20
bob = Turtle(world)
bob.delay = 0.01
teleport(bob, -180, 150)

# tell world to call keypress when the user presses a key
world.bind('<Key>', keypress)

