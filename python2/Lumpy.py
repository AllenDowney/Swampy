#!/usr/bin/python

"""UML diagrams for Python

Lumpy generates UML diagrams (currently object and class diagrams)
from a running Python program. It is similar to a graphical debugger
in the sense that it generates a visualization of the state of a
running program, but it is different from a debugger in the sense that
it tries to generate high-level visualizations that are compliant (at
least in spirit) with standard UML.

There are three target audiences for this module: teachers, students
and software engineers. Teachers can use Lumpy to generate figures
that demonstrate a model of the execution of a Python
program. Students can use Lumpy to explore the behavior of the Python
interpreter. Software engineers can use Lumpy to extract the structure
of existing programs by diagramming the relationships among the
classes, including classes defined in libraries and the Python
interpreter.


  Copyright 2005 Allen B. Downey

    This file contains wrapper classes I use with tkinter.  It is
    mostly for my own use; I don't support it, and it is not very
    well documented.

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



import inspect, traceback
from Gui import *

# get the version of Python
v = sys.version.split()[0].split('.')
major = int(v[0])

if major < 2:
    print 'You must have at least Python version 2.0 to run Lumpy.'
    sys.exit()

minor = int(v[1])
if major == 2 and minor < 4:
    # TODO: need to find a substitute implementation of set
    pass
        
if major == 2:
    tkinter_module = Tkinter
else:
    tkinter_module = tkinter

# most text uses the font specified below; some labels
# in object diagrams use smallfont.  Lumpy uses the size
# of the fonts to define a length unit, so
# changing the font sizes will cause the whole diagram to
# scale up or down.
font = ("Helvetica", 12)
smallfont = ("Helvetica", 10)


class DiagCanvas(GuiCanvas):
    """a Canvas for displaying Diagrams"""
    
    def box(self, box, padx=0.5, pady=0.3, **options):
        """draw a rectangle with the given bounding box, expanded
        by padx and pady.  box can be a Bbox object or a list of
        two coordinate pairs.
        """

        # underride sets default values only if the called hasn't
        underride(options, outline='black')
        box.left -= padx
        box.top -= pady
        box.right += padx
        box.bottom += pady
        item = self.rectangle(box, **options)
        return item

    def arrow(self, start, end, **options):
        """draw an arrow: start and end can be a Point object or
        a list of two coordinates
        """
        return self.line([start, end], **options)

    def str(self, pos, text, dx=0, dy=0, **options):
        """draw the given text at the given position, with an offset
        specified by dx and dy
        """
        underride(options, fill='black', font=font, anchor=W)
        x, y = pos
        x += dx
        y += dy
        return self.text([x, y], text, **options)
        
    def dot(self, pos, r=0.2, **options):
        """draw a dot at the given position with radius r"""
        underride(options, fill='white', outline='orange')
        return self.circle(pos, r, **options)
        
    def measure(self, t, **options):
        """find the bounding box of the list of words by
        drawing them, measuring them, and then deleting them
        """
        pos = Point([0,0])
        tags = 'temp'
        for s in t:
            self.str(pos, s, tags=tags, **options)
            pos.y += 1
        bbox = self.bbox(tags)
        self.delete(tags)
        return bbox
    

nextid = 0
def make_tags(prefix='Tag'):
    """return a tuple with a single element: a tag string with
    with the given prefix and a unique id as a suffix
    """
    global nextid
    nextid += 1
    id = '%s%d' % (prefix, nextid)
    return id,


class Thing(object):
    """the parent class for objects that have a graphical
    representation.  Each Thing object corresponds to an item
    or set of items in a diagram.  A Thing can only be drawn in
    one Diagram at a time.
    """
    things_created = 0
    things_drawn = 0

    def __new__(cls, *args, **kwds):
        """override __new__ so we can count the number of Things"""
        Thing.things_created += 1
        return object.__new__(cls)
    
    def bbox(self):
        """return the bounding box of this object if it is drawn
        """
        return self.canvas.bbox(self.tags)
    
    def set_offset(self, pos):
        """the offset attribute keeps track of the offset between
        the bounding box of the Thing and its nominal position, so
        that if the Thing is moved later, we can compute its new
        nominal position.
        """
        self.offset = self.bbox().offset(pos)

    def pos(self):
        """Compute the nominal position of a Thing by getting the
        current bounding box and adding the offset.
        """
        return self.bbox().pos(self.offset)

    def isdrawn(self):
        """return True if the object has been drawn"""
        return hasattr(self, 'drawn')

    def draw(self, diag, pos, flip, tags=tuple()):
        """draw this Thing at the given position on the given
        diagram with the given tags (in addition to the specific
        tag for this thing).  flip=1 means draw left to right;
        flip=-1 means right to left.  Return a list of Things
        that were drawn.

        draw and drawme are not allowed to mofify pos
        """
        if self.isdrawn():
            return []

        self.drawn = True
        self.diag = diag
        self.canvas = diag.canvas

        # keep track of how many things have been drawn.
        # Simple values can get drawn more than once, so the
        # total number of things drawn can be greater than
        # the number of things.
        Thing.things_drawn += 1
        if Thing.things_drawn % 100 == 0:
            print Thing.things_drawn
            #self.diag.lumpy.update()

        # each thing has a list of tags: its own tag plus
        # the tag of each thing it belongs to.  This convention
        # makes it possible to move entire structures with one
        # move command.
        self.tags = make_tags(self.__class__.__name__)
        tags += self.tags

        # invoke drawme in the child class
        drawn = self.drawme(diag, pos, flip, tags)
        if drawn == None:
            drawn = [self]
            
        self.set_offset(pos)
        return drawn

    def bind(self, tags=None):
        """create bindings for each of the items with the given tags
        """
        tags = tags or self.tags
        items = self.canvas.find_withtag(tags)
        for item in items:
            self.canvas.tag_bind(item, "<Button-1>", self.down)

    def down(self, event):
        """this callback is invoked when the user clicks on an item
        """
        self.dragx = event.x
        self.dragy = event.y
        self.canvas.bind("<B1-Motion>", self.motion)
        self.canvas.bind("<ButtonRelease-1>", self.up)
        return True

    def motion(self, event):
        """this callback is invoked when the user drags an item"""
        dx = event.x - self.dragx
        dy = event.y - self.dragy

        self.dragx = event.x
        self.dragy = event.y

        self.canvas.move(self.tags, dx, dy)
        self.diag.update_arrows()
  
    def up(self, event):
        """this callback is invoked when the user releases the button"""
        event.widget.unbind ("<B1-Motion>")
        event.widget.unbind ("<ButtonRelease-1>")
        self.diag.update_arrows()


class Dot(Thing):
    """the Thing that represents a dot in a diagram"""
    def drawme(self, diag, pos, flip, tags=tuple()):
        self.canvas.dot(pos, tags=tags)


class Simple(Thing):
    """the graphical representation of a simple value like a number
    or a string"""
    def __init__(self, lumpy, val):
        lumpy.register(self, val)
        self.val = val

    def drawme(self, diag, pos, flip, tags=tuple()):
        p = pos.copy()
        p.x += 0.1 * flip        
        anchor = {1:W, -1:E}

        # put quotes around strings; for everything else, use
        # the standard str representation
        val = self.val
        maxlen = 30
        if isinstance(val, str):
            val = val.strip('\n')
            label = "'%s'" % val[0:maxlen]
        else:
            label = str(val)
        
        self.canvas.str(p, label, tags=tags, anchor=anchor[flip])
        self.bind()


class Index(Simple):
    """the graphical representation of an index in a Sequence.
    An Index object does not register with lumpy, so that even
    in pedantic mode, it is always drawn, and it is never the
    target of a reference (since it is not really a value at
    run-time).
    """
    def __init__(self, lumpy, val):
        self.val = val

    def drawme(self, diag, pos, flip, tags=tuple()):
        p = pos.copy()
        p.x += 0.1 * flip        
        anchor = {1:W, -1:E}

        label = str(self.val)
        
        self.canvas.str(p, label, tags=tags, anchor=anchor[flip])
        self.bind()

class Mapping(Thing):
    """the graphical representation of a mapping type (usually a
    dictionary).  Sequence and Instance inherit from Mapping."""
    
    def __init__(self, lumpy, val):
        lumpy.register(self, val)
        self.bindings = make_kvps(lumpy, val.items())
        self.boxoptions = dict(outline='purple')

        if lumpy.pedantic:
            self.label = type(val).__name__
        else:
            self.label = ''

    def bbox(self):
        """the bbox of a Mapping is the bbox of its box item.
        This is different from other Things.
        """
        return self.canvas.bbox(self.boxitem)

    def drawme(self, diag, pos, flip, tags=tuple()):
        """drawme is the middle part of the way objects are drawn.
        Thing.draw does some prep work, invokes drawme, and then
        does some cleanup.  draw and drawme are not allowed to
        modify pos.
        """
        p = pos.copy()

        # intag is attached to items that should be considered
        # inside the box
        intag = self.tags[0] + 'inside'

        # draw the bindings
        for binding in self.bindings:
            # check whether the key was already drawn
            drawn = binding.key.isdrawn()

            # draw the binding
            binding.draw(diag, p, flip, tags=tags)

            # apply intag to the dots 
            self.canvas.addtag_withtag(intag, binding.dot.tags)
            if drawn:
                # if the key was already drawn, then the binding
                # contains two dots, so we should add intag to the
                # second one.
                if binding.dot2:
                    self.canvas.addtag_withtag(intag, binding.dot2.tags)
            else:
                # if the key wasn't drawn yet, it should be
                # considered inside this mapping
                self.canvas.addtag_withtag(intag, binding.key.tags)

            # move down to the position for the next binding
            p.y = binding.bbox().bottom + 1.8

        if len(self.bindings):
            # if there are any bindings, draw a box around them
            bbox = self.canvas.bbox(intag)
            item = self.canvas.box(bbox, tags=tags, **self.boxoptions)
        else:
            # otherwise just draw a box
            bbox = BBox([p.copy(), p.copy()])
            item = self.canvas.box(bbox, padx=0.4, pady=0.4, tags=tags,
                              **self.boxoptions)

        # make the box clickable
        self.bind(item)
        self.boxitem = item

        # put the label above the box
        if self.label:
            p = bbox.upperleft()
            item = self.canvas.str(p, self.label, anchor=SW,
                              font=smallfont, tags=tags)
            # make the label clickable
            self.bind(item)

        # if the whole mapping is not in the right position, shift it.
        if flip == 1:
            dx = pos.x - self.bbox().left
        else:
            dx = pos.x - self.bbox().right

        self.canvas.move(self.tags, dx, 0, transform=True)

    def scan_bindings(self, cls):
        """scan the bindings in this mapping, looking for
        references to other object types.  cls is the Class
        of the object that contains this mapping"""
        for binding in self.bindings:
            for val in binding.vals:
                self.scan_val(cls, val)

    def scan_val(self, cls, val):
        """if we find a reference to an object type, make a note
        of the HAS-A relationship.  If we find a reference to a
        container type, scan it for references."""        
        if isinstance(val, Instance) and val.cls is not None:
            cls.add_hasa(val.cls)
        elif isinstance(val, Sequence):
            val.scan_bindings(cls)
        elif isinstance(val, Mapping):
            val.scan_bindings(cls)
        

class Sequence(Mapping):
    """the graphical representation of a sequence type (mostly
    lists and tuples)
    """
    def __init__(self, lumpy, val):
        lumpy.register(self, val)
        self.bindings = make_bindings(lumpy, enumerate(val))

        if lumpy.pedantic:
            self.label = type(val).__name__
        else:
            self.label = ''

        # color code lists, tuples, and other sequences
        if isinstance(val, list):
            self.boxoptions = dict(outline='green1')
        elif isinstance(val, tuple):
            self.boxoptions = dict(outline='green4')
        else:
            self.boxoptions = dict(outline='green2')


class Instance(Mapping):
    """The graphical representation of an object (usually).
    Anything with a __dict__ is treated as an Instance.
    """
    def __init__(self, lumpy, val):
        lumpy.register(self, val)

        # if this object has a class, make a Thing to
        # represent the class, too
        if hasclass(val):
            class_or_type = val.__class__
            self.cls = make_thing(lumpy, class_or_type)
        else:
            class_or_type = type(val)
            self.cls = None
            
        self.label = class_or_type.__name__

        if class_or_type in lumpy.instance_vars:
            # if the class is in the list, only display only the
            # unrestricted instance variables
            ks = lumpy.instance_vars[class_or_type]
            it = [(k, getattr(val, k)) for k in ks]
            seq = make_bindings(lumpy, it)
        else:
            # otherwise, display all of the instance variables
            if hasdict(val):
                it = val.__dict__.iteritems()
            elif hasslots(val):
                it = [(k, getattr(val, k)) for k in val.__slots__]
            else:
                t = [k for k, v in type(val).__dict__.iteritems()
                     if str(v).find('attribute') == 1]
                it = [(k, getattr(val, k)) for k in t]
            
            seq = make_bindings(lumpy, it)

            # and if the object extends list, tuple or dict,
            # append the items
            if isinstance(val, (list, tuple)):
                seq += make_bindings(lumpy, enumerate(val))

            if isinstance(val, dict):
                seq += make_bindings(lumpy, val.iteritems())

        # if this instance has a name attribute, show it
        attr = '__name__'
        if hasname(val):
            seq += make_bindings(lumpy, [[attr, val.__name__]])

        self.bindings = seq
        self.boxoptions = dict(outline='red')

    def scan_bindings(self, cls):
        """scan the bindings in this Instance, looking for
        references to other object types; also, make a note
        of the names of the instance variables.
        cls is the Class object this instance belongs to.
        """
        for binding in self.bindings:
            cls.add_ivar(binding.key.val)
            for val in binding.vals:
                self.scan_val(cls, val)

class Frame(Mapping):
    """The graphical representation of a frame,
    implemented as a list of Bindings"""
    def __init__(self, lumpy, frame):
        it = frame.locals.iteritems()
        self.bindings = make_bindings(lumpy, it)
        self.label = frame.func
        self.boxoptions = dict(outline='blue')
    


# the following are short functions that check for certain attributes
def hasname(obj): return hasattr(obj, '__name__')
def hasclass(obj): return hasattr(obj, '__class__')
def hasdict(obj): return hasattr(obj, '__dict__')
def hasslots(obj): return hasattr(obj, '__slots__')
def hasdiag(obj): return hasattr(obj, 'diag')
def iscallable(obj): return hasattr(obj, '__call__')


class Class(Instance):
    """a graphical representation of a Class.  It inherits
    from Instance, which controls how a Class appears in an
    object diagram, and contains a ClassDiagramClass, which
    controls how the Class appears in a class diagram.
    """
    def __init__(self, lumpy, classobj):
        Instance.__init__(self, lumpy, classobj)
        self.cdc = ClassDiagramClass(lumpy, classobj)
        self.cdc.cls = self
        
        lumpy.classes.append(self)
        
        self.classobj = classobj
        self.module = classobj.__module__
        self.bases = classobj.__bases__

        # childs is the list of classes that inherit directly
        # from this one; parents is the list of base classes
        # for this one
        self.childs = []

        # refers is a dictionary that records, for each other
        # class, the total number of references we have found from
        # this class to that
        self.refers = {}

        # make a list of Things to represent the
        # parent classes
        if lumpy.is_opaque(classobj):
            self.parents = []
        else:
            self.parents = [make_thing(lumpy, base) for base in self.bases]

        # add self to the parents' lists of children
        for parent in self.parents:
            parent.add_child(self)

        # height and depth are used to lay out the tree
        self.height = None
        self.depth = None
        
    def add_child(self, child):
        """when a subclass is created, it notifies its parent
        classes, who update their list of children"""
        self.childs.append(child)

    def add_hasa(self, child, n=1):
        """increment the number of references we have found
        from this class to the given child class"""
        self.refers[child] = self.refers.get(child, 0) + n

    def set_height(self):
        """compute the maximum height between this class and
        a leaf class (one with no children)
        """
        if self.height != None:
            return
        if not self.childs:
            self.height = 0
            return
        for child in self.childs:
            child.set_height()
            
        heights = [child.height for child in self.childs]
        self.height = max(heights) + 1

    def set_depth(self):
        """compute the maximum depth between this class and
        a root class (one with no parents)
        """
        if self.depth != None:
            return
        if not self.parents:
            self.depth = 0
            return
        for parent in self.parents:
            parent.set_depth()
            
        depths = [parent.depth for parent in self.parents]
        self.depth = max(depths) + 1

    def add_ivar(self, var):
        """add to the set of instance variables for this class
        """
        self.cdc.ivars.add(var)


class ClassDiagramClass(Thing):
    """a graphical representation of a Class as it appears
    in a Class Diagram (which is different from the way class
    objects appear in Object Diagrams).
    """
    def __init__(self, lumpy, classobj):
        self.lumpy = lumpy
        self.classobj = classobj

        # self.methods is the list of methods defined in this class.
        # self.cvars is the list of class variables.
        # self.ivars is a set of instance variables.
        
        self.methods = []
        self.cvars = []
        self.ivars = set()

        # if this is a restricted (or opaque) class, then
        # vars contains the list of instance variables that
        # will be shown; otherwise it is None.
        try:
            vars = lumpy.instance_vars[classobj]
        except KeyError:
            vars = None

        # we can get methods and class variables now, but we
        # have to wait until the Lumpy representation of the stack
        # is complete before we can go looking for instance vars.
        for key, val in classobj.__dict__.items():
            if vars != None and key not in vars: continue
            
            if iscallable(val):
                self.methods.append(val)
            else:
                self.cvars.append(key)

        key = lambda x: x.__class__.__name__ + "."  + x.__name__
        self.methods.sort(key=key)
        self.cvars.sort()

        self.boxoptions = dict(outline='blue')
        self.lineoptions = dict(fill='blue')


    def drawme(self, diag, pos, flip, tags=tuple()):
        p = pos.copy()

        # draw the name of the class
        name = self.classobj.__name__
        item = self.canvas.str(p, name, tags=tags)
        p.y += 0.8

        # in order to draw lines between segments, we have
        # to store the locations and draw the lines, later,
        # when we know the location of the box
        lines = []

        # draw a line between the name and the methods
        if self.methods:
            lines.append(p.y)
            p.y += 1

        # draw the methods
        for f in self.methods:
            item = self.canvas.str(p, f.__name__, tags=tags)
            p.y += 1

        # draw the class variables
        cvars = self.cvars
        try:
            cvars.remove('__doc__')
            cvars.remove('__module__')
        except:
            pass
        
        # draw the class variables
        if cvars:
            lines.append(p.y)
            p.y += 1

        for varname in cvars:
            item = self.canvas.str(p, varname, tags=tags)
            p.y += 1

        # if this is a restricted (or opaque) class, remove
        # unwanted instance vars from self.ivars
        try:
            vars = self.lumpy.instance_vars[self.classobj]
            self.ivars.intersection_update(vars)
        except KeyError:
            pass
            
        # draw the instance variables
        ivars = list(self.ivars)
        ivars.sort()
        if ivars:
            lines.append(p.y)
            p.y += 1

        for varname in ivars:
            item = self.canvas.str(p, varname, tags=tags)
            p.y += 1

        # draw the box
        bbox = self.bbox()
        item = self.canvas.box(bbox, tags=tags, **self.boxoptions)
        self.boxitem = item

        # draw the lines
        for y in lines:
            coords = [[bbox.left, y], [bbox.right, y]]
            item = self.canvas.line(coords, tags=tags, **self.lineoptions)

        # only the things we have drawn so far should be bound
        self.bind()

        # make a list of all classes drawn
        alldrawn = [self]

        # draw the descendents of this class
        childs = self.cls.childs

        if childs:
            q = pos.copy()
            q.x = bbox.right + 8
            
            drawn = self.diag.draw_classes(childs, q, tags)
            alldrawn.extend(drawn)

            self.head = self.arrow_head(diag, bbox, tags)

            # connect this class to its children
            for child in childs:
                a = ParentArrow(self.lumpy, self, child.cdc)
                self.diag.add_arrow(a)

        # if the class is not in the right position, shift it.
        dx = pos.x - self.bbox().left
        self.canvas.move(self.tags, dx, 0)

        return alldrawn

    def arrow_head(self, diag, bbox, tags, size=0.5):
        """draw the hollow arrow head that connects this class
        to its children.
        """
        x, y = bbox.midright()
        x += 0.1
        coords = [[x, y], [x+size, y+size], [x+size, y-size], [x, y]]
        item = self.canvas.line(coords, tags=tags, **self.lineoptions)
        return item


class Binding(Thing):
    """the graphical representation of the binding between a
    key and a value.
    """
    def __init__(self, lumpy, key, val):
        lumpy.register(self, (key, val))
        self.key = key
        self.vals = [val]

    def rebind(self, val):
        self.val.append(val)

    def draw_key(self, diag, p, flip, tags):
        """draw a reference to a previously-drawn key rather
        than drawing the key inside the mapping.
        """
        p.x -= 0.7 * flip
        self.dot2 = Dot()
        self.dot2.draw(diag, p, -flip, tags=tags)

        # only the things we have drawn so far should
        # be handles for this binding
        self.bind()

        if not self.key.isdrawn():
            p.x -= 2.0 * flip
            self.key.draw(diag, p, -flip, tags=tags)
        a = ReferenceArrow(self.lumpy, self.dot2, self.key, fill='orange')
        diag.add_arrow(a)
        

    def drawme(self, diag, pos, flip, tags=tuple()):
        self.dot = Dot()
        self.dot.draw(diag, pos, flip, tags=tags)
        
        p = pos.copy()
        p.x -= 0.7 * flip

        # if the key is a Simple, try to draw it inside the mapping;
        # otherwise, draw a reference to it
        if isinstance(self.key, Simple):
            drawn = self.key.draw(diag, p, -flip, tags=tags)

            # if a Simple thing doesn't get drawn, we must be in
            # pedantic mode.
            if drawn:
                self.bind()
                self.dot2 = None
            else:
                self.draw_key(diag, p, flip, tags)                
        else:
            self.draw_key(diag, p, flip, tags)                

        p = pos.copy()
        p.x += 2.0 * flip

        for val in self.vals:
            val.draw(diag, p, flip, tags=tags)
            a = ReferenceArrow(self.lumpy, self.dot, val, fill='orange')
            diag.add_arrow(a)
            p.y += 1


class ReferenceArrow(Thing):
    """a reference arrow, which show a reference in an object diagram
    """
    def __init__(self, lumpy, key, val, **options):
        self.lumpy = lumpy
        self.key = key
        self.val = val
        self.options = options
        
    def draw(self, diag):
        self.diag = diag
        canvas = diag.canvas
        self.item = canvas.arrow(self.key.pos(), self.val.pos(),
                                 **self.options)
        self.item.lower()

    def update(self):
        if not hasdiag(self): return
        self.item.coords([self.key.pos(), self.val.pos()])


class ParentArrow(Thing):
    """an inheritance arrow, which shows an is-a relationship
    between classes in a class diagram.
    """
    def __init__(self, lumpy, parent, child, **options):
        self.lumpy = lumpy
        self.parent = parent
        self.child = child
        underride(options, fill='blue')
        self.options = options
        
    def draw(self, diag):
        self.diag = diag
        parent, child = self.parent, self.child

        # the line connects the midleft point of the child
        # to the arrowhead of the parent; it always contains
        # two horizontal segments and one vertical.
        canvas = diag.canvas
        bbox = canvas.bbox(parent.head)
        p = bbox.midright()
        q = canvas.bbox(child.boxitem).midleft()
        midx = (p.x + q.x) / 2.0
        m1 = [midx, p.y]
        m2 = [midx, q.y]
        coords = [p, m1, m2, q]
        self.item = canvas.line(coords, **self.options)
        canvas.lower(self.item)

    def update(self):
        if not hasdiag(self): return
        self.diag.canvas.delete(self.item)
        self.draw(self.diag)


class ContainsArrow(Thing):
    """a contains arrow, which shows a has-a relationship between
    classes in a class diagram.
    """
    def __init__(self, lumpy, parent, child, **options):
        self.lumpy = lumpy
        self.parent = parent
        self.child = child
        underride(options, fill='orange', arrow=LAST)
        self.options = options
        
    def draw(self, diag):
        self.diag = diag
        parent, child = self.parent, self.child

        if not child.isdrawn():
            self.item = None
            return
        
        canvas = diag.canvas
        p = canvas.bbox(parent.boxitem).midleft()
        q = canvas.bbox(child.boxitem).midright()
        coords = [p, q]
        self.item = canvas.line(coords, **self.options)
        canvas.lower(self.item)

    def update(self):
        if not hasdiag(self): return
        self.diag.canvas.delete(self.item)
        self.draw(self.diag)



class Stack(Thing):
    """The graphical representation of a stack.
    """
    def __init__(self, lumpy, snapshot):
        self.lumpy = lumpy
        self.frames = [Frame(lumpy, frame) for frame in snapshot.frames]
    
    def drawme(self, diag, pos, flip, tags=tuple()):
        p = pos.copy()
        
        for frame in self.frames:
            frame.draw(diag, p, flip, tags=tags)
            bbox = self.bbox()
            #p.y = bbox.bottom + 3
            p.x = bbox.right + 3


def make_bindings(lumpy, iterator):
    """return a list of bindings, one for each key-value pair
    in iterator.  The keys are made into Index objects.
    """
    seq = [Binding(lumpy, Index(lumpy, k), make_thing(lumpy, v))
           for k, v in iterator]
    return seq


def make_kvps(lumpy, iterator):
    """return a list of bindings, one for each key-value pair
    in iterator.  The keys are made into Thing objects.
    """
    seq = [Binding(lumpy, make_thing(lumpy, k), make_thing(lumpy, v))
           for k, v in iterator]
    return seq


def make_thing(lumpy, val):
    """return the Thing that represents this value, either
    by making a new one or looking up an existing one.
    """
    # if we're being pedantic, then we always show aliased
    # values
    if lumpy.pedantic:
        thing = lumpy.lookup(val)
        if thing != None: return thing

    # otherwise for simple immutable types, ignore aliasing and
    # just draw
    simple = (str, bool, int, long, float, complex, type(None))

    if isinstance(val, simple):
        thing = Simple(lumpy, val)
        return thing

    # now check for aliasing even if we're not pedantic
    thing = lumpy.lookup(val)
    if thing != None: return thing

    # check the type of the value and dispatch accordingly
    if type(val) == type(Lumpy) or type(val) == type(type(int)):
        thing = Class(lumpy, val)  
    elif hasdict(val) or hasslots(val):
        thing = Instance(lumpy, val)
    elif isinstance(val, (list, tuple)):
        thing = Sequence(lumpy, val)
    elif isinstance(val, dict):
        thing = Mapping(lumpy, val)
    elif isinstance(val, object):
        thing = Instance(lumpy, val)
    else:
        # print "Couldn't classify", val, type(val)
        thing = Simple(lumpy, val)

    return thing


class Snapframe(object):
    """the data structure that represents a frame"""
    def __init__(self, tup):
        frame, filename, lineno, self.func, lines, index = tup
        (self.arg_names,
         self.args,
         self.kwds,
         locals) = inspect.getargvalues(frame)

        # make a copy of the dictionary of local vars
        self.locals = dict(locals)

        # the function name for the top-most frame is __main__
        if self.func == '?':
            self.func = '__main__'

    def subtract(self, other):
        """delete all the keys in other from self
        """
        for key in other.locals:
            try:
                del self.locals[key]
            except KeyError:
                print key, "this shouldn't happen"

class Snapshot(object):
    """the data structure that represents a stack"""

    def __init__(self):
        """convert from the format returned by inspect
        to a list of frames.  Drop the last three frames,
        which are the Lumpy functions object_diagram, make_stack,
        and Stack.__init__
        """
        st = inspect.stack()
        frames = [Snapframe(tup) for tup in st[3:]]
        frames.reverse()
        self.frames=frames

    def spew(self):
        """print the frames in this snapshot"""
        for frame in self.frames:
            print frame.func, frame

    def clean(self, ref):
        """Remove all the variables in the reference stack from self"""
        # NOTE: This currently only works on the top-most frame
        f1 = self.frames[0]
        f2 = ref.frames[0]
        f1.subtract(f2)
                    

class Lumpy(Gui):
    """the Lumpy object represents the GUI window.
    """
    def __init__(self, debug=False, pedantic=False):
        """debug is passed to Gui.__init__; it makes the outlines
        of the frames visible.
        If pedantic is false, simple values are replicated, rather
        than, for example, having all references to 1 refer to the
        same int object.
        """
        Gui.__init__(self, debug)
        self.pedantic = pedantic
        self.withdraw()

        # initially there is no object diagram, no class diagram
        # and no representation of the stack.
        self.od = None
        self.cd = None
        self.stack = None

        # instance_vars maps from classes to the instance vars
        # that are drawn for that class; for opaque classes, it
        # is an empty list.

        # an instance of an opaque class is shown with a small empty box;
        # the contents are not shown.
        self.instance_vars = {}

        # the following classes are opaque by default
        self.opaque_class(Lumpy)
        self.opaque_class(Gui)
        self.opaque_class(object)
        self.opaque_class(type(make_thing))    # function
        self.opaque_class(Exception)
        self.opaque_class(set)

        # any object that belongs to a class in the Tkinter module
        # is opaque (the name of the module depends on the Python version)
        self.opaque_module(tkinter_module)

        # by default, class objects and module objects are opaque
        classobjtype = type(Lumpy)
        self.opaque_class(classobjtype)
        modtype = type(inspect)
        self.opaque_class(modtype)

        # the __class__ of a new-style object is a type object.
        # when type objects are drawn, show only the __name__
        self.opaque_class(type)

        self.make_reference()

    def restrict_class(self, classobj, vars=None):
        """restrict this class so that when it is drawn, only
        the given vars are shown
        """
        if vars == None: vars = []
        self.instance_vars[classobj] = vars

    def opaque_class(self, classobj):
        """restrict this class to no variables"""
        self.restrict_class(classobj, None)

    def is_opaque(self, classobj):
        """check whether this class is completely opaque
        (restricted to _no_ instance variables)"""
        try:
            return self.instance_vars[classobj] == []
        except KeyError:
            return False

    def transparent_class(self, classobj):
        """remove the given type or class from the dictionary, which
        means that it's attributes will be shown.  If it is not in
        the dictionary, raise an exception."""
        del self.instance_vars[classobj]
        
    def opaque_module(self, modobj):
        """make all classes defined in this module opaque"""
        for var, val in modobj.__dict__.iteritems():
            if isinstance(val, type(Lumpy)):
                self.opaque_class(val)

    def make_reference(self):
        """make a reference point by taking a snapshot of the current
        state.  Subsequent diagrams will be relative to this reference.
        """
        self.make_reference2()

    def make_reference2(self):
        """this extra method call is here so that the reference
        and the snapshot we take later have the same number of
        frames on the stack.  UGH.
        """
        self.ref = Snapshot()

    def make_stack(self):
        """take a snapshot of the current state, subtract away the
        frames and variables that existed in the previous reference,
        then make a Stack.
        """
        self.snapshot = Snapshot()
        self.snapshot.clean(self.ref)
        
        self.values = {}
        self.classes = []
        self.stack = Stack(self, self.snapshot)
                
    def register(self, thing, val):
        """associate a value with the Thing that represents it,
        so that we can check later whether we have already created
        a Thing for a given value. """
        thing.lumpy = self
        thing.val = val
        self.values[id(val)] = thing
    
    def lookup(self, val):
        """check to see whether the given value is already represented
        by a Thing, and if so, return it.
        """
        vid = id(val)
        return self.values.get(vid, None)

    def object_diagram(self, obj=None):
        """create a new object diagram based on the current state.
        If an object is provided, draw the object.  Otherwise, draw
        the current run-time stack (relative to the last reference).
        """
        if obj:
            thing = make_thing(self, obj)
        else:
            if self.stack == None:
                self.make_stack()
            thing = self.stack

        # if there is already an Object Diagram, clear it; otherwise,
        # create one
        if self.od:
            self.od.clear()
        else:
            self.od = ObjectDiagram(self)

        # draw the object or stack, then the arrows
        self.od.draw(thing)
        self.od.draw_arrows()

        # wait for the user
        self.mainloop()

    def get_class_list(self):
        """return the list of classes that should be drawn in
        a class diagram
        """
        t = []
        for cls in self.classes:
            if not self.is_opaque(cls.classobj):
                t.append(cls)
            elif cls.parents or cls.childs:
                t.append(cls)
            
        return t

    def class_diagram(self, classes=None):
        """create a new object diagram based on the current state.
        If a list of classes is provided, only those classes are
        shown.  Otherwise, all classes that Lumpy know about are shown.
        """

        # if there is not already a snapshot, make one
        if self.stack == None:
            self.make_stack()

        # scan the the stack looking for has-a
        # relationships (note that we can't do this until the
        # stack is complete)
        for val in self.values.values():
            if isinstance(val, Instance) and val.cls is not None:
                val.scan_bindings(val.cls)
            
        # if there is already a class diagram, clear it; otherwise
        # create one
        if self.cd:
            self.cd.clear()
        else:
            self.cd = ClassDiagram(self, classes)

        self.cd.draw()
        self.mainloop()


class Diagram(object):
    """the parent class for ClassDiagram and ObjectDiagram.
    """
    def __init__(self, lumpy):
        self.lumpy = lumpy
        self.arrows = []

        self.tl = lumpy.tl()
        self.tl.title(self.title)
        self.tl.geometry('+0+0')
        self.tl.protocol("WM_DELETE_WINDOW", self.close)
        self.setup()

    def ca(self, width=100, height=100, **options):
        """make a canvas for the diagram"""
        return self.lumpy.widget(DiagCanvas, width=width, height=height,
                                 **options)
        
    def setup(self):
        """create the gui for the diagram"""

        # push the frame for the toplevel window
        self.lumpy.pushfr(self.tl)
        self.lumpy.col([0,1])

        # the frame at the top contains buttons
        self.lumpy.row([0,0,1], bg='white')
        self.lumpy.bu(text='Close', command=self.close)
        self.lumpy.bu(text='Print to file:', command=self.printfile)
        self.en = self.lumpy.en(width=10, text='lumpy.ps')
        self.en.bind('<Return>', self.printfile)
        self.la = self.lumpy.la(width=40)
        self.lumpy.endrow()

        # the grid contains the canvas and scrollbars
        self.lumpy.gr(2)
        
        self.ca_width = 1000
        self.ca_height = 500
        self.canvas = self.ca(self.ca_width, self.ca_height, bg='white')

        yb = self.lumpy.sb(command=self.canvas.yview, sticky=N+S)
        xb = self.lumpy.sb(command=self.canvas.xview, orient=HORIZONTAL,
                         sticky=E+W)
        self.canvas.configure(xscrollcommand=xb.set, yscrollcommand=yb.set,
                              scrollregion=(0, 0, 800, 800))
        
        self.lumpy.endgr()
        self.lumpy.endcol()
        self.lumpy.popfr()

        # measure some sample letters to get the text height
        # and set the scale factor for the canvas accordingly
        self.canvas.clear_transforms()
        bbox = self.canvas.measure(['bdfhklgjpqy'])
        self.unit = 1.0 * bbox.height()
        transform = ScaleTransform([self.unit, self.unit])
        self.canvas.add_transform(transform)
        

    def printfile(self, event=None):
        """dump the contents of the canvas to the filename in the
        filename entry.
        """
        filename = self.en.get()
        bbox = self.canvas.bbox(ALL)
        width=bbox.right*self.unit
        height=bbox.bottom*self.unit
        self.canvas.config(width=width, height=height)
        self.canvas.dump(filename)
        self.canvas.config(width=self.ca_width, height=self.ca_height)
        self.la.config(text='Wrote file ' + filename)
        
    def close(self):
        """close the window and exit"""
        self.tl.withdraw()
        self.lumpy.quit()

    def add_arrow(self, arrow):
        """append a new arrow on the list"""
        self.arrows.append(arrow)

    def draw_arrows(self):
        """draw all the arrows on the list"""
        for arrow in self.arrows:
            arrow.draw(self)

    def update_arrows(self, n=None):
        """update up to n arrows (or all of them is n==None)"""
        i = 0
        for arrow in self.arrows:
            arrow.update()
            i += 1
            if n and i>n: break


class ObjectDiagram(Diagram):

    def __init__(self, lumpy=None):
        self.title = 'Object Diagram'
        Diagram.__init__(self, lumpy)

    def draw(self, thing):
        """draw the given thing"""
        thing.draw(self, Point([2,2]), flip=1)

        # configure the scroll region
        bbox = Canvas.bbox(self.canvas, ALL)
        self.canvas.configure(scrollregion=bbox)

    def clear(self):
        self.arrows = []
        self.tl.deiconify()
        self.canvas.delete(ALL)

    def update_snapshot(self, snapshot):
        pass


class ClassDiagram(Diagram):

    def __init__(self, lumpy, classes=None):
        self.title = 'Class Diagram'
        Diagram.__init__(self, lumpy)
        self.classes = classes

    def draw(self):
        """draw the class diagram, including the classes in self.classes,
        or if there are none, then all the classes Lumpy has seen."""
        pos = Point([2,2])

        if self.classes == None:
            classes = self.lumpy.get_class_list()
        else:
            classes = [make_thing(self.lumpy, cls) for cls in self.classes]

        # find the classes that have no parents, and find the
        # height of each tree
        roots = [c for c in classes if c.parents == []]
        for root in roots:
            root.set_height()

        # for all the leaf nodes, compute the distance to
        # the parent
        leafs = [c for c in classes if c.childs == []]
        for leaf in leafs:
            leaf.set_depth()

        # if we're drawing all the classes, start with the roots;
        # otherwise draw the classes we were given.
        if self.classes == None:
            drawn = self.draw_classes(roots, pos)
        else:
            drawn = self.draw_classes(classes, pos)
            
        self.draw_arrows()

        # configure the scroll region
        bbox = Canvas.bbox(self.canvas, ALL)
        self.canvas.configure(scrollregion=bbox)

        
    def draw_classes(self, classes, pos, tags=tuple()):
        """draw this list of classes and all their subclasses,
        starting at the given position.  Return a list of all
        classes drawn.
        """
        p = pos.copy()
        alldrawn = []

        for c in classes:
            drawn = c.cdc.draw(self, p, tags)
            alldrawn.extend(drawn)

            # change this so it finds the bottom-most bbox in drawn
            bbox = c.cdc.bbox()
            
            for thing in alldrawn:
                if thing is not c:
                    # can't use bbox.union because it assumes that
                    # the positive y direction is UP
                    bbox = union(bbox, thing.bbox())
            
            p.y = bbox.bottom + 2

        for c in classes:
            for d in c.refers:
                a = ContainsArrow(self.lumpy, c.cdc, d.cdc)
                self.arrows.append(a)

        return alldrawn


def union(one, other):
    """return a new bbox that covers one and other,
    assuming that the positive y direction is DOWN"""
    left = min(one.left, other.left)
    right = max(one.right, other.right)
    top = min(one.top, other.top)
    bottom = max(one.bottom, other.bottom)
    return BBox([[left, top], [right, bottom]])



###########################
# test code below this line
###########################

def main(script, *args, **kwds):
    class Cell:
        def __init__(self, car=None, cdr=None):
            self.car = car
            self.cdr = cdr

        def __hash__(self):
            return hash(self.car) ^ hash(self.cdr)

    def func_a(x):
        t = [1, 2, 3]
        t.append(t)
        y = None
        z = 1L
        long_name = 'allen'
        d = dict(a=1, b=2)

        func_b(x, y, t, long_name)

    def func_b(a, b, s, name):
        d = dict(a=1, b=(1,2,3))
        cell = Cell()
        cell.car = 1
        cell.cdr = cell
        func_c()

    def func_c():
        t = (1, 2)
        c = Cell(1, Cell())
        d = {}
        d[c] = 7
        d[7] = t
        d[t] = c.cdr
        lumpy.object_diagram()

    func_a(17)

if __name__ == '__main__':
    lumpy = Lumpy()
    lumpy.make_reference()
    main(*sys.argv)
