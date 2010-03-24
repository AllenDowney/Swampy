
from World import *

class TurtleWorld(World):
    """an environment for Turtles and TurtleControls
    """
    def __init__(self, interactive=False):
        World.__init__(self)
        self.title('TurtleWorld')

        # the interpreter executes user-provided code
        self.inter = Interpreter(self, globals())

        # delays is time in seconds to sleep after an update
        self.delay = 0.05
        
        self.setup()
        if interactive:
            self.setup_interactive()

    def setup(self):
        """create the GUI"""

        # canvas width and height
        self.ca_width = 400
        self.ca_height = 400

        self.row()
        self.canvas = self.ca(width=self.ca_width,
                              height=self.ca_height,
                              bg='white')

    def setup_interactive(self):
        """create the right frame with the buttons for interactive mode
        """
        # right frame
        self.fr()

        self.gr(2, [1,1], [1,1], expand=0)
        self.bu(text='Print canvas', command=self.canvas.dump)
        self.bu(text='Quit', command=self.quit)
        self.bu(text='Make Turtle', command=self.make_turtle)
        self.bu(text='Clear', command=self.clear)
        self.endgr()

        # run this code
        self.bu(side=BOTTOM, text='Run code', command=self.run_text, expand=0)

        self.fr(side=BOTTOM)
        self.te_code = self.te(height=10, width=25, side=BOTTOM)
        self.te_code.insert(END, 'world.clear()\n')
        self.te_code.insert(END, 'bob = Turtle(world)\n')
        self.endfr()

        # run file
        self.row([0,1], pady=30, side=BOTTOM, expand=0)
        self.bu(side=LEFT, text='Run file', command=self.run_file)
        self.en_file = self.en(side=LEFT, text='turtle_code.py', width=5)
        self.endrow()
        
        # leave the right frame open so that Turtles can add TurtleControls
        # self.endfr()

    def setup_run(self):
        """add a row of buttons for run, step, stop and clear"""
        self.gr(2, [1,1], [1,1], expand=0)
        self.bu(text='Run', command=self.run)
        self.bu(text='Stop', command=self.stop)
        self.bu(text='Step', command=self.step)
        self.bu(text='Quit', command=self.quit)
        self.endgr()

    def make_turtle(self):
        """create a new turtle and corresponding controller"""
        turtle = Turtle(self)
        control = TurtleControl(turtle)
        turtle.control = control

    def clear(self):
        """undraw and remove all the animals, and anything else
        on the canvas
        """
        for animal in self.animals:
            animal.undraw()
            if hasattr(animal, 'control'):
                animal.control.frame.destroy()
                
        self.animals = []
        self.canvas.delete('all')


class Turtle(Animal):
    """represent a Turtle in a TurtleWorld
    """
    def __init__(self, world=None, delay=0.1):
        """a Turtle has a radius (r), heading, pen (True/False for
        active/inactive), and a color.
        """
        if world == None:
            world = TurtleWorld.current_world

        Animal.__init__(self, world)        
        self.r = 5
        self.heading = 0
        self.pen = True
        self.color = 'red'
        self.delay = delay
        self.draw()
        world.register(self)

    def step(self):
        """default step behavior is forward one pixel"""
        self.fd()

    def draw_line(self, scale, dtheta, **options):
        """draw a line through the center of this turtle,
        with a dtheta angle from the turtle's heading,
        and length 2r"""
        r = scale * self.r
        theta = self.heading + dtheta
        head = self.polar(self.x, self.y, r, theta)
        tail = self.polar(self.x, self.y, -r, theta)
        self.world.canvas.line([tail, head], **options)

    def draw(self):
        """draw the turtle"""
        self.tag = 'Turtle%d' % id(self)
        lw = self.r/2
        
        # draw the line that makes the head and tail
        self.draw_line(2.5, 0, tags=self.tag, width=lw, arrow=LAST)

        # draw the diagonal that makes two feet
        self.draw_line(1.8, 40, tags=self.tag, width=lw)

        # draw the diagonal that makes the other two feet
        self.draw_line(1.8, -40, tags=self.tag, width=lw)

        # draw the shell
        self.world.canvas.circle([self.x, self.y], self.r, self.color,
                                 tags=self.tag)
        self.update()

    def fd(self, dist=1):
        """move the turtle foward by the given distance"""
        x, y = self.x, self.y
        p1 = [x, y]
        p2 = self.polar(x, y, dist, self.heading)
        self.x, self.y = p2

        # if the pen is down, draw a line
        if self.pen:
            self.world.canvas.line([p1, p2], fill='black')
        self.redraw()

    def bk(self, dist=1):
        """move the turtle backward by the given distance"""
        self.fd(-dist)

    def rt(self, angle=90):
        """turn right by the given angle"""
        self.heading = self.heading - angle
        self.redraw()

    def lt(self, angle=90):
        """turn left by the given angle"""
        self.heading = self.heading + angle
        self.redraw()

    def pd(self):
        """put the pen down (active)"""
        self.pen = True

    def pu(self):
        """put the pen up (inactive)"""
        self.pen = False

    def set_color(self, color):
        """change the color of the turtle and redraw.
        Note that changing the color attribute doesn't change the
        turtle on the canvas until redraw is invoked.  One way
        to address that would be to make color a property.
        """
        self.color = color
        self.redraw()


class TurtleControl(object):
    """some turtles have a turtle control panel in the GUI"""

    def __init__(self, turtle):
        self.turtle = turtle
        self.setup()

    def setup(self):
        w = self.turtle.world

        self.frame = w.fr(bd=2, relief=SUNKEN, padx=1, pady=1, expand=0)
        w.la(text='Turtle Control')

        # forward and back (and the entry that says how far)
        w.fr(side=TOP)
        w.bu(side=LEFT, text='bk', command=Callable(self.move_turtle, -1))
        self.en_dist = w.en(side=LEFT, fill=NONE, expand=0, width=5, text='10')
        w.bu(side=LEFT, text='fd', command=self.move_turtle)
        w.endfr()

        # other buttons
        w.fr(side=TOP)
        w.bu(side=LEFT, text='lt', command=self.turtle.lt)
        w.bu(side=LEFT, text='rt', command=self.turtle.rt)
        w.bu(side=LEFT, text='pu', command=self.turtle.pu)
        w.bu(side=LEFT, text='pd', command=self.turtle.pd)
        w.endfr()

        # color menubutton
        colors = 'red', 'orange', 'yellow', 'green', 'blue', 'violet'
        w.row([0,1])
        w.la('Color:')
        self.mb = w.mb(text=colors[0])
        for color in colors:
            w.mi(self.mb, text=color, command=Callable(self.color, color))

        w.endrow()
        w.endfr()

    def color(self, color):
        """callback for the menu button: change the color of the
        turtle and the text on the button"""
        self.mb.config(text=color)
        self.turtle.set_color(color)

    def move_turtle(self, sign=1):
        """callback for fd and bk buttons: read the entry and move
        the turtle.  sign should be +1 or -1 for fd or back."""
        dist = int(self.en_dist.get())
        self.turtle.fd(sign*dist)

# add the turtle methods to the module namespace
# so they can be invoked as simple functions (not methods)
fd = Turtle.fd
bk = Turtle.bk
lt = Turtle.lt
rt = Turtle.rt
pu = Turtle.pu
pd = Turtle.pd
die = Turtle.die
set_color = Turtle.set_color

if __name__ == '__main__':
    world = TurtleWorld(interactive=True)
    wait_for_user()
