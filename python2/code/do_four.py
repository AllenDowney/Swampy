"""
Solution to Exercise X.X on page X of TITLE
Allen B. Downey

"""
 
def do_twice(f, arg):
    f(arg)
    f(arg)

def print_twice(arg):
    print arg
    print arg

do_twice(print_twice, 'spam')
print

def do_four(f, arg):
    do_twice(f, arg)
    do_twice(f, arg)

do_four(print_twice, 'spam')
print

