"""This module is part of Swampy, a suite of programs available from
allendowney.com/swampy.

Copyright 2010 Allen B. Downey
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import unittest

import TurtleWorld

class Tests(unittest.TestCase):

    def test_turtle_world(self):
        tw = TurtleWorld.TurtleWorld(interactive=True)
        tw.setup_run()
        tw.delay = 0.01
        control = tw.make_turtle()
        control.set_color('magenta')
        control.move_turtle(-1)
        tw.clear()
        tw.quit()
        
    def test_turtle(self):
        tw = TurtleWorld.TurtleWorld()
        t = TurtleWorld.Turtle()
        t.delay = 0.01
        t.step()

        t.bk(10)
        t.rt(10)
        t.lt(-10)
        t.pu()
        t.pd()
        t.set_color('papaya whip')

        TurtleWorld.fd(t, 10)
        TurtleWorld.bk(t, 10)
        TurtleWorld.lt(t, 10)
        TurtleWorld.rt(t, 10)
        TurtleWorld.pu(t)
        TurtleWorld.pd(t)
        TurtleWorld.set_color(t, 'cyan')

        tw.quit()

if __name__ == '__main__':
    unittest.main()
