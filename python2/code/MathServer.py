from RemoteObject import *

class MathServer(RemoteObject):
    def mul(s, arg1, arg2): return arg1*arg2
    def add(s, arg1, arg2): return arg1+arg2
    def sub(s, arg1, arg2): return arg1-arg2
    def div(s, arg1, arg2): return arg1/arg2
    
def main(script, name='bob', *args):
    print 'Starting MathServer %s...' % name
    server = MathServer(name)
    server.requestLoop()
    
if __name__ == '__main__':
    main(*sys.argv)
