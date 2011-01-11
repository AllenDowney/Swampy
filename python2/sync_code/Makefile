FILES = Gui.py Sync.py mutex.py mutex2.py barrier.py readwrite.py\
rendez.py signal.py coke.py readwrite2.py

MORE_FILES = sync.tgz rebar1.py rebar2.py rebar3.py 

DEST = /home/downey/sync/code

distrib:
	cp $(MORE_FILES) $(DEST)

tar:
	rm -rf sync
	mkdir sync
	cp $(FILES) sync
	tar -czf sync.tgz sync
	cp sync.tgz $(DEST)

