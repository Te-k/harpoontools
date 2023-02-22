PWD = $(shell pwd)

check:
	flake8
	ruff check --ignore E501 -q .

test:
	pytest

clean:
	rm -rf $(PWD)/build $(PWD)/dist $(PWD)/harpoontools.egg-info

dist:
	python3 setup.py sdist bdist_wheel

upload:
	python3 -m twine upload dist/*
