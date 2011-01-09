"""This module is part of Swampy, a suite of programs available from
allendowney.com/swampy.

Copyright 2010 Allen B. Downey
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import unittest

import Tkinter
import Gui

class Tests(unittest.TestCase):

    def test_gui(self):
        gui = Gui.Gui()
        fr = gui.fr()
        endfr = gui.endfr()
        self.assertEquals(gui, endfr)

        row = gui.row()
        gui.rowweights([1,2,3])

        col = gui.col()
        gui.colweights([1,2,3])

        popfr = gui.popfr()

        self.assertEquals(popfr, row)
        
        en = gui.en()

        ca = gui.ca()
        self.assertTrue(isinstance(ca, Gui.GuiCanvas))

        la = gui.la()

        widget = gui.la()
        widget = gui.lb()
        widget = gui.bu()

        mb = gui.mb()
        widget = gui.mi(mb)

        widget = gui.te()
        widget = gui.sb()
        widget = gui.cb()

        size = Tkinter.IntVar()
        widget = gui.rb(variable=size, value=1)

        widget = gui.st()
        self.assertTrue(isinstance(widget, Gui.Gui.ScrollableText))

        widget = gui.sc()
        self.assertTrue(isinstance(widget, Gui.Gui.ScrollableCanvas))

        gui.destroy()

    def testOptions(self):
        d = dict(a=1, b=2, c=3)
        res = Gui.pop_options(d, ['b'])
        self.assertEquals(len(res), 1)
        self.assertEquals(len(d), 2)

        res = Gui.get_options(d, ['a', 'c'])
        self.assertEquals(len(res), 2)
        self.assertEquals(len(d), 2)
        
        res = Gui.remove_options(d, ['c'])
        self.assertEquals(len(d), 1)

        d = dict(side=1, column=2, other=3)
        options, packopts, gridopts = Gui.split_options(d)
        self.assertEquals(len(options), 1)
        self.assertEquals(len(packopts), 1)
        self.assertEquals(len(gridopts), 1)
        
    def testBbox(self):
        bbox = Gui.BBox([[100, 200], [300, 500]])
        self.assertEquals(bbox.left, 100)
        self.assertEquals(bbox.right, 300)
        self.assertEquals(bbox.top, 200)
        self.assertEquals(bbox.bottom, 500)

        self.assertEquals(bbox.width(), 200)
        self.assertEquals(bbox.height(), 300)

        # TODO: upperleft, lowerright, midright, midleft, center, union

        t = bbox.flatten()
        self.assertEquals(t[0], 100)

        pairs = [pair for pair in Gui.pairiter(t)]
        self.assertEquals(len(pairs), 2)

        seq = Gui.flatten(pairs)
        self.assertEquals(len(seq), 4)

if __name__ == '__main__':
    unittest.main()
