develop:
	python setup.py develop

install:
	python setup.py install

test:
	py.test tests/

build:
	python setup.py sdist

upload: build
	scp ./dist/dice-0.0.2.tar.gz 114:
	scp ./dist/dice-0.0.2.tar.gz ali:
