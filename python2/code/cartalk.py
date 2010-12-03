"""

Solution to the Car Talk puzzler exercises.
Think Python: An Introduction to Software Design
Allen B. Downey

"""

""" Puzzler #1
    http://www.cartalk.com/content/puzzler/transcripts/200725
"""

def is_triple_double(word):
    """return True if the word contains three consecutive
    double letters."""
    i = 0
    count = 0
    while i < len(word)-1:
        if word[i] == word[i+1]:
            count = count + 1
            if count == 3:
                return True
            i = i + 2
        else:
            count = 0
            i = i + 1
    return False


def find_triple_double():
    fin = open('words.txt')
    for line in fin:
        word = line.strip()
        if is_triple_double(word):
            print word


print 'Here are all the words in the list that have'
print 'three consecutive double letters.'
find_triple_double()
print


""" Puzzle #2
    http://www.cartalk.com/content/puzzler/transcripts/200803
"""

def has_palindrome(i, start, len):
    """return True if the integer i, when written as a string,
    contains a palindrome with length (len), starting at index (start).
    """
    s = str(i)[start:start+len]
    return s[::-1] == s
    
def check(i):
    """check whether the integer (i) has the properties described
    in the puzzler
    """
    return (has_palindrome(i, 2, 4)   and
            has_palindrome(i+1, 1, 5) and
            has_palindrome(i+2, 1, 4) and
            has_palindrome(i+3, 0, 6))

def check_all():
    """enumerate the six-digit numbers and print any that satisfy the
    requirements of the puzzler"""

    i = 100000
    while i <= 999999:
        if check(i):
            print i
        i = i + 1

print 'The following are the possible odometer readings:'
check_all()
print


""" Puzzle #3
    http://www.cartalk.com/content/puzzler/transcripts/200813
"""

def str_fill(i, len):
    """return the integer (i) written as a string with at least
    (len) digits"""
    return str(i).zfill(len)


def are_reversed(i, j):
    """ return True if the integers i and j, written as strings,
    are the reverse of each other"""
    return str_fill(i,2) == str_fill(j,2)[::-1]


def num_instances(diff, flag=False):
    """returns the number of times the mother and daughter have
    pallindromic ages in their lives, given the difference in age.
    If flag==True, prints the details."""
    daughter = 0
    count = 0
    while True:
        mother = daughter + diff
        if are_reversed(daughter, mother) or are_reversed(daughter, mother+1):
            count = count + 1
            if flag:
                print daughter, mother
        if mother > 120:
            break
        daughter = daughter + 1
    return count
    

def check_diffs():
    """enumerate the possible differences in age between mother
    and daughter, and for each difference, count the number of times
    over their lives they will have ages that are the reverse of
    each other."""
    diff = 10
    while diff < 70:
        n = num_instances(diff)
        if n > 0:
            print diff, n
        diff = diff + 1

print 'diff  #instances'
check_diffs()

print
print 'daughter  mother'
num_instances(18, True)
