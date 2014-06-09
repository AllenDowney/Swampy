PYDOC = pydoc

DEST = /home/downey/public_html/greent/thinkpython

pydoc:
	$(PYDOC) -w AmoebaWorld
	$(PYDOC) -w CellWorld
	$(PYDOC) -w color_list
	$(PYDOC) -w Gui
	$(PYDOC) -w Lumpy
	$(PYDOC) -w structshape
	$(PYDOC) -w Sync
	$(PYDOC) -w TurmiteWorld
	$(PYDOC) -w TurtleWorld
	$(PYDOC) -w World
	rsync -a *.html $(DEST)

FILES = AmoebaWorld.py \
CellWorld.py \
color_list.py \
Gui.py \
lumpy_example1.py \
lumpy_example2.py \
lumpy_example3.py \
Lumpy.py \
mutex.py \
structshape.py \
Sync.py \
TurmiteWorld.py \
turtle_code.py \
TurtleWorld.py \
World.py \
danger.gif \
words.txt \

TESTS = AmoebaWorld_test.py \
CellWorld_test.py \
Gui_test.py \
Lumpy_test.py \
structshape_test.py \
Sync_test.py \
TurmiteWorld_test.py \
TurtleWorld_test.py \
World_test.py \

SCRIPTS = 

DOCS = AmoebaWorld.html \
CellWorld.html \
Gui.html \
Lumpy.html \
Sync.html \
TurmiteWorld.html \
TurtleWorld.html \
World.html \

FLAGS = -wn -x import

color:
	rsync color_list.py /home/downey/public_html/greent/complexity
	rsync color_list.py /home/downey/public_html/greent/thinkpython
	rsync color_list.py /home/downey/public_html/greent/thinkpython/code
	rsync color_list.py /home/downey/public_html/color

# cd ~/swampy/trunk
# edit Makefile and update versions
# make all
# make zip
# make zipdoc
# make distrib

python3:
	cp $(FILES) ../python3
	cp sync_code/*.py ../python3/sync_code
	cd ../python3; 2to3 $(FLAGS) AmoebaWorld.py
	cd ../python3; 2to3 $(FLAGS) CellWorld.py
	cd ../python3; 2to3 $(FLAGS) color_list.py
	cd ../python3; 2to3 $(FLAGS) Gui.py
	cd ../python3; 2to3 $(FLAGS) Lumpy.py
	cd ../python3; 2to3 $(FLAGS) structshape.py
	cd ../python3; 2to3 $(FLAGS) Sync.py
	cd ../python3; 2to3 $(FLAGS) TurmiteWorld.py
	cd ../python3; 2to3 $(FLAGS) TurtleWorld.py
	cd ../python3; 2to3 $(FLAGS) World.py


	cd ../python3; 2to3 $(FLAGS) AmoebaWorld_test.py
	cd ../python3; 2to3 $(FLAGS) CellWorld_test.py
	cd ../python3; 2to3 $(FLAGS) Gui_test.py
	cd ../python3; 2to3 $(FLAGS) Lumpy_test.py
	cd ../python3; 2to3 $(FLAGS) structshape_test.py
	cd ../python3; 2to3 $(FLAGS) TurmiteWorld_test.py
	cd ../python3; 2to3 $(FLAGS) TurtleWorld_test.py
	cd ../python3; 2to3 $(FLAGS) Sync_test.py
	cd ../python3; 2to3 $(FLAGS) World_test.py

# to update Swampy on PyPI
# cd ~/swampy/trunk/python2/swampy
# emacs CHANGES.txt setup.py
# update the version number below
# maybe also emacs MANIFEST
# cd ..
# make package
# make dist

# cd ~/downey/public_html/swampy
# make install.html point to new version
# cd ~/public_html; sh back
# cd ~/public_html/greent; sh back

PACKAGE = swampy
ZIP = swampy-2.1.7.zip

package:
	rsync $(FILES) $(PACKAGE)/swampy
	rsync $(TESTS) $(PACKAGE)/test
	rsync $(SCRIPTS) $(PACKAGE)/bin
	cd $(PACKAGE); zip -r $(ZIP) swampy

install:
	cd $(PACKAGE); sudo python setup.py install

dist:
	cd $(PACKAGE); rsync $(ZIP) $(DEST)
	cd $(PACKAGE); python setup.py sdist --formats gztar,zip upload
	cd /home/downey/public_html/greent; sh back

clean:
	rm *~ *.pyc
