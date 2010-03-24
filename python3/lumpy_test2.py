#!/usr/bin/python

from TurtleWorld import *

import Lumpy
lumpy = Lumpy.Lumpy()
lumpy.opaque_class(Interpreter)
lumpy.make_reference()

world = TurtleWorld()
bob = Turtle(world)

lumpy.object_diagram()
lumpy.class_diagram()

