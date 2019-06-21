.PHONY: help clean clean-pyc clean-build list test test-dbg test-cov test-all coverage docs release sdist install deps develop tag

project-name = lambda_handlers

version-var := "__version__ = "
version-string := $(shell grep $(version-var) $(project-name)/version.py)
version := $(subst __version__ = ,,$(version-string))

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-cov - run tests with the default Python and report coverage"
	@echo "test-dbg - run tests and debug with pdb"
	@echo "testloop - run tests in a loop"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"
	@echo "install - install"
	@echo "develop - install in development mode"
	@echo "deps - install dependencies"
	@echo "dev_deps - install dependencies for development"
	@echo "release - package a release in wheel and tarball"
	@echo "upload - make a release and run the scripts/deploy.sh"
	@echo "tag - create a git tag with current version"

install:
	pip install pipenv
	pipenv install
	python setup.py install

install-dev:
	pip install pipenv
	pipenv install --dev
	python setup.py develop

clean: clean-build clean-pyc clean-tox

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr *.spec

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name __pycache__ -exec rm -rf {} +
	find . -name '*.log*' -delete
	find . -name '*_cache' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +

clean-tox:
	rm -rf .tox/

lint:
	tox -e lint

test:
	tox -e tests

mypy:
	tox -e mypy

isort-check:
	tox -e isort

isort:
	isort -rc lambda_handlers/

test:
	py.test -v

test-cov:
	py.test --cov-report term-missing --cov=$(project-name)

test-dbg:
	py.test --pdb

testloop:
	py.test -f

coverage:
	pytest --cov=hansel
	coverage report -m

build:
	python setup.py sdist bdist_wheel 

tag: clean
	@echo "Creating git tag v$(version)"
	git tag v$(version)
	git push --tags

pypi:
	twine upload dist/*

release: clean build tag pypi
