#!/usr/bin/python

"""

"""

"""
  Copyright 2005 Allen B. Downey

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see
    http://www.gnu.org/licenses/gpl.html or write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
    02110-1301 USA
    
"""


import random
import time
import threading
from Gui import *

class World(Gui):
    """the environment where Animals live.  A World usually
    includes a canvas where animals are drawn, and a control panel.
    """
    def __init__(self, *args, **kwds):
        Gui.__init__(self, *args, **kwds)
        self.title('World')
        
        # keep track of the most recent world
        World.current_world = self

        # exists is set to False when the user presses quit.
        self.exists = True    

        # list of animals that live in this world.
        self.animals = []

    def quit(self):
        """shut down the World."""
        # setting exists tells other threads that the world is gone
        self.exists = False
        Gui.quit(self)

    def register(self, animal):
        """add a new animal to the world"""
        self.animals.append(animal)

    def unregister(self, animal):
        """remove an animal from the world"""
        self.animals.remove(animal)

    def clear(self):
        """undraw and remove all the animals, and anything else
        on the canvas.
        """
        for animal in self.animals:
            animal.undraw()
        self.animals = []
        self.canvas.delete('all')

    def step(self):
        """invoke the step method on every animal
        """
        for animal in self.animals:
            animal.step()
        
    def run(self):
        """invoke step intermittently until the user presses
        Quit or Stop
        """
        self.running = True
        while self.exists and self.running:
            self.step()
            self.update()

    def stop(self):
        """stop running"""
        self.running = False

    def map_animals(self, callable):
        """apply the given callable to all animals"""
        map(callable, self.animals)
        
    def run_text(self):
        """get the code from the TextEntry widget in the control
        panel, and execute it.

        Precondition: self must have an Interpreter and a text entry"""
        source = self.te_code.get(1.0, END)
        self.inter.run_code(source, '<user-provided code>')

    def run_file(self):
        """read the code from the filename in the entry and run it.
        
        Precondition: self must have an Interpreter and a filename entry"""
        filename = self.en_file.get()
        fp = open(filename)
        source = fp.read()
        self.inter.run_code(source, filename)


class Interpreter(object):
    """this object encapsulates the environment where user-provided
    code will execute
    """
    def __init__(self, world, gs=None):

        # if the caller didn't provide globals, use the current env
        if gs == None:
            self.globals = globals()
        else:
            self.globals = gs
            
    def run_code_thread(self, *args):
        """run the given code in a new thread"""
        MyThread(self.run_code, *args)
        
    def run_code(self, source, filename):
        """run the given code in the saved environment"""
        code = compile(source, filename, 'exec')
        try:
            exec code in self.globals
        except KeyboardInterrupt:
            self.world.quit()


class MyThread(threading.Thread):
    """this is a wrapper for threading.Thread that improves
    the syntax for creating and starting threads.
    """
    def __init__(self, target, *args):
        threading.Thread.__init__(self, target=target, args=args)
        self.start()


class Animal(object):
    """Animal is an abstract class the specifies the methods an
    Animal child class needs to provide.
    """
    def __init__(self, world):
        """each animal has a location (x, y) and a reference to the
        world it lives in
        """
        self.world = world
        self.x = 0
        self.y = 0
        self.delay = 0
        
    def step(self):
        """subclasses should override this method"""
        pass

    def draw(self):
        """subclasses should override this method"""
        pass

    def undraw(self):
        try:
            # delete the items on the canvas that have my tag...
            self.world.canvas.delete(self.tag)
        except AttributeError:
            # ...assuming the canvas exists
            pass

    def die(self):
        """remove this animal from the world and undraw it"""
        self.world.unregister(self)
        self.undraw()

    def redraw(self):
        """undraw and then redraw this animal"""
        self.undraw()
        self.draw()

    def update(self):
        """update the world and then sleep"""
        self.world.update()
        time.sleep(self.delay)

    def polar(self, x, y, r, theta):
        """convert polar coordinates (r, theta) to cartesian
        coordinates with the origin at (x, y).  (theta is in degrees)"""
        rad = theta * math.pi/180
        s = math.sin(rad)
        c = math.cos(rad)
        return [ x + r * c, y + r * s ]         


def wait_for_user():
    """invoke mainloop on the most recent World"""
    World.current_world.mainloop()

if __name__ == '__main__':

    # make a generic world
    world = World()

    # create a canvas and put a text item on it
    world.ca().text([0,0], 'hello')

    # wait for the user
    wait_for_user()
