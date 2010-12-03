"""

Solution to the numerical approximation of pi exercise.
Think Python: An Introduction to Software Design
Allen B. Downey

Algorithm due to Srinivasa Ramanujan, from 
http://en.wikipedia.org/wiki/Pi

"""

import math

def factorial(n):
    if n == 0:
        return 1
    else:
        recurse = factorial(n-1)
        result = n * recurse
        return result

def estimate_pi():
    total = 0
    k = 0
    factor = 2 * math.sqrt(2) / 9801
    while True:
        num = factorial(4*k) * (1103 + 26390*k)
        den = factorial(k)**4 * 396**(4*k)
        term = factor * num / den
        total += term
        
        if abs(term) < 1e-15: break
        k += 1

    return 1 / total

print estimate_pi()
