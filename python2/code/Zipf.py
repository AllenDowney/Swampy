
"""

Code example from _Computational_Modeling_
http://greenteapress.com/compmod

Copyright 2008 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

"""

import sys
import string
import pylab

from Hist import *

class Zipf(Hist):
    """Zipf is a histogram that maps from words to frequencies.

    It provides methods to generate data for a Zipf plot (frequency
    versus rank).
    """
    def rank_freq(self):
        """return a list of tuples where each tuple is a rank
        and the number of times the item with that rank appeared.
        """
        # sort the list of frequencies in decreasing order
        t = [f[0] for f in self.itervalues()]
        t.sort(reverse=True)

        # enumerate the ranks and frequencies 
        rf = [(r+1, f) for r, f in enumerate(t)]
        return rf


    def print_ranks(self):
        """print the rank vs. frequency data"""
        for r, f in self.rank_freq():
            print r, f

    def plot_ranks(self):
        """use pylab to plot a chart in which the x-axis
        shows ranks in increasing order and the y-axis shows the
        frequency of the value with the given rank.
        """
        t = self.rank_freq()
        rs, fs = zip(*t)
        pylab.loglog(rs, fs, 'r-')
        pylab.xlabel('log ranks')
        pylab.ylabel('log frequencies')
        pylab.show()


def iter_words(filename):
    """this is a generator that returns an iterator that yields
    the words from a file one at a time, with the punctuation stripped."""

    fp = open(filename, 'r')
    for line in fp:
        line = line.replace('--', ' ')
        line = line.replace("'s ", ' ')
        for word in line.rstrip().split():
            word = word.strip(string.punctuation)
            yield word


def main(name, filename='gatsby.txt', flag='print', *args):

    # build a Zipf histogram of the words in filename
    iter = iter_words(filename)
    z = Zipf(iter)

    # either print the results or plot them
    if flag == 'print':
        z.print_ranks()
    elif flag == 'plot':
        z.plot_ranks()
    else:
        print 'Usage: Zipf.py [print|plot]'


if __name__ == '__main__':
    main(*sys.argv)
