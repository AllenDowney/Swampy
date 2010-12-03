from string import *

def clean(s):
# take a word and return a new word with the whitespace and punctuation
# stripped from the beginning and end
    s = s.lower()
    s = s.strip(whitespace+punctuation)
    return s

def clean_list(words):
# take a list of words and return a new list with all the words cleaned
    res = []
    for word in words:
        res.append(clean(word))
    return res

def print_most_common(d):
# Print the ten most common words in the dictionary.
# Make a list of tuples, where each tuple contains
# a frequency and a word.  Sort them in decreasing
# order of frequency and print the first ten.
    t = []
    for key in d:
        pair = (d[key], key)
        t.append(pair)
    t.sort()
    t.reverse()
    for i in range(10):
        print t[i]

def process_file(file):
# open read the given file, clean each line and count the number of
# words in the whole file
    fp = open(file)
    total = 0
    d = {}
    for line in fp:
        words = split(line)
        t = clean_list(words)
        for word in t:
            d[word] = d.get(word, 0) + 1
        total += len(t)
    print_most_common(d)
    return total, len(d)

print process_file('short.txt')

