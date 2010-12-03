import os
from World import *

class Hello(Gui):
    def __init__(self, debug=False):
        Gui.__init__(self, debug)
        self.ca_width = 400
        self.ca_height = 400

    def setup(self):
        """setup creates the GUI elements (called widgets)"""
        
        self.col()
        self.canvas = self.ca(width=self.ca_width, height=self.ca_height,
                              bg='white')

        self.row([1,1])
        self.bu(text='Hello', command=self.hello)
        self.bu(text='Quit', command=self.quit)
        self.endrow()

        self.endcol()

    def hello(self):
        self.canvas.text([0, 0], 'Hello')

if __name__ == '__main__':

    # configure Lumpy
    import Lumpy
    lumpy = Lumpy.Lumpy()
    lumpy.transparent_class(Gui)
    lumpy.transparent_class(Tk)
    lumpy.transparent_class(Wm)
    lumpy.transparent_class(Misc)
    lumpy.make_reference()
    
    # create the GUI
    h = Hello()
    h.setup()

    if True:
        lumpy.object_diagram()
        lumpy.class_diagram()

    # wait for user events
    h.mainloop()
