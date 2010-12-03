from World import *
from filters import *

class Palindrome(Gui):
    """a Palindrome object is a kind of Gui"""

    def __init__(self):
        """the __init__ function is called when we create a Palindrome"""
        Gui.__init__(self)
        self.setup()

    def setup(self):
        """ create the widgets that make up the GUI"""

        # text entry
        self.entry = self.en()
        # label
        self.label = self.la()

        # grid with two columns
        self.gr(2, [1,1])
        # two buttons
        self.bu(text='Check', command=self.check_palindrome)
        self.bu(text='Quit', command=self.quit)
        # end of grid
        self.endgr()

    def check_palindrome(self):
        """this is the function that gets called when the user presses
        the Check button"""

        #get the contents of the text entry
        word = self.entry.get()
        # check the word
        if is_palindrome(word):
            text = 'Yes! %s is a palindrome.' % word
        else:            
            text = '%s is not a palindrome.' % word
        # change the contents of the label
        self.label.configure(text=text)

pal = Palindrome()
pal.mainloop()
