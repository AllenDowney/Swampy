
"""

Solution to the anagram set exercise
Think Python
Allen B. Downey

"""

def signature(s):
    """return the signature of this string, which is a string
    that contains all of the letters in order
    """
    t = list(s)
    t.sort()
    t = ''.join(t)
    return t

def all_anagrams(filename):
    d = {}
    for line in open(filename):
        word = line.strip().lower()
        t = signature(word)

        if t not in d:
            d[t] = [word]
        else:
            d[t].append(word)
    return d

def print_anagram_sets(d):
    for v in d.values():
        if len(v) > 1:
            print len(v), v

def print_anagram_sets_in_order(d):
    t = []
    for v in d.values():
        if len(v) > 1:
            t.append((len(v), v))
    t.sort(reverse=True)
    for x in t:
        print x

d = all_anagrams('words.txt')
print_anagram_sets_in_order(d)
