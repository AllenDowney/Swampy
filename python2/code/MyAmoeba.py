# read the code in AmoebaWorld.py
from World import *

# read the math module and the time module
from math import *
import time

# create the world
world = AmoebaWorld()

# create a new amoeba, telling it what world it lives in
amoeba = Amoeba(world)

# the range of t is from start to end
start = 0
end = 10

# store the current time
real_start_time = time.time()

# count from t=start to t=end in steps of 0.1 seconds
t = start
while t < end:

    # compute x(t) and y(t)
    x = 9 * sin(t) * cos(t)
    y = 9 * sin(t)
    
    # redraw the amoeba and update the world
    print 't = %.1f   x = %.1f   y = %.1f' % (t, x, y)
    amoeba.redraw(x, y)
    world.update()

    # sleep for 0.1 seconds and then see what time it is
    time.sleep(0.1)
    t = time.time() - real_start_time

# create a quit button, then wait for the user to press it
world.bu(TOP, text='Quit', command=world.quit)
world.mainloop()


