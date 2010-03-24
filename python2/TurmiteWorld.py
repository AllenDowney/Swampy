
from CellWorld import *

class TurmiteWorld(CellWorld):
    """TurmiteWorld provides a grid of cells that Turmites occupy
    """
    def __init__(self, csize=5):
        CellWorld.__init__(self, csize)
        self.title('TurmiteWorld')
        
        # the interpreter executes user-provided code
        self.inter = Interpreter(self, globals())

    def setup(self):
        self.ca_width = 600
        self.ca_height = 600

        self.row()
        self.canvas = self.ca(width=self.ca_width, height=self.ca_height,
                              bg='white', scale = [self.csize, self.csize])
        # right frame
        self.col([0,0,1,0])

        self.row([1,1,1])
        self.bu(text='Make Turmite', command=self.make_turmite)
        self.bu(text='Print canvas', command=self.canvas.dump)
        self.bu(text='Quit', command=self.quit)
        self.endrow()

        # make the run and stop buttons
        self.row([1,1,1,1], pady=30)
        self.bu(text='Run', command=self.run)
        self.bu(text='Stop', command=self.stop)
        self.bu(text='Step', command=self.step)
        self.bu(text='Clear', command=self.clear)
        self.endrow()

        # create the text entry for adding code
        self.te_code = self.te(height=20, width=40)
        self.te_code.insert(END, 't1 = Turmite(world)\n')
        self.te_code.insert(END, 't2 = Turmite(world)\n')
        self.te_code.insert(END, 't3 = Turmite(world)\n')
        self.te_code.insert(END, 't2.lt()\n')
        self.te_code.insert(END, 't3.rt()\n')
        self.te_code.insert(END, 'world.run()\n')

        self.bu(text='Run code', command=self.run_text)
        self.endcol()

    def make_turmite(self):
        """callback for the Make Turmite button"""
        turmite = Turmite(self)

    def clear(self):
        """callback for the Clean button: remove all the animals and
        all the cells"""
        for animal in self.animals:
            animal.undraw()
        for cell in self.cells.values():
            cell.undraw()
        self.animals = []
        self.cells = {}



class Turmite(Animal):
    """represents a Turmite in TurmiteWorld"""
    
    def __init__(self, world):
        Animal.__init__(self, world)
        self.dir = 0
        self.draw()
        world.register(self)
        

    def draw(self):
        """draw the Turmite"""
        # get the bounds of the cell
        cell = self.get_cell()
        bounds = world.cell_bounds(self.x, self.y)

        # draw a triangle inside the cell, pointing in the
        # appropriate direction
        bounds = rotate(bounds, self.dir)
        mid = vmid(bounds[1], bounds[2])
        self.tag = self.world.canvas.polygon([bounds[0], mid,
                                                     bounds[3]], fill='red')

    def fd(self, dist=1):
        """move forward"""
        if self.dir==0:
            self.x += dist
        elif self.dir==1:
            self.y += dist
        elif self.dir==2:
            self.x -= dist
        else:
            self.y -=dist
        self.redraw()

    def bk(self, dist=1):
        """move back"""
        self.fd(-dist)

    def rt(self):
        """turn right"""
        self.dir = (self.dir-1) % 4
        self.redraw()

    def lt(self):
        """turn left"""
        self.dir = (self.dir+1) % 4
        self.redraw()

    def get_cell(self):
        """get the cell this turmite is on (creating one if necessary)"""
        x, y, world = self.x, self.y, self.world
        return world.get_cell(x,y) or world.make_cell(x,y) 

    def step(self):
        """this step function implements the rules for Langton's
        Ant (see http://mathworld.wolfram.com/LangtonsAnt.html)
        """
        cell = self.get_cell()
        if cell.is_marked():
            self.lt()
        else:
            self.rt()
        cell.toggle()
        self.fd()



if __name__ == '__main__':
    world = TurmiteWorld()
    world.mainloop()
