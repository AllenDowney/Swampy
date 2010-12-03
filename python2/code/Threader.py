from TurtleWorld import *

class Threader(Turtle):
    def __init__(self, world):
        Turtle.__init__(self, world)
        self.delay = 0.005
        self.set_color('purple')

    def step():
        """Threaders don't need no stinkin' step method."""
    
    def moveto(self, x, y):
        self.x = x
        self.y = y
        self.redraw()

    def koch(self, n):
        if n<8:
            self.fd(n)
            return
        for angle in [-60, 120, -60, 0]:
            self.koch(n/3.0)
            self.rt(angle)

    def snowflake(self):
        for i in range(3):
            self.koch(300)
            self.rt(120)
        self.undraw()

def make_threader(world):
    t = Threader(world)
    t.moveto(-150, 90)
    t.snowflake()

world = TurtleWorld()
world.setup_interactive()
world.bu(text='Make Threader', command=Callable(make_threader, world))
world.mainloop()

