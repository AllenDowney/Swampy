PYDOC = pydoc

pydoc:
	$(PYDOC) -w Gui
	$(PYDOC) -w World
	$(PYDOC) -w TurtleWorld
	$(PYDOC) -w CellWorld
	$(PYDOC) -w TurmiteWorld
	$(PYDOC) -w AmoebaWorld
	$(PYDOC) -w Sync
	$(PYDOC) -w Lumpy

FILES = \
AmoebaWorld.py       Gui_test.py        Lumpy_test.py    TurmiteWorld_test.py\
AmoebaWorld_test.py  lumpy_example1.py  mutex.py         turtle_code.py\
CellWorld.py         lumpy_example2.py  Sync.py          TurtleWorld.py\
CellWorld_test.py    lumpy_example3.py  Sync_test.py     World.py\
Gui.py               Lumpy.py           TurmiteWorld.py  World_test.py\
danger.gif           words.txt		TurtleWorld_test.py



python3:
	cp $(FILES) ../python3
	cd ../python3; 2to3 -wn Gui.py
	cd ../python3; 2to3 -wn World.py
	cd ../python3; 2to3 -wn TurtleWorld.py
	cd ../python3; 2to3 -wn CellWorld.py
	cd ../python3; 2to3 -wn TurmiteWorld.py
	cd ../python3; 2to3 -wn AmoebaWorld.py
	cd ../python3; 2to3 -wn Lumpy.py
	cd ../python3; 2to3 -wn Sync.py

	cd ../python3; 2to3 -wn Gui_test.py
	cd ../python3; 2to3 -wn World_test.py
	cd ../python3; 2to3 -wn TurtleWorld_test.py
	cd ../python3; 2to3 -wn CellWorld_test.py
	cd ../python3; 2to3 -wn TurmiteWorld_test.py
	cd ../python3; 2to3 -wn AmoebaWorld_test.py
	cd ../python3; 2to3 -wn Lumpy_test.py
	cd ../python3; 2to3 -wn Sync_test.py

clean:
	rm *~ *.pyc