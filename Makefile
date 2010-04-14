
FILES = \
AmoebaWorld.py  Gui.py          lumpy_test3.py  readwrite.py     turtle_code.py\
CellWorld.py    Lumpy.py        lumpy_test.py   Sync.py          TurtleWorld.py\
coke.py         lumpy_test2.py  mutex.py        TurmiteWorld.py  World.py\
danger.gif	words.txt

VERSION = swampy.1.4
DEST = /home/downey/public_html

all:	zip2 zip3 zipdoc dist

dist:
	cp $(VERSION).python2.zip $(DEST)
	cp $(VERSION).python3.zip $(DEST)
	cp $(VERSION).doc.zip $(DEST)

two2three:
	cd python2; make python3

zip2:
	mkdir $(VERSION) 
	cd python2; cp $(FILES) ../$(VERSION)
	zip -r $(VERSION).python2.zip $(VERSION)
	rm -rf $(VERSION) 

zip3:
	mkdir $(VERSION) 
	cd python3; cp $(FILES) ../$(VERSION)
	zip -r $(VERSION).python3.zip $(VERSION)
	rm -rf $(VERSION) 

DIR = swampy.1.4.doc
zipdoc:
	mkdir $(DIR) 
	cd doc; cp * ../$(DIR)
	zip -r $(VERSION).doc.zip $(DIR)
	rm -rf $(DIR) 

