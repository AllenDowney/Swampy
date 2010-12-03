import os

def etime():
    """see how much user and system time this process has used
    so far and return the sum"""
    user, sys, chuser, chsys, real = os.times()
    return user+sys

def goodsum(t, init):
    """(t) is a list of lists; (init) is the starting list:
    append all of the lists in (t) onto (init) and return the
    result. 
    """
    total = init
    for x in t:
        total.extend(x)
    return total

def test_func(f, n):
    """test the function (f) with a list of lists of length (n)
    and return the elapsed time."""
    t = [[1]] * n

    start = etime()
    f(t, [])
    end = etime()
    elapsed = end - start
    return elapsed

def main(script, name='sum'):

    # depending on which function we are testing, we need to
    # us a different order of magnitude for (n)
    if name == 'sum':
        factor = 1000
    elif name == 'goodsum':
        factor = 100000

    # look up the string (name) and get the function object
    f = eval(name)

    # test (f) over a range of values for (n)
    for i in range(5, 25):
        n = factor * i
        print n, test_func(f, n)


if __name__ == '__main__':
    import sys
    main(*sys.argv)
