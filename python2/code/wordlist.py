"""

Solution to the word list exercise
Think Python
Allen B. Downey

"""

def make_word_list1():
    t = []
    fin = open('words.txt')
    for line in fin:
        word = line.strip()
        t.append(word)
    return t

def make_word_list2():
    t = []
    fin = open('words.txt')
    for line in fin:
        word = line.strip()
        t = t + [word]
    return t

t = make_word_list1()
print len(t)
print t[:10]

t = make_word_list2()
print len(t)
print t[:10]

