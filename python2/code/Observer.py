import random
from RemoteObject import *

class Observer(RemoteObject):
    """An Observer is an object that watches another object and reacts
    whenever the Subject changes state."""

    def __init__(self, subject_name):

        # connect to the name server
        id = random.randint(0, 1000000)
        observer_name = subject_name + '_observer%d' % id
        RemoteObject.__init__(self, observer_name)
        
        # register with the subject
        self.subject = subject_name
        ns = NameServer()
        proxy = ns.get_proxy(subject_name)
        proxy.register(observer_name)
        print "I just registered."

    # the following methods are intended to be invoked remotely

    def notify(self):
        """when the Subject is modified, it invokes notify;
        then the Observer uses get_state to see the update.
        As a simpler alternative, the Subject could pass the
        new state as a parameter."""
        print 'Notified'
        ns = NameServer()
        proxy = ns.get_proxy(self.subject)
        print 'Got proxy'
        state = proxy.get_state()
        print 'Observer notified; new state =', state

obs = Observer('bob')
obs.requestLoop()

