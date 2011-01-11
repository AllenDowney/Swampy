"""This module is part of Swampy, a suite of programs available from
allendowney.com/swampy.

Copyright 2011 Allen B. Downey
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import unittest

import Sync

class Tests(unittest.TestCase):

    def test_sync(self):
        sync = Sync.Sync('mutex.py')


if __name__ == '__main__':
    unittest.main()
