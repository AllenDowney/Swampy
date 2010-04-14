#!/usr/bin/python

"""
  Copyright 2005 Allen B. Downey

    This file contains a simulator I wrote to demonstrate
    synchronized, multithreaded programs in Python.  It goes
    along with The Little Book of Semaphores.  It is
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
    along with this program; if not, see http://www.gnu.org/licenses/gpl.html
    or write to the Free Software Foundation, Inc., 51 Franklin St, 
    Fifth Floor, Boston, MA  02110-1301  USA
"""

from Gui import *
from random import *
from time import sleep

import sys
import copy
import string

# get the version of Python
v = sys.version.split()[0].split('.')
major = int(v[0])

if major == 2:
    all_thread_names = string.uppercase + string.lowercase
else:
    all_thread_names = string.ascii_uppercase + string.ascii_lowercase


font = ("Courier", 12)
FSU = 10                    # FSU, the fundamental Sync unit,
                            # determines the size of most things.

class Semaphore:
    """this is the semaphore class used by threads running in
    the simulator.  It maintains a FIFO queue.
    """
    def __init__(self, n=0):
        self.n = n
        self.queue = []

    def __str__(self): return str(self.n)

    def wait(self):
        self.n -= 1
        if self.n < 0:
            self.block()
        return self.n

    def block(self):
        thread = current_thread
        thread.enqueue()
        self.queue.append(thread)

    def signal(self, n=1):
        for i in range(n):
            self.n += 1
            if self.queue:
                self.unblock()

    def unblock(self):
        thread = self.queue.pop(0)
        thread.dequeue()
        thread.next_loop()


class RandomSemaphore(Semaphore):
    """this is a variant of Semaphore that implements a random queue.
    """
    def unblock(self):
        thread = choice(self.queue)
        self.queue.remove(thread)
        thread.dequeue()
        thread.next_loop()

class Lightswitch:
    def __init__(self):
        self.counter = 0
        self.mutex = Semaphore(1)

    def lock(self, semaphore):
        self.mutex.wait()
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.signal()

    def unlock(self, semaphore):
        self.mutex.wait()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.signal()

def pid():
    return current_thread.name

def num_threads():
    sync = current_thread.column.p
    return len(sync.threads)

current_thread = None


# Anything above this line can be accessed from code running
# in the simulator.
sim_globals = globals()
sim_locals = locals()


class Sync(Gui):
    def __init__(self, filename=None):
        Gui.__init__(self)
        #self.geometry('1260x800+74+32')
        self.filename = filename
        self.views = {}
        self.w = self
        self.threads = []
        self.running = 0
        self.delay = 0.2
        self.setup()
        self.run_init()
        for col in self.cols:
            col.create_thread()

    def destroy(self):
        self.running = 0
        Gui.destroy(self)

    def setup(self):
        if self.filename:
            self.read_file(self.filename)
            return

        self.topcol = Column(self, n=5)
        self.colfr = self.fr()
        self.cols = [Column(self, LEFT, n=5) for i in range(2)]
        self.bu(RIGHT, text='Add\ncolumn', command=self.add_col)
        self.endfr()
        self.buttons()

    def buttons(self):
        self.row([1,1,1,1,1])
        self.bu(text='Run', command=self.run)
        self.bu(text='Random Run', command=self.random_run)
        self.bu(text='Stop', command=self.stop)
        self.bu(text='Step', command=self.step)
        self.bu(text='Random Step', command=self.random_step)
        self.endfr()

    # the Sync object keeps a list of threads, so new threads
    # have to register themselves
    def register(self, thread):
        self.threads.append(thread)

    def unregister(self, thread):
        self.threads.remove(thread)

    # run and random_run both invoke run_helper, passing either
    # step or random_step as a parameter.

    def run(self):
        self.run_helper(self.step)

    def step(self):
        for thread in self.threads:            
            thread.step_loop()

    def random_run(self):
        self.run_helper(self.random_step)
        
    def random_step(self):
        threads = [thread for thread in self.threads if not thread.queued]
        if not threads:
            print 'There are currently no threads that can run.'
            return
        thread = choice(threads)
        thread.step_loop()

    def run_helper(self, step=None):
        self.running = 1
        while self.running:
            step()
            self.update()
            sleep(self.delay)

    def stop(self):
        self.running = 0

    def read_file(self, filename):
        """read a file that contains code for the simulator
        to execute.  Lines that start with ## do not appear
        in the display.  A line that starts with ## and
        contains the word thread indicates the beginning of
        a new column of code.
        """
        col = self.topcol = TopColumn(self)
        self.colfr = self.fr()
        self.cols = []
        self.endfr()
        
        fp = open(filename)
        for line in fp:
            line = line.rstrip()
            if line == '': continue
            if line[0:2] == '##':
                words = line.strip('#').split()
                if words[0].lower() == 'thread':
                    col = self.add_col(0)
                continue
            col.add_row(line)
        fp.close()
        self.buttons()
            
    def add_col(self, n=5):
        "add a new column of code to the display"
        self.pushfr(self.colfr)
        col = Column(self, LEFT, n)
        self.cols.append(col)
        self.popfr()
        return col

    def run_init(self):
        "run the initialization code in the top column"
        self.clear_views()
        self.views = {}

        self.locals = copy.copy(sim_locals)
        self.globals = copy.copy(sim_globals)
        
        thread = Thread(self.topcol, name='0')
        while 1:
            thread.step()
            if thread.row == None: break

        self.unregister(thread)
        self.update_views()

    def update_views(self):
        for key in self.views:
            view = self.views[key]
            view.update(self.locals[key])

    def clear_views(self):
        for key in self.views:
            view = self.views[key]
            view.clear()

    def qu(self, **options):
        return self.widget(QueueCanvas, **options)


# dictionary functions
def subtract(d1, d2):
    """ return a new dictionary containing all the keys from
    d1 that are not in d2
    """
    d = {}
    for key in d1:
        if key not in d2:
            d[key] = d1[key]
    return d

def diff(d1, d2):
    """return two dictionaries: the first contains all the keys
    from d1 that are not in d2; the second contains all the keys
    that are in both dictionaries, but which have different values.
    """
    d = {}
    c = {}
    for key in d1:
        if key not in d2:
            d[key] = d1[key]
        elif d1[key] is not d2[key]:
            c[key] = d1[key]
    return d, c

# the following classes define the composite objects that make
# up the display: Row, TopRow, Column and TopColumn.  They are
# all subclasses of Thing.

# Each Thing keeps a reference to its immediate parent Thing (p)
# and to the top-most thing (w).
        
class Thing:
    def __init__(self, p, *args, **options):
        self.p = p
        self.w = p.w
        self.setup(*args, **options)


class Row(Thing):
    """each row contains two queues, runnable and queued,
    and an entry that contains a line of code.
    """
    def setup(self, text=''):
        self.tag = None
        self.fr = self.w.row([0,0,1])
        self.queued = self.w.qu(side=LEFT, n=3)
        self.runnable = self.w.qu(side=LEFT, n=3, label='Run')
        self.en = self.w.en(side=LEFT, font=font)
        self.en.bind('<Key>', self.keystroke)
        self.w.endrow()
        self.put(text)

    def update(self, val):
        if self.tag: self.clear()
        text = str(val)
        self.tag = self.runnable.display_text(text)

    def clear(self):
        self.runnable.delete(self.tag)

    def keystroke(self, event=None):
        "resize the entry whenever the user types a character"
        self.entry_size()
        
    def entry_size(self):
        "resize the entry"
        text = self.get()
        width = self.en.cget('width')
        l = len(text) + 2
        if l > width:
            self.en.configure(width=l)

    def add_thread(self, thread):
        self.runnable.add_thread(thread)

    def remove_thread(self, thread):
        self.runnable.remove_thread(thread)

    def enqueue_thread(self, thread):
        self.queued.add_thread(thread)

    def dequeue_thread(self, thread):
        self.queued.remove_thread(thread)

    def put(self, text):
        self.en.delete(0, END)
        self.en.insert(0, text)
        self.entry_size()

    def get(self):
        return self.en.get()


class TopRow(Row):
    """the top row is special because there is no queue for
    queued threads, and the "runnable" queue is actually used
    to display the value of variables.
    """
    def setup(self, text=''):
        Row.setup(self, text)
        self.queued.destroy()
        self.runnable.delete('all')


class Column(Thing):
    """a column is a list of rows and a few buttons
    """
    def setup(self, side=TOP, n=0, Row=Row):
        self.fr = self.w.fr(side=side, bd=3)
        self.Row = Row
        self.rows = [self.Row(self) for i in range(n)]

        self.buttons = self.w.row([1,1], side=BOTTOM)
        self.bu1 = self.w.bu(text='Create thread',
                                 command=self.create_thread)
        self.bu2 = self.w.bu(text='Add row',
                             command=self.add_row)
        self.w.endrow()
        self.w.endfr()

    def add_row(self, text=''):
        self.w.pushfr(self.fr)
        row = self.Row(self, text)
        self.w.popfr()
        self.rows.append(row)

    def create_thread(self):
        new = Thread(self)
        return new

    # iterating through a Column is the same as iterating
    # through its list of rows.
    def __iter__(self): return self.rows.__iter__()


class TopColumn(Column):
    """a top column is different from the other columns in
    two ways: it has different buttons, and it uses the TopRow
    constructor to make new rows rather than the Row constructor.
    """
    def setup(self, side=TOP, n=0, Row=TopRow):
        Column.setup(self, side, n, Row)
        self.bu1.configure(text='Run initialization',
                                 command=self.p.run_init)

class QueueCanvas(GuiCanvas):
    """a subclass of GuiCanvas used to display the
    runnable and queued threads.
    """
    def __init__(self, w, n=1, label='Queue'):
        self.n = n
        self.label = label
        width = 2 * n * FSU
        height = 3 * FSU
        GuiCanvas.__init__(self, w, width=width, height=height,
                           transforms=[])
        self.threads = []
        self.setup()
        
    def setup(self):
        self.text([3, 15], self.label, font=font, anchor=W, fill='gray80')
        
    def add_thread(self, thread):
        self.undraw_queue()
        self.threads.append(thread)
        self.draw_queue()

    def remove_thread(self, thread):
        self.undraw_queue()
        self.threads.remove(thread)
        self.draw_queue()

    def draw_queue(self):
        x = FSU
        y = FSU
        r = 0.9 * FSU
        for thread in self.threads:
            self.draw_thread(thread, x, y, r)
            x += 1.5*r
            if x > self.get_width():
                x = FSU
                y += 1.5*r
        
    def undraw_queue(self):
        for thread in self.threads:
            self.delete(thread.tag)

    def draw_thread(self, thread, x=FSU, y=FSU, r=0.9*FSU):
        thread.tag = 'Thread' + thread.name
        self.circle([x, y], r, fill=thread.color, tags=thread.tag)
        font=('Courier', int(r+3))
        self.text([x, y], thread.name, font=font, tags=thread.tag)
        self.tag_bind(thread.tag, '<Button-1>', thread.step_loop)

    def undraw_thread(self, thread):
        self.delete(thread.tag)

    def display_text(self, text):
        tag = self.text([15, 15], text, font=font)
        return tag


class Thread:
    """this class represents simulated threads.
    """
    names = all_thread_names
    next_name = 0
    colors = ['red', 'orange', 'yellow', 'greenyellow',
              'green', 'mediumseagreen', 'skyblue',
              'violet', 'magenta']
    next_color = 0

    def __init__(self, column, name=None):
        self.column = column
        if name == None:
            self.name = Thread.names[Thread.next_name]
            Thread.next_name += 1
            Thread.next_name %= len(Thread.names)

            self.color = Thread.colors[Thread.next_color]
            Thread.next_color += 1
            Thread.next_color %= len(Thread.colors)
        else:
            self.name = name
            self.color = 'white'

        sync = self.column.p
        sync.register(self)
        self.start()

    def __str__(self):
        return '<' + self.name + '>'

    def enqueue(self):
        self.queued = True
        self.row.remove_thread(self)
        self.row.enqueue_thread(self)

    def dequeue(self):
        self.queued = False
        self.row.dequeue_thread(self)
        self.row.add_thread(self)

    def start(self):
        self.queued = False
        self.iter = self.column.__iter__()
        self.row = None
        self.next_loop()

    def next_row(self):
        "move this thread to the next row in the column"
        if self.queued: return
        if self.row:
            self.row.remove_thread(self)
        try:
            self.row = self.iter.next()
            self.row.add_thread(self)
        except StopIteration:
            self.row = None

    def next_loop(self):
        "move to the next row, looping to the top if necessary"
        self.next_row()
        if self.row == None: self.start()

    def step(self, event=None):
        """execute the current line of code, then move to the next row.
        The current limitation of this simulator is that each row
        has to contain a complete Python statement.  Also, each line
        of code is executed atomically.
        """
        if self.queued: return
        source = self.row.get()
        source = source.strip()
        print self, source

        code = compile(source, '<user-provided code>', 'exec')

        # debugging code for catching certain exceptions
        # try:
        # except:
        #     (type, value, traceback) = sys.exc_info()
        #     print traceback
        #     print type, value
        #     self.next()
        #     return

        global current_thread        
        current_thread = self

        sync = self.column.p
        before = copy.copy(sync.locals)
        exec code in sync.globals, sync.locals

        defined, changed = diff(sync.locals, before)
        for key in defined:
            sync.views[key] = self.row

        sync.update_views()
        self.next_row()

    def step_loop(self, event=None):
        self.step()
        if self.row == None: self.start()
        
    def run(self):
        while 1:
            self.step()
            if self.row == None: break


def main(script, filename='sync_code.py', *args):
    sync = Sync(filename)
    sync.mainloop()
 
# if we are running the program as a script (as opposed to
# importing it, we should call main(), passing along
# the command-line arguments
if __name__ == '__main__':
    main(*sys.argv)
