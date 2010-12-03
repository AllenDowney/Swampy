"""

This module provides read_colors, which takes an optional
filename as an argument and returns 

colors: a dictionary that maps color names to rgb tuples

rgbs: a sorted list of pairs, where each pair is an rgb tuple
    and a sorted list of color names.

    An rgb tuple is a triplet of values in the range 0-255.

If the filename is provided, read_colors uses it; otherwise
it searches for the X11 color list in a file named rgb.txt.
It checks the usual places first and then uses find if necessary.

Allen B. Downey
2008

"""

import os
import re

def read_colors(filename=None):
    """find the list of X11 colors, parse the file and return
    colors: a dictionary that maps color names to rgb tuples, and
    rgbs: a sorted list of pairs, where each pair is an rgb tuple
    and a sorted list of color names.

    An rgb tuple is a triplet of values in the range 0-255.
    """
    colors = read_file(filename)
    rgbs = invert_dict(colors).items()
    rgbs.sort()
    for rgb, names in rgbs:
        names.sort()
    return colors, rgbs

def invert_dict(d):
    """return an inverse dictionary that maps from values to
    lists of keys
    """
    inv = dict()
    for key in d:
        val = d[key]
        if val not in inv:
            inv[val] = [key]
        else:
            inv[val].append(key)
    return inv

def print_rgbs(rgbs):
    """rgbs is a sorted list of pairs, where each pair is an
    RGB tuple and a list of color names.
    """
    for rgb, names in rgbs:
        print rgb, '\t',
        for s in names:
            print repr(s),
        print ''


def read_file(filename=None):
    """read the color file rgb.txt and return a dictionary
    that maps from color names to RGB tuples.
    """

    # if the user doesn't provide a filename, try to find rgb.txt
    if filename == None:
        filename = find_file()

    # regular expressions to match numbers and color names
    number = '(\d+)'
    space = '[ \\t]*'
    name = '([ \w]+)'
    pattern = space + (number + space) * 3 + name
    prog = re.compile(pattern)

    # read the file
    d = dict()
    for line in open(filename):
        ro = prog.match(line)
        if ro:
            r, g, b, name = ro.groups()
            d[name] = int(r), int(g), int(b)

    return d

def find_file():
    """try to find rgb.txt, either by looking in the usual places
    or by using find (which is slow)
    """
    
    filename = find_file1()

    if filename == None:
        print "Couldn't find your rgb.txt file (rgb.txt)."
        print "Using find; this might take a while..."
        filename = find_file2()

    return filename

def find_file1():
    """look for rgb.txt is the usual places"""
    files = [
    '/usr/share/X11/rgb.txt',
    '/etc/X11/rgb.txt',
    '/usr/local/lib/X11/rgb.txt',
    '/usr/lib/X11/rgb.txt',
    '/X11/R5/lib/X11/rgb.txt',
    '/X11/R4/lib/rgb/rgb.txt',
    '/usr/openwin/lib/X11/rgb.txt'
    ]

    for file in files:
        if os.path.exists(file):
            return file

def find_file2():
    """use find to list all files with the name rgb.txt, and return
    the first one that has 'X11' somewhere in the path.
    """
    cmd = 'find / -name rgb.txt'
    stdin, stdout, stderr = os.popen3(cmd)
    for line in stdout:
        filename = line.strip()
        if filename.find('X11') != -1:
            break

    stdin.close()
    stdout.close()
    stderr.close()
    return filename


if __name__ == '__main__':
    colors, rgbs = read_colors()
    print_rgbs(rgbs)
