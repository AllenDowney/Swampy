from Gui import *
import threading
import os

class MyThread(threading.Thread):
    """this is a wrapper for threading.Thread that improves
    the syntax for creating and starting threads.  See Appendix A
    of The Little Book of Semaphores, http://greenteapress.com/semaphores/
    """
    def __init__(self, target, *args):
        threading.Thread.__init__(self, target=target, args=args)
        self.start()

class Popup(Gui):
    def __init__(self, message=''):
        Gui.__init__(self)
        self.la(text=message)
        self.bu(text='Close', command=self.destroy)
        self.mainloop()
        
def main(script, message=None, *args):
    if message==None:
        message = 'default message'
    Popup(message)
    
if __name__ == '__main__':
    main(*sys.argv)
