SHELL := /bin/bash

# List of targets the `readme` target should call before generating the readme
export README_TEMPLATE_FILE ?= .README.md.gotmpl

-include $(shell curl -sSL -o .build-harness "https://git.io/build-harness"; echo .build-harness)
-include $(shell curl -sSL -o $(README_TEMPLATE_FILE) "https://git.io/enter-at-readme")

project-name = lambda_handlers

version-var := "__version__ = "
version-string := $(shell grep $(version-var) $(project-name)/version.py)
version := $(subst __version__ = ,,$(version-string))

.PHONY : help
help:
	@echo "install - install"
	@echo "install-dev - install also development dependencies"
	@echo "clean-all - clean all below"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-tox - clean tox cache"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-cov - run tests with the default Python and report coverage"
	@echo "test-dbg - run tests and debug with pdb"
	@echo "develop - run tests in loop mode"
	@echo "deploy - deploy"
	@echo "mypy - check type hinting with mypy"
	@echo "isort - sort imports"
	@echo "isort-check - check if your imports are correctly sorted"
	@echo "build - create the distribution package"
	@echo "docs - build the documentation pages"
	@echo "docs-serve - build and serve locally the documentation pages"
	@echo "release - package a release in wheel and tarball, requires twine"

.PHONY : install
install:
	python -m pip install .

.PHONY : install-ci
install-ci:
	pip install -r dev-requirements.txt
	python -m pip install -e .

.PHONY : install-dev
install-dev: install-ci
	pre-commit install

.PHONY : clean-all
clean-all: clean-build clean-pyc clean-caches

.PHONY : clean-build
clean-build:
	rm -fr build/
	find . -name 'dist' -exec rm -rf {} +
	find . -name '.eggs' -exec rm -rf {} +
	find . -name '*.egg-info' -delete
	find . -name '*.spec' -delete

.PHONY : clean-pyc
clean-pyc:
	find . -name '*.py?' -delete
	find . -name '*~' -exec rm -f {} +
	find . -name __pycache__ -exec rm -rf {} +
	find . -name '*.log*' -delete
	find . -name '*_cache' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +

.PHONY : clean-caches
clean-caches:
	find . -name '.tox' -exec rm -rf {} +
	find . -name '.pytest_cache' -exec rm -rf {} +

.PHONY : lint
lint:
	tox -e lint

.PHONY : test
test:
	tox -e tests

.PHONY : mypy
mypy:
	tox -e mypy

.PHONY : isort-check
isort-check:
	tox -e isort

.PHONY : isort
isort:
	isort lambda_handlers/

.PHONY : test-cov
test-cov:
	py.test --cov-report term-missing --cov=$(project-name)

.PHONY : test-dbg
test-dbg:
	py.test --pdb

.PHONY : test-develop
develop:
	py.test --color=yes -f

.PHONY : coverage
coverage:
	pytest --cov=hansel
	coverage report -m

.PHONY : docs
docs:
	tox -e docs

.PHONY : docs-serve
docs-serve:
	tox -e docs -- serve

.PHONY : build
build:
	python setup.py sdist bdist_wheel

.PHONY : pypi
pypi:
	twine upload dist/*

.PHONY : release
release: clean build pypi
