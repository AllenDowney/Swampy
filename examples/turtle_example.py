#!/usr/bin/python

"""
This module is part of Swampy, a suite of programs available from
allendowney.com/swampy.

Copyright 2005 Allen B. Downey
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

"""

from swampy.TurtleWorld import TurtleWorld, Turtle

# create the GUI
world = TurtleWorld(interactive=True)

# create the Turtle
turtle = Turtle()
    
# wait for the user to do something
world.mainloop()
