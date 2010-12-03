"""

Solution to the homophone Car Talk Puzzler
Think Python
Allen B. Downey

"""

from pronounce import read_dictionary
phonetic = read_dictionary()

def make_word_list():
    """read the words in words.txt and return a dictionary
    that contains the words as keys"""
    d = dict()
    fin = open('words.txt')
    for line in fin:
        word = line.strip().lower()
        d[word] = word

    return d

wordlist = make_word_list()

def homophones(a, b):
    """return True if words (a) and (b) can be pronounced the
    same way, False otherwise.

    If either word is not in the pronouncing dictionary, return False
    """
    if a not in phonetic or b not in phonetic:
        return False

    return phonetic[a] == phonetic[b]

def check_word(word):
    """check to see if the word has the following property:
    removing the first letter yields a word in (d),
    and removing the second letter yields a word in (d)."""
    word1 = word[1:] 
    if word1 not in wordlist: return False
    if not homophones(word, word1): return False

    word2 = word[0] + word[2:]
    if word2 not in wordlist: return False
    if not homophones(word, word2): return False

    return True

def check_all_words():
    for word in wordlist:
        if check_word(word):
            print word

check_all_words()

