from RemoteObject import *

class Modifier:
    """A Modifier is an object that reads and writes the state of
    a Subject, but it is not a registered Observer."""


    def __init__(self, subject_name):
        self.subject = ns.get_proxy(subject_name)

    def modify(self):
        """increment the state of the Subject"""
        state = self.subject.get_state()
        self.subject.set_state(state+1)
        print 'Set state ' + str(state+1)

ns = NameServer()
subject_name = 'bob'
mod = Modifier(subject_name)
mod.modify()
