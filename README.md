# lambda-handlers

[![](https://img.shields.io/pypi/v/lambda-handlers.svg)](https://pypi.org/project/lambda-handlers/)
[![](https://travis-ci.org/enter-at/lambda-handlers.svg?branch=master)](https://travis-ci.org/enter-at/lambda-handlers)
[![](https://api.codeclimate.com/v1/badges/a39e55b85bfcc31204b9/maintainability)](https://codeclimate.com/github/enter-at/lambda-handlers/maintainability)
[![](https://api.codeclimate.com/v1/badges/a39e55b85bfcc31204b9/test_coverage)](https://codeclimate.com/github/enter-at/lambda-handlers/test_coverage)
[![](https://readthedocs.org/projects/lambda-handlers/badge/?version=latest)](https://lambda-handlers.readthedocs.io/en/latest/)
[![](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![](https://badges.renovateapi.com/github/enter-at/lambda-handlers)](https://renovatebot.com/)

An opinionated Python package that facilitates specifying AWS Lambda handlers.

It includes input validation, error handling and response formatting.

## Documentation
Read more about the project motivation and API documentation at:

- [https://lambda-handlers.readthedocs.io/en/latest/](https://lambda-handlers.readthedocs.io/en/latest/)

## How to collaborate

This project uses [pipenv](https://pipenv.readthedocs.io) to manage its dependencies
and Python environment. You can install it by:

```bash
pip install --user pipenv
```

We recommend using a Python virtual environment for each separate project you do.
For that, we suggest using [pyenv](https://github.com/pyenv/pyenv-installer).

### Installation

For development you should also install the development dependencies,
so run instead:

```bash
cd <clone_dest>
make install-dev
```

This will install all dependencies and this project in development mode.

### Testing

We use [tox](https://tox.readthedocs.io/en/latest/) to run the code checkers.

You can run the tests by running `tox` in the top-level of the project.
