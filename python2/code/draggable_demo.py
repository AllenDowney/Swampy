"""

Example code from
Think Python: An Introduction to Software Design
Allen B. Downey

This program requires Gui.py, which is part of
Swampy; you can download it from thinkpython.com/swampy.

"""

from Gui import *

class Draggable(Item):
    """a Canvas Item with bindings for dragging and dropping.

    Given an item, Draggable(item) creates bindings and returns
    a Draggable object with the same canvas and tag as the original.
    """
    def __init__(self, item):
        self.canvas = item.canvas
        self.tag = item.tag
        self.bind('<ButtonPress-3>', self.select)
        self.bind('<B3-Motion>', self.drag)
        self.bind('<ButtonRelease-3>', self.drop)

    # the following event handlers take an event object as a parameter

    def select(self, event):
        """select this item for dragging"""
        self.dragx = event.x
        self.dragy = event.y

        self.fill = self.cget('fill')
        self.config(fill='yellow')
        
    def drag(self, event):
        """move this item using the pixel
        coordinates in the event object."""
        # see how far we have moved
        dx = event.x - self.dragx
        dy = event.y - self.dragy

        # save the current drag coordinates
        self.dragx = event.x
        self.dragy = event.y

        # move the item 
        self.move(dx, dy)

    def drop(self, event):
        """drop this item"""
        self.config(fill=self.fill)


# create the Gui and the Canvas
g = Gui()
ca = g.ca(width=500, height=500, bg='white')

# clicking on the canvas makes a new draggable circle
def make_circle(event):
    pos = ca.canvas_coords([event.x, event.y])
    item = ca.circle(pos, 5, fill='red')
    item = Draggable(item)

ca.bind('<ButtonPress-1>', make_circle)

# pressing Return in the Entry makes a text item
def make_text(event=None):
    text = en.get()
    item = ca.text([0,0], text)
    item = Draggable(item)

g.row([0,1])
bu = g.bu('Make text item:', make_text)
en = g.en()
en.bind('<Return>', make_text)

g.mainloop()
