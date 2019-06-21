#!/usr/bin/python

"""
This module is part of Swampy, a suite of programs available from
allendowney.com/swampy.

Copyright 2005 Allen B. Downey
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

"""

from swampy.AmoebaWorld import AmoebaWorld, Amoeba

# create the GUI
world = AmoebaWorld(interactive=True)
world.set_end_time('2 * math.pi')
world.set_x_t('10 * math.cos(t)')
world.set_y_t('10 * math.sin(t)')

# create the amoeba
amoeba = Amoeba()
    
# wait for the user to do something
world.mainloop()
