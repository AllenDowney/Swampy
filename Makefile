

VERSION = swampy-2.1.5
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

DIR = swampy.2.1.5.doc
zipdoc:
	mkdir $(DIR) 
	cd doc; cp * ../$(DIR)
	zip -r $(VERSION).doc.zip $(DIR)
	rm -rf $(DIR) 

