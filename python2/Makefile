pydoc:
	pydoc -w Gui
	pydoc -w World
	pydoc -w TurtleWorld
	pydoc -w CellWorld
	pydoc -w TurmiteWorld
	pydoc -w AmoebaWorld

FILES = \
AmoebaWorld.py  Gui.py          lumpy_test3.py  readwrite.py     turtle_code.py\
CellWorld.py    Lumpy.py        lumpy_test.py   Sync.py          TurtleWorld.py\
coke.py         lumpy_test2.py  mutex.py        TurmiteWorld.py  World.py\
danger.gif	words.txt


python3:
	cp $(FILES) ../python3
	cd ../python3; 2to3 -wn Gui.py
	cd ../python3; 2to3 -wn World.py
	cd ../python3; 2to3 -wn TurtleWorld.py
	cd ../python3; 2to3 -wn CellWorld.py
	cd ../python3; 2to3 -wn TurmiteWorld.py
	cd ../python3; 2to3 -wn AmoebaWorld.py
	cd ../python3; 2to3 -wn Lumpy.py
	cd ../python3; 2to3 -wn -x next Sync.py

clean:
	rm *~ *.pyc