"""

Solution to the reducible word Car Talk Puzzler
Think Python
Allen B. Downey

"""

def make_word_list():
    """read the words in words.txt and return a dictionary
    that contains the words as keys"""
    d = dict()
    fin = open('words.txt')
    for line in fin:
        word = line.strip().lower()
        d[word] = word

    # have to add single letter words to the word list;
    # also, the empty string is considered a word.
    for letter in ['a', 'i', '']:
        d[letter] = letter
    return d

wordlist = make_word_list()

"""a string is reducible if it has at least one child that is 
reducible.  The empty string is also reducible."""

"""memo is a dictionary that maps from each word that is known
to be reducible to a list of its reducible children.  It starts
with the empty string."""

memo = dict()
memo[''] = ['']

def children(word):
    """build and return a list of all words that can be formed
    by removing one letter from (word)"""
    res = []
    for i in range(len(word)):
        child = word[:i] + word[i+1:]
        if child in wordlist:
            res.append(child)
    return res

def reduce(word):
    """if this word is reducible, return a list of its reducible
    children; also add an entry to the memo dictionary."""

     # if have already checked this word, return the answer
    if word in memo:
        return memo[word]

    # check each of the children and make a list of the reducible ones
    res = []
    for child in children(word):
        t = reduce(child)
        if t:
            res.append(child)

    # memoize and return the result
    memo[word] = res
    return res

def reduce_all_words():
    """check all the words in the wordlist.  Return a list
    of the ones that are reducible.
    """
    res = []
    for word in wordlist:
        t = reduce(word)
        if t != []:
            res.append(word)
    return res

def print_trail(word):
    """print the sequence of words that reduces this word to the
    empty string; if there is more than one choice, it chooses the
    first."""
    if len(word) == 0:
        return
    print word,
    t = reduce(word)
    print_trail(t[0])

def print_longest_words():
    words = reduce_all_words()

    # use DSU to sort by word length
    t = []
    for word in words:
        t.append((len(word), word))
    t.sort(reverse=True)

    # print the longest 5 words
    for length, word in t[0:5]:
        print_trail(word)
        print '\n'

print_longest_words()
