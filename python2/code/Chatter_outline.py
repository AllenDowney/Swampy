
from World import *
from RemoteObject import *

class Chatter(Gui):
    def __init__(self, channel='1'):
        Gui.__init__(self)

    def setup(self):
        self.col()
        self.display = self.te()

        self.row()
        self.entry = self.en()
        self.bu(text='Send', command=self.send)
        self.bu(text='Quit', command=self.quit)
        self.endrow()

        self.endcol()

    def quit(self):
        Gui.quit(self)

    def send(self):
        message = self.entry.get()
        print message

    def insert(self, message):
        self.display.insert(END, message)


def main(name, channel='1', *args):
    chat = Chatter(channel)
    chat.setup()
    chat.mainloop()

if __name__ == '__main__':
    main(*sys.argv)


