#!/usr/bin/python

"""
This module is part of Swampy, a suite of programs available from
allendowney.com/swampy.

Copyright 2005 Allen B. Downey
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

"""

from swampy.TurmiteWorld import TurmiteWorld, Turmite

# create the GUI
world = TurmiteWorld()

# create the Turmite
turmite = Turmite(world)
    
# wait for the user to do something
world.mainloop()
