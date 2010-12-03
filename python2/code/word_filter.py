import sys, string
from filters import *

# apply_filter: read each line of the given file and apply the
# given filter.  If the result is true, print the line that passes.
def apply_filter(file, filter, *args):
    try:
        fp = open(file, 'r')
    except IOError:
        print "Couldn't find a file named", file
        sys.exit()

    for word in fp:
        word = string.rstrip(word)
        word = string.lower(word)
        if filter(word, *args):
            print word

# main processes the command-line arguments and calls apply_filter()
def main(script, filter='has_e', *args):
    # since filter is a string, we have to use eval() to find
    # the function object it names
    try:
        filter = eval(filter)
    except NameError:
        print 'There is no filter named', filter
        sys.exit()

    # then we can apply the filter to a file
    file='/usr/share/dict/words'
    apply_filter(file, filter, *args)


# if we are running the program as a script (as opposed to
# importing it, we should call main(), passing along
# the command-line arguments
if __name__ == '__main__':
    main(*sys.argv)
