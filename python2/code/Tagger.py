"""

This module is part of an exercise for
Think Python: an Introduction to Software Design
Allen B. Downey

"""

from Wobbler import *
import math

class Missed(Exception):
    """this is the exception raised when a turtle tries to tag
    someone too far away"""

class Tagger(Wobbler):

    def __init__(self, world, speed=1, clumsiness=60, color='red'):
        Wobbler.__init__(self, world, speed, clumsiness, color)
        self.it = 0
        self.sulking = 0

    def steer(self):
        """steer the Wobbler in the general direction it should go.
        Postcondition: the Wobbler's heading may be changed, but
        its position may not."""
        
        # if sulking, decrement the sulking clock
        if self.sulking > 0:
            self.sulking -= 1
            if self.sulking == 0:
                self.color = 'red'
                self.speed = self.old_speed
            return

        # if out of bounds, turn toward the center
        if self.distance() > 200:
            self.turn_toward(0, 0)
            return

        # if not it, just wander
        if not self.it:
            return

        # if it, chase the closest player
        target = self.closest(self.world.animals)
        try:
            self.apply_tag(target)
        except Missed:
            self.chase(target)
        

    def turn_toward(self, x=0, y=0):
        """turn to face the given point"""
        self.heading = self.away(x, y) + 180
        self.redraw()

    def away(self, x=0, y=0):
        """compute the angle (in degrees) that faces away from
        the given point"""
        dx = self.x - x
        dy = self.y - y
        heading = math.atan2(dy, dx)
        return heading * 180 / math.pi

    def distance(self, x=0, y=0):
        """compute the distance from this turtle to the given point"""
        dx = self.x - x
        dy = self.y - y
        return math.sqrt(dx**2 + dy**2)

    def distance_from(self, other):
        """compute the distance between turtles"""
        return self.distance(other.x, other.y)

    def youre_it(self):
        """make this turtle 'it' """
        self.it = 1
        self.old_speed = self.speed
        self.old_color = self.color
        self.speed = 0
        self.color = 'blue'
        self.sulking = 200
        self.redraw()

    def not_it(self):
        """make this turtle not 'it' """
        self.it = 0
        self.color = self.old_color
        self.redraw()

    def away(self, x=0, y=0):
        """compute the angle (in degrees) that faces away from
        the given point"""
        dx = self.x - x
        dy = self.y - y
        heading = math.atan2(dy, dx)
        return heading * 180 / math.pi

    def flee(self, other):
        """face away from the other turtle"""
        self.heading = self.away(other.x, other.y)
        
    def chase(self, other):
        """face the other turtle"""
        self.turn_toward(other.x, other.y)

    def turn_toward(self, x=0, y=0):
        """turn to face the given point"""
        self.heading = self.away(x, y) + 180
        self.redraw()

    def closest(self, others):
        """return the animal in the list that is closest to self
        (not including self!)"""
        t = [(self.distance_from(animal), animal)
              for animal in others if animal is not self]
        (distance, animal) = min(t)
        return animal

    def apply_tag(self, other):
        """try to tag the other turtle.  if it is too far away,
        raise an exception"""
        if self.distance_from(other) < 10:
            self.not_it()
            other.youre_it()
        else:
            # other.flee(self)
            raise Missed


if __name__ == '__main__':
    world = make_world(Tagger)
    world.animals[0].youre_it()
    world.mainloop()
