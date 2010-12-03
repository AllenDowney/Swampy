

"""

Code example from _Computational_Modeling_
http://greenteapress.com/compmod

Copyright 2008 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

"""


import urllib
import csv

format = 'http://www.census.gov/popest/cities/tables/SUB-EST2007-04-%2.2d.csv'

def download(filename='populations.csv'):
    """Download files from the U.S. Census Bureau.
    Concatenate the contents of these pages and store them in (filename).
    Files are numbered from 01 to 56, with a couple of gaps for future
    expansion (just kidding -- they are for U.S. territories)."""
    out = open(filename, 'w')
    for i in range(1,57):
        url = format % i

        conn = urllib.urlopen(url)
        for line in conn.fp:
            out.write(line)

def process(filename='populations.csv'):
    """Read the previously-downloaded contents of (filename), parse
    it as CSV and extract all lines that seem to contain population
    information for a city or town.  For each line that is in the
    right format to be parsed, print the population as of 2006.
    """
    fp = open(filename)
    reader = csv.reader(fp)
    res = []

    for t in reader:
        if len(t) != 11: continue

        try:
            name = t[0]
            if 'town' not in name and 'city' not in name: continue

            # use the second-to-last data point, which seems to
            # have fewer NAs
            pop = t[-2]
            pop = pop.replace(',', '')
            pop = int(pop)
            res.append(pop)
        except:
            # if anything goes wrong, skip to the next one
            pass
            
    return res

def main(script, command=None):
    if command == 'download':
        download()
    elif command == 'process':
        pops = process()
        for pop in pops:
            print pop
    else:
        print 'Usage: populations.py [download|process]'
    

import sys
if __name__ == '__main__':
    main(*sys.argv)
