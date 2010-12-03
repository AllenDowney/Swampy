from World import *

class AmoebaWorld(World):
    """AmoebaWorld is a microscope slide, with hash marks, where
    Amoebas trace parametric equations.
    """

    def __init__(self):
        World.__init__(self)
        self.title('AmoebaWorld')
        self.ca_width = 400             # canvas width and height
        self.ca_height = 400
        self.animals = []               # a list of Amoebas
        self.thread = None

        # create the canvas
        self.row()
        self.canvas = self.ca(width=self.ca_width, height=self.ca_height,
                              bg='white', scale=[20,20])

        # draw the grid
        dash = {True:'', False:'.'}
        (xmin, xmax) = (-10, 10)
        (ymin, ymax) = (-10, 10)
        for x in range(xmin, xmax+1, 1):
            self.canvas.line([[x, ymin], [x, ymax]], dash=dash[x==0])
        for y in range(ymin, ymax+1, 1):
            self.canvas.line([[xmin, y], [xmax, y]], dash=dash[y==0])

    def control_panel(self):
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
        """make the entries for the equations x(t) and y(t)
        """
        self.la(text=label)
        entry = self.en(width=5, text=' t')
        return entry

    def clear(self):
        """undraw and remove all the animals, and anything else
        on the canvas
        """
        for animal in self.animals:
            animal.undraw()
        self.canvas.delete('slime')

    def run_thread(self):
        """execute AmoebaWorld.run in a new thread"""
        
        # if there is already a thread, kill it and wait for it to die
        if self.thread:
            self.running = 0
            self.thread.join()

        # find out how long to run
        end = self.en_end.get()
        end = int(end)

        # create a thread and start it
        self.thread = MyThread(self.run, end)

    def run(self, end=10):
        """count from 0 to end seconds in 0.1 second increments.
        At each step, compute the location of the Amoebas and update.
        """
        self.running = 1
        start_time = time.time()
        t = 0
        xexpr = self.en_xoft.get()
        yexpr = self.en_yoft.get()
        while self.exists and self.running and t < end:
            for amoeba in self.animals:
                x = eval(xexpr)
                y = eval(yexpr)
                print 't = %.1f   x = %.1f   y = %.1f' % (t, x, y)
                amoeba.redraw(x, y)
            time.sleep(0.1)
            t = time.time() - start_time
            
        
class Amoeba(Animal):
    """a soft, round animal that lives in AmoebaWorld"""
    
    def __init__(self, world, xoft=None, yoft=None):
        self.world = world

        # xoft and yoft are functions that compute the location
        # of the Amoeba as a function of time
        self.xoft = xoft or self.xoft
        self.yoft = yoft or self.yoft

        # size and color
        self.size = 0.5
        self.color1 = 'violet'
        self.color2 = 'medium orchid'
        world.register(self)

    def xoft(self, t):
        """a simple function that computes the Amoeba's x position"""
        return t

    def yoft(self, t):
        """a simple function that computes the Amoeba's y position"""
        return t

    # NOTE: the interfaces for draw and redraw are different from
    # other animals.  I pass x and y as parameters because I wanted
    # to avoid using attributes.  Students haven't seen attributes
    # yet when they work with AmoebaWorld.

    def redraw(self, x, y):
        """erase the Amoeba and redraw at location x, y"""
        self.undraw()
        self.draw(x, y)

    def draw(self, x, y):
        """draw the Amoeba"""

        # thetas is the sequence of angles used to compute the perimeter
        thetas = range(0, 360, 30)
        coords = self.poly_coords(x, y, thetas, self.size)

        self.tag = 'Amoeba%d' % id(self)
        slime = 'lavender'

        # draw the slime outline which will be left behind
        self.world.canvas.polygon(coords, fill=slime, outline=slime,
                                  tags='slime')

        # draw the outer perimeter
        self.world.canvas.polygon(coords,
            fill=self.color1, outline=self.color2, tags=self.tag)

        # draw the perimeter of the nucleus
        coords = self.poly_coords(x, y, thetas, self.size/2)
        self.world.canvas.polygon(coords,
            fill=self.color2, outline=self.color1, tags=self.tag)

    def poly_coords(self, x, y, thetas, size):
        """compute the coordinates of a polygon centered around x,y,
        with a radius of approximately size, but with random variation
        """
        rs = [size+random.uniform(0, size) for theta in thetas]
        coords = [self.polar(x, y, r, theta) for (r, theta) in zip(rs, thetas)]
        return coords


class GuiAmoeba(Amoeba):
    """there are two kinds of Amoebas: for a regular Amoeba, xoft
    and yoft are functions that compute coordinates as a function of
    time.  For a GuiAmoeba, xoft and yoft use methods from
    AmoebaWorld to read expressions for x(t) and y(t) from the GUI.
    """    
    def xoft(self, t):
        return self.world.xoft(t)

    def yoft(self, t):
        return self.world.yoft(t)


if __name__ == '__main__':
    # create the GUI
    world = AmoebaWorld()
    world.control_panel()

    # create the amoeba
    amoeba = GuiAmoeba(world)
    
    # wait for the user to do something
    world.mainloop()
