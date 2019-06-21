.PHONY: help Makefile README.md

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
