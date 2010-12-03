# Turtle3D.py
# by Allen Downey

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Numeric import *
import sys
from time import sleep

def get_frame():
    # get the model-view matrix
    return glGetFloat(GL_MODELVIEW_MATRIX)

def whereami():
    frame = get_frame()
    return frame[3][:-1]

def print_frame(frame=None):
    frame = frame or get_frame()
    print transpose(array(frame))


class World:
    def __init__(self, args, size=(500, 500), pos=(100, 100), bg=(1, 1, 1, 0)):
        self.args = args
        self.size = size
        self.pos = pos
        self.bg = bg
        self.delay = 0.001
        
        self.opaques = []
        self.transparents = []
        self.fog = Fog()

        self.set_up_gl()
        World.identity = get_frame()
        self.camera = None
        self.lights = []
        self.add_lights()

    def add_opaque(self, object):
        self.opaques.append(object)

    add = add_opaque

    def add_transparent(self, object):
        self.transparents.append(object)

    def set_up_gl(self):
        # process command-line arguments
        glutInit(self.args)

        # turn on double-buffering and rgb color
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)

        # create the window
        glutInitWindowSize(*self.size)
        glutInitWindowPosition(*self.pos)
        glutCreateWindow(self.args[0])

        # clear the background
        glClearColor(*self.bg)

        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
#        glLightModel(GL_LIGHT_MODEL_LOCAL_VIEWER, 1)
#        glLightModel(GL_LIGHT_MODEL_TWO_SIDE, 1)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # set up the callbacks
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.keyboard)
        glutMouseFunc(self.mouse)
        glutIdleFunc(self.idle)

    def add_lights(self):
        # put a red light on the front
        position = (0, 0, 10, 0)
        color = (1, 0, 0, 0)
        light = Light(GL_LIGHT0, position, color)
        self.lights.append(light)

        # put a blue light on the right
        position = (10, 0, 0, 0)
        color = (0, 0, 1, 0)
        light = Light(GL_LIGHT1, position, color)
        self.lights.append(light)

        # put a green light at high noon
        position = (0, 10, 0, 0)
        color = (0, 1, 0, 0)
        light = Light(GL_LIGHT2, position, color)
        self.lights.append(light)

    def display(self):
        # precondition: matrix mode is modelview
        # invariant: restores the current matrix

        glMaterial(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 0.15))
        glMaterial(GL_FRONT, GL_SHININESS, (100.0, ))
        
        # clear out the colors and the buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # you have to draw the fog every time
        if hasattr(self, 'fog'):
            self.fog.setup()

        # display all the objects
        glMaterial(GL_FRONT, GL_EMISSION, ( 0.0, 0.0, 0.0, 1.0))
        glMaterial(GL_FRONT, GL_DIFFUSE, (0.75, 0.75, 0.0, 1.0))

        self.camera.point()

        for object in self.opaques:
                object.display()

        glMaterial(GL_FRONT, GL_EMISSION, ( 0.0, 0.3, 0.3, 0.6))
        glMaterial(GL_FRONT, GL_DIFFUSE, ( 0.0, 0.8, 0.8, 0.8))
        glDepthMask(GL_FALSE)

        for object in self.transparents:
            object.display()

        glDepthMask(GL_TRUE)
        glutSwapBuffers()

    def reshape (self, w, h):
        glViewport (0, 0, w, h)

    def keyboard(self, key, x, y):
        # quit if the user presses Control-C
        if key == chr(3):
            sys.exit(0)

    def mouse(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                glutIdleFunc(None)
            elif state == GLUT_UP:
                glutIdleFunc(self.idle)
    
    def idle(self):
        for object in self.opaques:
            object.step()

        for object in self.transparents:
            object.step()

        # mark the scene for redisplay during the next iteration
        # of mainLoop
        glutPostRedisplay()
        sleep(self.delay)

    def mainloop(self):
        glutMainLoop()


class Thing:
    X = (1, 0, 0)
    Y = (0, 1, 0)
    Z = (0, 0, 1)
    
    def __init__(self, parent, *args, **kwds):
        self.parent = parent
        self.frame = World.identity
        self.args = args
        self.kwds = kwds
        self.objects = []
        self.parent.add(self)

    def position(self):
        return self.frame[3]

    def begin(self, type, vertices):
        self.ribbon = Ribbon(self.parent, type, vertices)

    def fan(self, vertices=None):
        self.begin(GL_TRIANGLE_FAN, vertices)
    
    def strip(self, vertices=None):
        self.begin(GL_TRIANGLE_STRIP, vertices)

    def vertex(self):
        pos = self.position()        
        self.ribbon.append(pos)

    def end(self):
        self.ribbon = None

    # turtle motion primitives:
    
    def load(self):
        glPushMatrix()
        glLoadMatrixf(self.frame)
        # postcondition: turtle state is loaded

    def unload(self):
        # precondition: turtle state is loaded
        self.frame = get_frame()
        glPopMatrix()
        
    def translate(self, x=0, y=0, z=0):
        # precondition: turtle state is loaded
        glTranslate(x, y, z)

    def rotate(self, angle, axis):
        # precondition: turtle state is loaded
        glRotate(angle, *axis)        

    def scale(self, x=1, y=1, z=1):
        # precondition: turtle state is loaded
        glScale(x, y, z)

    # turtle motion methods:
    # these methods load the turtle frame, modify it, and unload it
    # they leave GL state unchanged (provided that there is room
    # on the stack)
    
    def fd(self, z=0):
        self.load()
        self.translate(0, 0, z)
        self.unload()

    def bk(self, z=0): self.fd(-z)

    def left(self, x=0):
        self.load()
        self.translate(x, 0, 0)
        self.unload()

    def right(self, x=0): self.left(-x)

    def up(self, y=0):
        self.load()
        self.translate(0, y, 0)
        self.unload()

    def down(self, y=0): self.up(-y)

    def yaw(self, angle):
        self.load()
        self.rotate(angle, self.Y)
        self.unload()

    def pitch(self, angle):
        self.load()
        self.rotate(angle, self.X)
        self.unload()

    def roll(self, angle):
        self.load()
        self.rotate(angle, self.Z)
        self.unload()

    def zig(self, x=0, y=0, z=0):
        self.load()
        self.translate(x, y, z)
        self.unload()

    def zag(self, x=0, y=0, z=0):
        self.load()
        self.translate(-x, -y, -z)
        self.unload()

    def zigzag(self, x=0, y=0, z=0):
        self.zig(x, y, z)
        self.vertex()
        self.zag(x, y, z)

    def grow(self, x=1, y=1, z=1):
        self.load()
        self.scale(x, y, z)
        self.unload()

    def shrink(self, x=1, y=1, z=1):
        self.grow(1.0/x, 1.0/y, 1.0/z)        

    def add(self, obj):
        self.objects.append(obj)

    def clear(self):
        self.objects = []

    def step(self): pass

    def draw(self): pass

    def display(self):
        glPushMatrix()

        glMultMatrixf(self.frame)

        self.display_self()

        for obj in self.objects:
            obj.display()
        
        glPopMatrix()

    def display_self(self):
        glRotate(-90, *self.Y)
        teapot(*self.args, **self.kwds)


class Camera(Thing):
    def __init__(self, world,
                 fovy=60, aspect=1, near=1, far=20,
                 *args, **kwds):
        Thing.__init__(self, world, *args, **kwds)
        self.fovy = fovy
        self.aspect = aspect
        self.near = near
        self.far = far

    def point(self, target=None):
        # set up the projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fovy, self.aspect, self.near, self.far)

        # set up the modelview matrix
        glMatrixMode(GL_MODELVIEW)

        # compute the camera position, target, and up vector
        # by loading the turtle's frame temporarily
        glLoadMatrixf(self.frame)
        position = whereami()

        if target == None:
            glTranslate(0, 0, 1)
            target = whereami()

        glTranslate(0, 10, 0)
        up = whereami()

        # use gluLookAt to load the model-view matrix
        glLoadIdentity()
        gluLookAt(*position + target + up)

    def display_self(self): pass


class Ribbon(Thing):
    def __init__(self, parent, type=GL_TRIANGLE_STRIP, vertices=None):
        Thing.__init__(self, parent)
        self.type = type
        self.vertices = vertices or []

    def append(self, obj): self.vertices.append(obj)

    def display(self):
        glBegin(self.type)
        for vertex in self.vertices:
            normal = vertex[0:3]
            glNormal(normal)
            glVertex(vertex)
        glEnd()

    def printv(self):
        for v in self.vertices:
            print '[%.3f %.3f %.3f]' % (v[0], v[1], v[2])

    def step(self): pass


class Turtle(Camera):
    def __init__(self, parent, size=1):
        Camera.__init__(self, parent)
        self.size = size
        self.counter = 0
        self.draw()

    def step(self):
        self.counter += 1
        if self.counter % 200 == 50: self.hide()
        if self.counter % 200 == 100: self.unhide()
        
        self.fd(0.2)
        self.yaw(2.5)
        self.pitch(-1)

        self.zigzag(y=0.2)
        self.zigzag(y=-0.2)

        self.redraw()

    def redraw(self): pass

    def draw(self):
        self.strip()
        x = self.size
        
        self.head = Sphere(self, 0.4*x)
        self.head.fd(1.0*x)
        self.head.up(0.1*x)

        self.tail = Cone(self, 0.4*x, 1.0*x)
        self.tail.yaw(180)
        self.tail.pitch(5)
        self.tail.fd(0.1*x)
        
        self.legs = []
        leg_len = 0.8*x
        for yaw in [45, -45, 135, -135]:
                leg = Cone(self, 0.15*x, leg_len)
                leg.yaw(yaw)
                leg.pitch(10)
                leg.fd(leg_len)
                leg.yaw(180)
                self.legs.append(leg)

        self.body = Sphere(self, 0.8*x)

        parts = [self.head, self.tail, self.body]
        scale = (0.7, 0.4, 1)
        for part in parts:
            part.grow(*scale)


    def hide(self, m=1):
        d = 0.6 * m
        self.head.bk(d)
        for leg in self.legs:
            leg.fd(d)

    def unhide(self): self.hide(-1)

    def display_self(self): pass

    def point(self):
        self.bk(2.5)
        self.yaw(10)
        Camera.point(self)
        self.yaw(-10)
        self.fd(2.5)

def cone(base=1, height=1, slices=32, stacks=32):
    glutSolidCone(base, height, slices, stacks)
def torus(inner=1, outer=2, nsides=32, rings=32):
    glutSolidTorus(inner, outer, nsides, rings)
def sphere(radius=1, slices=32, stacks=32):
    glutSolidSphere(radius, slices, stacks)
def teapot(size=1): glutSolidTeapot(size)
def cube(size=1): glutSolidCube(size)
def dodecahedron(): glutSolidDodecahedron()
def icosahedron(): glutSolidIcosahedron()
def octahedron(): glutSolidOctahedron()
def tetrahedron(): glutSolidTetrahedron()

class Cone(Thing):
    def display_self(self):
        cone(*self.args, **self.kwds)

class Torus(Thing):
    def display_self(self):
        torus(*self.args, **self.kwds)

class Sphere(Thing):
    def display_self(self):
        sphere(*self.args, **self.kwds)

class Cube(Thing):
    def display_self(self):
        cube(*self.args, **self.kwds)

class Teapot(Thing):
    def display_self(self):
        teapot(*self.args, **self.kwds)

class Tetrahedron(Thing):
    def display_self(self):
        tetrahedron(*self.args, **self.kwds)

class Octahedron(Thing):
    def display_self(self):
        octahedron(*self.args, **self.kwds)

class Dodecahedron(Thing):
    def display_self(self):
        dodecahedron(*self.args, **self.kwds)

class Icosahedron(Thing):
    def display_self(self):
        icosahedron(*self.args, **self.kwds)

class Fog:
    def __init__(self, color=(1, 1, 1, 1), mode=GL_LINEAR,
                 density=0.1, hint=GL_DONT_CARE, start=2, end=20):
        self.color = color
        self.mode = mode
        self.density = density
        self.hint = hint
        self.start = start
        self.end = end
        self.setup()

    def setup(self):
        glEnable(GL_FOG)
        glFog(GL_FOG_MODE, self.mode)
        glFog(GL_FOG_COLOR, self.color)
        glFog(GL_FOG_DENSITY, self.density)
        glFog(GL_FOG_START, self.start)
        glFog(GL_FOG_END, self.end)       
        glHint(GL_FOG_HINT, self.hint)

class Light:
    def __init__(self, name, position=(0, 0, 1, 0), color=(1, 1, 1, 1)):
        self.name = name
        self.position = position
        self.acolor = color
        self.dcolor = color
        self.scolor = color
        self.setup()

    def setup(self):
        glLightfv(self.name, GL_AMBIENT, self.acolor)
        glLightfv(self.name, GL_DIFFUSE, self.dcolor)
        glLightfv(self.name, GL_SPECULAR, self.scolor)
        glLightfv(self.name, GL_POSITION, self.position)
        glEnable(self.name)

def main(*args):
    world = World(args)

    camera1 = Camera(world, size=0.1)
    camera1.fd(10)
    camera1.yaw(180)

    camera2 = Camera(world, size=0.1)
    camera2.up(10)
    camera2.pitch(90)

    world.camera = camera2

    for angle in [0, 90, 180, 270]:
        thing = Turtle(world, 1)
        thing.yaw(angle)
        thing.pitch(90)
        thing.right(3)

    world.camera = thing
    world.mainloop()

if __name__ == "__main__":
    main(*sys.argv)
