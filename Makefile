

pypi:
	rm dist/*
	python setup.py sdist
	twine upload dist/*

documentation:
	cd python3; make pydoc; mv *.html ../docs
