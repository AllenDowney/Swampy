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

def process_file(file):
# open read the given file, clean each line and count the number of
# words in the whole file
    fp = open(file)
    total = 0
    for line in fp:
        words = split(line)
        t = clean_list(words)
        total += len(t)
    return total

print process_file('gatsby.txt')

