"""

Solution to the palindrome exercise.
Think Python: An Introduction to Software Design
Allen B. Downey

"""

def first(word):
    return word[0]

def last(word):
    return word[-1]

def middle(word):
    return word[1:-1]

def is_palindrome(word):
    if len(word) <= 1:
        return True
    if first(word) != last(word):
        return False
    return is_palindrome(middle(word))

def is_abecedarian(word):
    if len(word) <= 1:
        return True
    if word[0] > word[1]:
        return False
    return is_abecedarian(word[1:])

print is_palindrome('allen')
print is_palindrome('bob')
print is_palindrome('otto')
print is_palindrome('redivider')

