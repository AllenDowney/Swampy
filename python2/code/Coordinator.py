#!/usr/bin/python

import Pyro.core
import Pyro.util
import Pyro.naming
from RemoteObject import *

class Coordinator(RemoteObject):
    def __init__(self, channel='1'):
        self.channel = channel
        self.name = 'sd_chat_channel_' + channel
        RemoteObject.__init__(self, self.name)
        self.rlist = []
    
    def register(self, uri):
        print 'Registering', uri
        receiver = Pyro.core.getProxyForURI(uri)
        self.rlist.append(receiver)

    def broadcast(self, message):
        print 'Broadcasting', message
        for receiver in self.rlist:
            print 'Sending to', receiver 
            try:
                receiver.post_message(message)
            except:
                print 'Failed: removing', receiver 
                # self.rlist.remove(receiver)         OOOPS!!!
                receiver.name = None
        self.rlist = [r for r in self.rlist if r.name != None]

def main(name, channel='1', *args):
    c = Coordinator(channel)
    c.requestLoop()
    
if __name__ == '__main__':
    main(*sys.argv)
