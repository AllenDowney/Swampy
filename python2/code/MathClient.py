from RemoteObject import *

def main(script, name='bob', *args):
    ns = NameServer()
    server = ns.get_proxy(name)

    print server.mul(111,9)
    print server.add(100,222)
    print server.sub(222,100)
    print server.div(2.0,9.0)
    print server.mul('*',10)
    print server.add('String1','String2')

if __name__ == '__main__':
    main(*sys.argv)
