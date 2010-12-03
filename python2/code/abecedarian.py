"""

Solution to the abecedarian exercise.
Think Python: An Introduction to Software Design
Allen B. Downey

"""

def is_abecedarian(word):
    if len(word) <= 1:
        return True
    if word[0] > word[1]:
        return False
    return is_abecedarian(word[1:])

def is_abecedarian(word):
    previous = word[0]
    for c in word:
        if c < previous:
            return False
        previous = c
    return True

print is_abecedarian('accegj')
print is_abecedarian('bob')

