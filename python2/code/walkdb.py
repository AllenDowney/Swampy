import os, sys, getopt
from os.path import *
import shelve

def get_ctime(file):
    # get the file's time of last modification
    try:
        return getctime(file)
    except OSError:
        return -1


def loop(dir, function):
    # loop through the subdirectories and files
    # invoking function on each file
    for root, dirs, files in os.walk(dir):
        for name in files:
            file = join(root, name)
            function(file)


class Database:
    def __init__(self, dbname):
        # open the database
        self.db = shelve.open(dbname, 'c')

    def store_ctime(self, file):
        # put the file's ctime in the database
        ct = get_ctime(file)
        self.db[file] = ct

    def check_ctime(self, file):
        # check whether the file has been modified since the database
        # was updated
        ct = get_ctime(file)
        try:
            old_ct = self.db[file]
            if ct > old_ct:
                print file
        except:
            print file
        self.db[file] = ct

    def read(self):
        # print the contents of the database
        for key in self.db:
            print self.db[key], key


def main(script, *args):
    # separate the options from the arguments
    optlist, args = getopt.getopt(args, 'rwc')

    # open the database
    dir = args[0]
    dbname = join(dir, 'lastmod.db')
    db = Database(dbname)

    # handle the options
    flags = dict(optlist)

    if '-r' in flags:
        db.read()
    elif '-w' in flags:
        loop(dir, db.store_ctime)
    elif '-c' in flags:
        loop(dir, db.check_ctime)

if __name__ == '__main__':
    main(*sys.argv)
