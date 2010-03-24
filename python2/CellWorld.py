from math import *
from World import *

class CellWorld(World):
    """a CellWorld contains cells that represent regions and animals
    that move around between regions.
    """
    def __init__(self, size=500, csize=5):
        World.__init__(self)
        self.title('CellWorld')
        self.delay = 0.0           # time in seconds to sleep after an update
        self.size = size             # canvas size
        self.csize = csize             # cell size

        # cells is the mapping from index tuples to Cell objects
        self.cells = {}
        self.setup()
        
    def setup(self):
        """create the GUI
        """
        self.canvas = self.ca(width=self.size, height=self.size,
                              bg='white', scale = [self.csize, self.csize])

        self.la(text='Click or drag on the canvas to create cells.')
        self.setup_scale()
        
    def bind(self):
        """create bindings for the canvas
        """
        self.canvas.bind('<ButtonPress-1>', self.click)
        self.canvas.bind('<B1-Motion>', self.click)

    def click(self, event):
        """this event handler is executed when the user clicks or drags
        on the canvas.  It creates a new cell or toggles an existing cell.
        """
        # convert the button click coordinates to an index tuple
        x, y = self.canvas.invert([event.x, event.y])
        i, j = int(floor(x)), int(floor(y))

        # toggle the cell if it exists; create it otherwise
        cell = self.get_cell(i,j)
        if cell:
            cell.toggle()
        else:
            self.make_cell(x, y)

    def cell_bounds(self, i, j):
        """return the bounds of the cell with indices i, j"""
        p1 = [i, j]
        p2 = [i+1, j]
        p3 = [i+1, j+1]
        p4 = [i, j+1]
        bounds = [p1, p2, p3, p4]
        return bounds

    def get_cell(self, i, j, default=None):
        """get the cell at i, j or return (default)"""
        cell = self.cells.get((i,j), default)
        return cell

    four_neighbors = [(1,0), (-1,0), (0,1), (0,-1)]
    eight_neighbors = four_neighbors + [(1,1), (1,-1), (-1,1), (-1,-1)]

    def get_four_neighbors(self, cell, default=None):
        """return the four Von Neumann neighbors of (cell)
        """
        return self.get_neighbors(cell, default, CellWorld.four_neighbors)
        
    def get_eight_neighbors(self, cell, default=None):
        """return the four Von Neumann neighbors of (cell)
        """
        return self.get_neighbors(cell, default, CellWorld.eight_neighbors)
        
    def get_neighbors(self, cell, default=None, deltas=[(0,0)]):
        """return the neighbors of (cell) as determined (deltas), which
        is a list of tuple offsets.
        """
        i, j = cell.indices
        cells = [self.get_cell(i+di, j+dj, default) for di, dj in deltas]
        return cells
        
    def make_cell(self, i, j):
        """create and return a new cell at i,j.
        """
        bounds = self.cell_bounds(i, j)
        cell = Cell(self, bounds)
        self.cells[i,j] = cell
        return cell

    def setup_scale(self, side=TOP):
        """add GUI elements that allow the user to change the scale
        (cell size)
        """
        self.row([0,1,0], side=side)
        self.la(text='Cell size: ')
        self.csize_en = self.en(width=10, text=str(self.csize))
        self.bu(text='resize', command=self.rescale)
        self.endrow()

    def rescale(self):
        """this event handler reads the new scale from the GUI,
        changes the canvas transform, and redraws the world.
        """
        csize = self.csize_en.get()
        csize = int(csize)
        self.canvas.transforms[0].scale = [csize, csize]
        self.redraw()

    def redraw(self):
        """clear the canvas and redraw all cells and animals.
        """
        self.canvas.clear()
        for cell in self.cells.itervalues():
            cell.draw()
        for animal in self.animals:
            animal.draw()


class Cell(object):
    """represents a rectangular region in CellWorld"""
    def __init__(self, world, bounds):
        self.world = world

        # options used for a marked cell
        self.marked_options = dict(fill='black', outline='gray80')

        # options used for an unmarked cell
        self.unmarked_options = dict(fill='yellow', outline='gray80')

        self.marked = False
        self.bounds = bounds
        self.draw()

    def draw(self):
        """draw the cell"""
        if self.marked:
            options = self.marked_options
        else:
            options = self.unmarked_options

        # bounds returns all four corners, so slicing every other
        # element yields two opposing corners, which is what we
        # pass to Canvas.rectangle
        coords = self.bounds[::2]
        self.tag = self.world.canvas.rectangle(coords, **options)

    def undraw(self):
        """delete any items with this cell's tag"""
        self.world.canvas.delete(self.tag)
        
    def config(self, **options):
        """configure this cell with the given options"""
        self.world.canvas.itemconfig(self.tag, **options)

    def cget(self, x, y, option):
        """get the configuration of this cell"""
        return self.world.canvas.itemconfig(self.tag, option)

    def mark(self):
        """mark this cell and configure it"""
        self.marked = True
        self.config(**self.marked_options)
        
    def unmark(self):
        """unmark this cell and configure it"""
        self.marked = False
        self.config(**self.unmarked_options)
        
    def is_marked(self):
        """check whether this cell is marked."""
        return self.marked

    def toggle(self):
        if self.is_marked():
            self.unmark()
        else:
            self.mark()

# the following are some random linear-algebra utilities
# written as functions (not methods)

def vadd(p1, p2):
    "add vectors p1 and p2 (returns a new vector)"
    return [x+y for x,y in zip(p1, p2)]

def vscale(p, s):
    "multiply p by a scalar (returns a new vector)"
    return [x*s for x in p]

def vmid(p1, p2):
    "return a new vector that is the pointwise average of p1 and p2"
    return vscale(vadd(p1, p2), 0.5)

def rotate(v, n=1):
    """rotate the elements of a sequence by (n) places.
    returns a new list.
    """
    n %= len(v)
    return v[n:] + v[:n]



if __name__ == '__main__':
    world = CellWorld()
    world.bind()
    world.mainloop()
