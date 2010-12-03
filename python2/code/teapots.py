# teapots.py
# by Allen Downey

# The following program demonstrates features from the
# first few chapters of the Red Book.  I have lifted
# lines from lots of different examples, with the intention
# of getting it all in one place.

# The documentation for PyOpenGL, GLU and GLUT is at:

#http://pyopengl.sourceforge.net/documentation/manual/reference-GL.xml
#http://pyopengl.sourceforge.net/documentation/manual/reference-GLU.xml
#http://pyopengl.sourceforge.net/documentation/manual/reference-GLUT.xml

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from time import sleep

revolution = 10
rotation = 10


def init():
    # clear the background
    glClearColor (1, 1, 1, 0)

    # other choice is GL_FLAT
    glShadeModel (GL_SMOOTH)

    # enable hidden surface removal
    glEnable(GL_DEPTH_TEST)

    # enable lighting
    glEnable(GL_LIGHTING)

    # put a red light on the camera
    position = [0, 0, 10, 0]
    color = [1, 0, 0, 0]
    set_up_light(GL_LIGHT0, position, color)

    # put a blue light on the right
    position = [10, 0, 0, 0]
    color = [0, 0, 1, 0]
    set_up_light(GL_LIGHT1, position, color)

    # put a green light at high noon
    position = [0, 10, 0, 0]
    color = [0, 1, 0, 0]
    set_up_light(GL_LIGHT2, position, color)


def display():
    # display runs whenever we have to redraw the screen

    # clear out the colors and the buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # for reasons I don't understand, we have to set up
    # the camera every time display runs
    set_up_camera()

    # tell GL which matrix we want to work with, and
    # set it to the identity
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # draw a sphere at the current location, size 2
    # use 32 lines of latitude and longitude
    glutSolidSphere(2, 32, 32)

    # save the current matrix before we mangle it
    glPushMatrix()

    # rotate to the right position in the orbit
    axis = (0, 1, 0)
    glRotatef(revolution, *axis)

    # move out to the orbit
    glTranslatef(7.2, 0, 0)

    # rotate the teapot
    axis = (0, 1, 0)
    glRotatef(rotation, *axis)

    # draw the teapot, size 1
    glutSolidTeapot(1)

    # restore the saved matrix
    glPopMatrix()

    # reveal the finished picture
    glutSwapBuffers()


def set_up_camera():
    # where is the camera
    camera = (0, 0, 10)

    # what is it looking at
    target = (0, 0, 0)

    # which way is up
    up = (0, 1, 0)

    # point and shoot!
    gluLookAt(*camera+target+up)


def set_up_light(name, position=[0, 0, 1, 0], color=[1, 1, 1, 1]):

    # tell GL which matrix we want, and save the current state
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # color is in RGBA format
    light_ambient =  color
    light_diffuse =  color
    light_specular = color

    # position is in x, y, z, w format
    # if w is 0 then the light is "directional"
    # otherwise it is "positional"
    # directional is like the sun, very far away
    # positional behaves like a lamp in the scene
    light_position = position

    # turn on the lights
    # read the documentation for an explanation of the
    # different kinds of light
    glLightfv(name, GL_AMBIENT, light_ambient)
    glLightfv(name, GL_DIFFUSE, light_diffuse)
    glLightfv(name, GL_SPECULAR, light_specular)
    glLightfv(name, GL_POSITION, light_position)
    glEnable(name)

    # restore the matrix before we go
    glPopMatrix()

def reshape (w, h):
    # reshape gets invoked when the window is resized

    # change the size of the viewport
    glViewport (0, 0, w, h)

    # change the way the scene is projected into
    # the viewport
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    (fovy, aspect, near, far) = (60, 1, 2, 20)
    gluPerspective(fovy, aspect, near, far)


def keyboard(key, x, y):
    # keyboard in invoked when the user presses a key

    # quit if the user presses Control-C
    if key == chr(3):
        sys.exit(0)


def mouse(button, state, x, y):
    # mouse is invoked when the user clicks the mouse
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            sys.exit()
    

def idle():
    # idle is invoked when GL isn't doing anything else
    global revolution, rotation

    # update revolution and rotation
    revolution = (revolution + 1) % 360
    rotation = (rotation + 2) % 360

    # mark the scene for redisplay during the next iteration
    # of mainLoop
    glutPostRedisplay()
    sleep(0.005)


def main(*args):
    # process command-line arguments
    glutInit(args)

    # turn on double-buffering
    # and rgb color with alpha channel
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGBA)

    # create the window
    glutInitWindowSize (500, 500)
    glutInitWindowPosition (100, 100)
    glutCreateWindow (args[0])

    # run my init function
    init ()

    # set up the callbacks
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutIdleFunc(idle)

    # loop!
    glutMainLoop()

if __name__ == "__main__":
    main(*sys.argv)
    
