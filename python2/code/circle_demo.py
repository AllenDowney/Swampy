"""

Solution to an exercise from
Think Python: An Introduction to Software Design
Allen B. Downey

This program requires Gui.py, which is part of
Swampy; you can download it from thinkpython.com/swampy.

"""

from Gui import *

g = Gui()
g.title('circle demo')
canvas = g.ca(width=500, height=500, bg='white')
circle = None

def callback1():
    """called when the user presses 'Create circle' """
    global circle
    circle = canvas.circle([0,0], 100)

def callback2():
    """called when the user presses 'Change color' """

    # if the circle hasn't been created yet, do nothing
    if circle == None:
        return

    # get the text from the entry and try to change the circle's color
    color = entry.get()
    try:
        circle.config(fill=color)
    except TclError, message:
        # probably an unknown color name
        print message
        

# create the widgets
g.bu(text='Create circle', command=callback1)
entry = g.en()
g.bu(text='Change color', command=callback2)

g.mainloop()
