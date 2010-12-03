"""

pronounce module
Allen B. Downey


"""

def read_dictionary(filename='c06d'):
    """read (filename) and build a dictionary that maps from
    each word to a string that describes its primary pronunciation.

    Secondary pronunciations are added to the dictionary with
    a number, in parentheses, at the end of the key, so the
    key for the second pronunciation of "abdominal" is "abdominal(2)".
    """
    d = dict()
    fin = open(filename)
    for line in fin:

        # skip over the comments
        if line[0] == '#': continue

        t = line.split()
        word = t[0].lower()
        pron = ' '.join(t[1:])
        d[word] = pron

    return d

if __name__ == '__main__':
    d = read_dictionary()
    for k, v in d.items():
        print k, v
