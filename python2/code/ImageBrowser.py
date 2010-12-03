"""

Solution to an exercise from
Think Python: An Introduction to Software Design
Allen B. Downey

This program requires Gui.py, which is part of
Swampy; you can download it from thinkpython.com/swampy.

This program started with a recipe by Noah Spurrier at
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/521918

"""

import os, sys
from Gui import *
import Image as PIL      # to avoid name conflict with Tkinter
import ImageTk

class ImageBrowser(Gui):
    """An image browser that scans the files in a given directory and
    displays any images that can be read by PIL.
    """
    def __init__(self):
        Gui.__init__(self)

        # clicking on the image breaks out of mainloop
        self.button = self.bu(command=self.quit, relief=FLAT)

    def image_loop(self, dirname='.'):
        """loop through the files in (dirname), displaying
        images and skipping files PIL can't read.
        """
        files = os.listdir(dirname)
        for file in files:
            try:
                self.show_image(file)
                print file
                self.mainloop()
            except IOError:
                continue
            except:
                break

    def show_image(self, filename):
        """Use PIL to read the file and ImageTk to convert
        to a PhotoImage, which Tk can display.
        """
        image = PIL.open(filename)
        self.tkpi = ImageTk.PhotoImage(image)
        self.button.config(image=self.tkpi)

def main(script, dirname='.'):
    g = ImageBrowser()
    g.image_loop(dirname)

if __name__ == '__main__':
    main(*sys.argv)
