PYDOC = pydoc

DEST = /home/downey/public_html/greent/thinkpython

pydoc:
	$(PYDOC) -w Gui
	$(PYDOC) -w World
	$(PYDOC) -w TurtleWorld
	$(PYDOC) -w CellWorld
	$(PYDOC) -w TurmiteWorld
	$(PYDOC) -w AmoebaWorld
	$(PYDOC) -w Sync
	$(PYDOC) -w Lumpy
	rsync -a *.html $(DEST)

FILES = \
AmoebaWorld.py       Gui_test.py        Lumpy_test.py    TurmiteWorld_test.py\
AmoebaWorld_test.py  lumpy_example1.py  mutex.py         turtle_code.py\
CellWorld.py         lumpy_example2.py  Sync.py          TurtleWorld.py\
CellWorld_test.py    lumpy_example3.py  Sync_test.py     World.py\
Gui.py               Lumpy.py           TurmiteWorld.py  World_test.py\
danger.gif           words.txt		TurtleWorld_test.py

FLAGS = -wn -x import

python3:
	cp $(FILES) ../python3
	cp sync_code/*.py ../python3/sync_code
	cd ../python3; 2to3 $(FLAGS) Gui.py
	cd ../python3; 2to3 $(FLAGS) World.py
	cd ../python3; 2to3 $(FLAGS) TurtleWorld.py
	cd ../python3; 2to3 $(FLAGS) CellWorld.py
	cd ../python3; 2to3 $(FLAGS) TurmiteWorld.py
	cd ../python3; 2to3 $(FLAGS) AmoebaWorld.py
	cd ../python3; 2to3 $(FLAGS) Lumpy.py
	cd ../python3; 2to3 $(FLAGS) Sync.py

	cd ../python3; 2to3 $(FLAGS) Gui_test.py
	cd ../python3; 2to3 $(FLAGS) World_test.py
	cd ../python3; 2to3 $(FLAGS) TurtleWorld_test.py
	cd ../python3; 2to3 $(FLAGS) CellWorld_test.py
	cd ../python3; 2to3 $(FLAGS) TurmiteWorld_test.py
	cd ../python3; 2to3 $(FLAGS) AmoebaWorld_test.py
	cd ../python3; 2to3 $(FLAGS) Lumpy_test.py
	cd ../python3; 2to3 $(FLAGS) Sync_test.py

clean:
	rm *~ *.pyc