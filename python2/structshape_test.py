"""This module is part of Swampy, a suite of programs available from
allendowney.com/swampy.

Copyright 2011 Allen B. Downey
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import unittest

from structshape import structshape

class Tests(unittest.TestCase):

    def test_lumpy(self):
        t = [1,2,3]
        self.assertEqual(structshape(t), 'list of 3 int')

        t2 = [[1,2], [3,4], [5,6]]
        self.assertEqual(structshape(t2), 'list of 3 list of 2 int')

        t3 = [1, 2, 3, 4.0, '5', '6', [7], [8], 9]
        self.assertEqual(structshape(t3), 
                         'list of (3 int, float, 2 str, 2 list of int, int)')

        class Point:
            """trivial object type"""

        t4 = [Point(), Point()]
        self.assertEqual(structshape(t4), 'list of 2 Point')

        s = set('abc')
        self.assertEqual(structshape(s), 'set of 3 str')

        lt = zip(t, s)
        self.assertEqual(structshape(lt), 'list of 3 tuple of (int, str)')

        d = dict(lt)        
        self.assertEqual(structshape(d), 'dict of 3 int->str')

        it = iter('abc')
        self.assertEqual(structshape(it), 'iterator of 3 str')


if __name__ == '__main__':
    unittest.main()
