
build:
	python setup.py sdist

alpha:
	twine upload -r testpypi dist/*

publish:
	twine upload dist/*
