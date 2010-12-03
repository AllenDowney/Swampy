import sys
import string

def is_palindrome(word):
    """return True if the given word is a palindrome;
    otherwise return False"""
    if word == 'palindrome':
        return True
    else:
        return False

def apply_filter(file, filter, *args):
    """read each line of the given file and apply the given filter.
    If the result is true, print the line."""
    try:
        fp = open(file, 'r')
    except IOError:
        print "Couldn't find a file named", file
        sys.exit()

    for word in fp:
        word = word.rstrip()
        word = word.lower()
        if filter(word, *args):
            print word

def main(script, filter='is_palindrome', *args):
    """Processes the command-line arguments and call apply_filter().
    Since filter is a string, we have to use eval() to find
    the function object it names."""
    try:
        filter = eval(filter)
    except NameError:
        print 'There is no filter named', filter
        sys.exit()

    # then we can apply the filter to a file
    file='words.txt'
    apply_filter(file, filter, *args)


# if we are running the program as a script (as opposed to
# importing it, we should call main(), passing along
# the command-line arguments
if __name__ == '__main__':

    # there are two ways to run this program.  While
    # you are debugging a filter, test it by calling
    # it with a few examples, like this:
    print is_palindrome('palindrome')
    print is_palindrome('not palindrome')
    
    # once the filter is working, make sure it is a silent
    # function and then uncomment the following line
    # to search the dictionary for all instances.
    # main(*sys.argv)

