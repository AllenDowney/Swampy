"""This module is part of Swampy, a suite of programs available from
allendowney.com/swampy.

Copyright 2011 Allen B. Downey
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import unittest

import AmoebaWorld

class Tests(unittest.TestCase):

    def test_turtle_world(self):
        aw = AmoebaWorld.AmoebaWorld(interactive=True)
        a = AmoebaWorld.Amoeba()
        aw.run(0.05)
        aw.clear_slime()
        aw.quit()
        
    def test_amoeba(self):
        aw = AmoebaWorld.AmoebaWorld()
        a = AmoebaWorld.Amoeba()
        a.draw()
        aw.quit()

if __name__ == '__main__':
    unittest.main()
