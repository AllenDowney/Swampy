"""

Example program from
Think Python: An Introduction to Software Design
Allen B. Downey

This program requires Gui.py, which is part of
Swampy; you can download it from thinkpython.com/swampy.

"""

from Gui import *

g = Gui()
photo = PhotoImage(file='danger.gif')
g.bu(image=photo)

canvas = g.ca(width=300)
canvas.image([0,0], image=photo)

import Image as PIL
import ImageTk

image = PIL.open('allen.png')
photo2 = ImageTk.PhotoImage(image)
g.la(image=photo2)

g.mainloop()
