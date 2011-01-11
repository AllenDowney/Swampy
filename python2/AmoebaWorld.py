"""This module is part of Swampy, a suite of programs available from
allendowney.com/swampy.

Copyright 2011 Allen B. Downey
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import math
import random
import time

from World import World, Animal, MyThread


class AmoebaWorld(World):
    """A microscope slide where Amoebas trace parametric equations."""

    def __init__(self, interactive=False):
        World.__init__(self)
        self.title('AmoebaWorld')
        self.thread = None

        self.make_canvas()
        if interactive:
            self.make_control_panel()

    def make_canvas(self, low=-10, high=10):
        # create the canvas
        self.row()
        self.ca_width = 400
        self.ca_height = 400
        self.canvas = self.ca(width=self.ca_width, height=self.ca_height,
                              bg='white', scale=[20,20])

        # draw the grid
        d = {True:'', False:'.'}
        xmin, xmax = low, high
        ymin, ymax = low, high
        for x in range(xmin, xmax+1, 1):
            self.canvas.line([[x, ymin], [x, ymax]], dash=d[x==0])
        for y in range(ymin, ymax+1, 1):
            self.canvas.line([[xmin, y], [xmax, y]], dash=d[y==0])

    def make_control_panel(self):
        self.col([0,0,0,1])

        # run, stop, quit buttons
        self.gr(2, [1,1], [1,1])
        self.bu(text='Clear', command=self.clear)
        self.bu(text='Quit', command=self.quit)
        self.bu(text='Run', command=self.run_thread)
        self.bu(text='Stop', command=self.stop)
        self.endgr()

        # end time entry
        self.row([0,1,0], pady=30)
        self.la(text='end time')
        self.en_end = self.en(width=5, text='10')
        self.la(text='seconds')
        self.endfr()

        # entries for x(t) and y(t)

        self.gr(2, [0,1])
        self.en_xoft = self.make_entry('x(t) = ')
        self.la()
        self.la()
        self.en_yoft = self.make_entry('y(t) = ')
        self.endgr()

        self.la()

        self.endcol()

    def make_entry(self, label):
        """Makes an entry with the given label."""
        self.la(text=label)
        entry = self.en(width=5, text=' t')
        return entry

    def run_thread(self):
        """Execute AmoebaWorld.run in a new thread."""
        
        # if there is already a thread, kill it and wait for it to die
        if self.thread:
            self.running = 0
            self.thread.join()

        # find out how long to run
        end = self.en_end.get()
        end = float(end)

        # create a thread and start it
        self.thread = MyThread(self.run, end)

    def run(self, end=10):
        """Run in real time from 0 to end in  increments.

        At each step, compute the location of the Amoebas and update.
        """
        self.clear_slime()
        self.running = 1

        xexpr = self.en_xoft.get()
        yexpr = self.en_yoft.get()
        amoeba = self.animals[0]

        start_time = time.time()
        t = 0
        while self.exists and self.running and t < end:
            x = eval(xexpr)
            y = eval(yexpr)
            print 't = %.1f   x = %.1f   y = %.1f' % (t, x, y)
            amoeba.move(x, y)
            
            time.sleep(0.1)
            t = time.time() - start_time
            
    def clear_slime(self):
        self.canvas.delete('slime')
            
        
class Amoeba(Animal):
    """A soft, round animal that lives in AmoebaWorld"""
    
    def __init__(self, world=None):
        Animal.__init__(self, world)

        # size and color
        self.size = 0.5
        self.color1 = 'violet'
        self.color2 = 'medium orchid'

    def move(self, x, y):
        self.x = x
        self.y = y
        self.redraw()

    def draw(self):
        """Draws the Amoeba."""

        # thetas is the sequence of angles used to compute the perimeter
        thetas = range(0, 360, 30)
        coords = self.poly_coords(self.x, self.y, thetas, self.size)

        self.tag = 'Amoeba%d' % id(self)
        slime = 'lavender'

        # draw the slime outline which will be left behind
        self.world.canvas.polygon(coords, fill=slime, outline=slime,
                                  tags='slime')

        # draw the outer perimeter
        self.world.canvas.polygon(coords,
            fill=self.color1, outline=self.color2, tags=self.tag)

        # draw the perimeter of the nucleus
        coords = self.poly_coords(self.x, self.y, thetas, self.size/2)
        self.world.canvas.polygon(coords,
            fill=self.color2, outline=self.color1, tags=self.tag)

    def poly_coords(self, x, y, thetas, size):
        """Computes coordinates of a polygon with random variation.

        Args:
            x, y: center point
            thetas: sequence of angles
            size: minimum radius; actual radius is up to 2x bigger
        """
        rs = [size+random.uniform(0, size) for theta in thetas]
        coords = [self.polar(x, y, r, theta) for (r, theta) in zip(rs, thetas)]
        return coords


if __name__ == '__main__':
    # create the GUI
    world = AmoebaWorld(interactive=True)

    # create the amoeba
    amoeba = Amoeba(world)
    
    # wait for the user to do something
    world.mainloop()
