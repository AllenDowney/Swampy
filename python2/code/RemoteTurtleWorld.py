from TurtleWorld import *
from RemoteObject import *

class RemoteTurtleWorld(TurtleWorld, RemoteObject):
    def __init__(self, name):
        TurtleWorld.__init__(self)
        RemoteObject.__init__(self, name)

    def quit(self):
        self.stopLoop()
        self.join()
        World.quit(self)

    def run_message(self, message):
        self.inter.run_code(message, '<user-provided code>')

def main(script, name='bob'):
    world = RemoteTurtleWorld(name)
    world.threadLoop()
    world.mainloop()

if __name__ == '__main__':
    main(*sys.argv)

