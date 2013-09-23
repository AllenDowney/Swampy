
FILES = \
AmoebaWorld.py       lumpy_example2.py  TurmiteWorld_test.py\
AmoebaWorld_test.py  lumpy_example3.py  turtle_code.py\
CellWorld.py         Lumpy.py           TurtleWorld.py\
CellWorld_test.py    Lumpy_test.py      TurtleWorld_test.py\
Gui.py               mutex.py           World.py\
Gui_test.py          Sync.py            World_test.py\
__init__.py          Sync_test.py\
lumpy_example1.py    TurmiteWorld.py \
danger.gif	     words.txt

VERSION = swampy-2.1
DEST = /home/downey/public_html/swampy

all:
	cd python2; make python3
	cd python2; make pydoc
	cd python3; make pydoc

setup:
	python setup.py sdist --formats=zip

zip:
	mkdir $(VERSION) 
	mkdir $(VERSION)/sync_code
	cd python2; cp $(FILES) ../$(VERSION)
	cd python2; cp sync_code/*.py ../$(VERSION)/sync_code
	zip -r $(VERSION).python2.zip $(VERSION)
	rm -rf $(VERSION)
	mkdir $(VERSION) 
	cd python3; cp -r $(FILES) ../$(VERSION)
	zip -r $(VERSION).python3.zip $(VERSION)
	rm -rf $(VERSION) 

distrib:
	cp python2/*.html $(DEST)
	cp dist/swampy-*.zip swampy-*.zip $(DEST)

DIR = swampy.1.4.doc
zipdoc:
	mkdir $(DIR) 
	cd doc; cp * ../$(DIR)
	zip -r $(VERSION).doc.zip $(DIR)
	rm -rf $(DIR) 

