"""

Example code from
Think Python: An Introduction to Software Design
Allen B. Downey

This program requires Gui.py, which is part of
Swampy; you can download it from thinkpython.com/swampy.

"""

from Gui import *

g = Gui()
g.title('')
g.la('Select a color:')
colors = ['red', 'green', 'blue']
mb = g.mb(text=colors[0])

def set_color(color):
    print color
    mb.config(text=color)

for color in colors:
    g.mi(mb, text=color, command=Callable(set_color, color))

g.mainloop()
