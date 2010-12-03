import Pyro.core, Pyro.util, Pyro.naming
import sys
import threading
import socket
import os
import signal

default_ns_host = 'ece.olin.edu'

class MyThread(threading.Thread):
    """MyThread is a wrapper for threading.Thread that improves
    the syntax for creating and starting threads.
    """
    def __init__(self, target, *args):
        threading.Thread.__init__(self, target=target, args=args)
        self.start()


class Watcher:
    """The Watcher class solves two problems with multithreaded
    programs in Python, (1) a signal might be delivered
    to any thread (which is just a malfeature) and (2) if
    the thread that gets the signal is waiting, the signal
    is ignored (which is a bug).

    The watcher is a concurrent process (not thread) that
    waits for a signal and then kills the process that contains the
    active threads.  See Appendix A of The Little Book of Semaphores.

    I have only tested this on Linux.  I would expect it to
    work on OS X and not work on Windows.
    """
    
    def __init__(self, callback=None):
        """ Creates a child thread, which returns.  The parent
            thread waits for a KeyboardInterrupt and then kills
            the child thread.
        """
        self.child = os.fork()
        if self.child == 0:
            return
        else:
	    self.watch(callback)

    def watch(self, callback=None):
        """Wait for a KeyboardInterrupt and then kill the child process.
        """
        try:
            os.wait()
        except KeyboardInterrupt:
            # I put the capital B in KeyBoardInterrupt so I can
            # tell when the Watcher gets the SIGINT
            if callback:
                callback()
            print 'KeyBoardInterrupt'
            self.kill()
        sys.exit()

    def kill(self):
        """Kill the child process.
        """
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError: pass


def get_ip_addr():
    """get the real IP address of this machine"""
    csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csock.connect((default_ns_host, 80))
    (addr, port) = csock.getsockname()
    csock.close()
    return addr

class NameServer:
    """A NameServer object is a proxy for the name server running
    on a remote host"""

    def __init__(self, ns_host=default_ns_host):
        """locate the name server on the given host"""
        self.ns_host = ns_host
        self.ns = Pyro.naming.NameServerLocator().getNS(ns_host)

    def get_proxy(self, name):
        """look up a remote object by name and create a proxy for it"""
        try:
            uri = self.ns.resolve(name)
        except Pyro.errors.NamingError:
            type, value, traceback = sys.exc_info()
            print 'Pyro NamingError:', value
            sys.exit(1)

        return Pyro.core.getProxyForURI(uri)

    def query(self, name, group=None):
        """check whether the given name is registered in the given group.
        return 1 if the name is a remote object, 0 if it is a group,
        and -1 if it doesn't exist."""
        t = self.ns.list(group)
        for k, v in t:
            if k == name:
                return v
        return -1

    def create_group(self, name):
        """create a group with the given name"""
        self.ns.createGroup(name)
    
    def get_remote_object_list(self, prefix='', group=None):
        """return a list of the remote objects in the given group
        that start with the given prefix"""
        t = self.ns.list(group)
        u = [s for (s, n) in t if n==1 and s.startswith(prefix)]
        return u

    def clear(self, prefix='', group=None):
        """unregister all objects in the given group that start
        with the given prefix"""
        t = self.ns.list(group)
        print t
        for (s, n) in t:
            if not s.startswith(prefix): continue
            if n==1:
                if group:
                    s = '%s.%s' % (group, s)
                print s
	        self.ns.unregister(s)
    

class RemoteObject(Pyro.core.ObjBase):
    """RemoteObject is an extension of the Pyro ObjBase that
    provides a higher level of abstraction.

    Objects that want to be available remotely should inherit
    from this class, and either (1) don't override __init__ or
    (2) call RemoteObject.__init__ explicitly"""

    def __init__(self, name=None, ns=None):
        """Create a new RemoteObject with the given name and
        register with the given name server.  If name is omitted,
        one is generated based on the object id.  If ns is omitted,
        it uses the default name server.
        """
        Pyro.core.ObjBase.__init__(self)

        if name == None:
            name = 'remote_object' + str(id(self))
        self.name=name
        
        if ns == None:
            ns = NameServer()

        self.connect(ns, name)
        
    def connect(self, ns, name):
        """Connect to the given name server with the given name"""

        # create the daemon (the attribute is spelled "demon" to
        # avoid a name collision)
        addr = get_ip_addr()
        self.demon = Pyro.core.Daemon(host=addr)
        self.demon.useNameServer(ns.ns)

        # instantiate the object and advertise it
        try:
            print 'Connecting remote object', name
            self.uri = self.demon.connect(self, name)
        except Pyro.errors.NamingError:
            print 'Pyro NamingError: name already exists or is illegal'
            sys.exit(1)

        return self.name

    def requestLoop(self):
        """Run the request loop until an exception occurs"""
        try:
            self.demon.requestLoop()
        except:
            self.cleanup()
            if sys.exc_type != KeyboardInterrupt:
                raise sys.exc_type, sys.exc_value

    def cleanup(self):
        """Remove this object from the name server"""
        print 'Shutting down remote object', self.name
        try:
            self.demon.disconnect(self)
        except KeyError:
            print "tried to remove a name that wasn't on the name server"
        self.stopLoop()
        self.demon.shutdown()

    def threadLoop(self):
        """Run the request loop in a separate thread"""
        self.thread = threading.Thread(target=self.stoppableLoop)
        self.thread.start()
        
    def stoppableLoop(self):
        """Run handleRequests until another thread clears self.running"""
        self.running = 1
        try:
            while self.running:
                self.demon.handleRequests(0.1)
        finally:
            self.cleanup()

    def stopLoop(self):
        """If stoppableLoop is running, stop it"""
        self.running = 0

    def join(self):
        """Wait for the threadLoop to complete"""
        if hasattr(self, 'thread'):
            self.thread.join()


def main(script, name='remote_object', group='test', *args):

    # find the name server
    ns = NameServer()

    # if it doesn't have a group named test, make one
    if ns.query(group) == -1:
        print 'Making group %s...' % group
        ns.create_group(group)

    # create a remote object and connect it
    full_name = '%s.%s' % (group, name)
    server = RemoteObject(full_name, ns)

    # confirm that the group and object are on the name server
    print group, ns.query(group)
    print full_name, ns.query(name, group)    
    print group, ns.get_remote_object_list(group=group)

    # create a Watcher and then run the server loop in a thread
    watcher = Watcher(server.cleanup)
    child = MyThread(client_code, full_name, server)
    server.stoppableLoop()
    print 'Server done.'

def client_code(full_name, server):
    # get a proxy for this object
    # and invoke a method on it
    ns = NameServer()
    proxy = ns.get_proxy(full_name)
    print proxy.__hash__()

    # stop the server
    server.stopLoop()
    server.join()

    # child thread completes
    print 'Thread complete.'


if __name__ == '__main__':
    main(*sys.argv)
