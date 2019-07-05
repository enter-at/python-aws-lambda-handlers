# lambda-handlers

[![](https://img.shields.io/pypi/v/lambda-handlers.svg)](https://pypi.org/project/lambda-handlers/)
[![](https://travis-ci.org/enter-at/lambda-handlers.svg?branch=master)](https://travis-ci.org/enter-at/lambda-handlers)
[![](https://api.codeclimate.com/v1/badges/a39e55b85bfcc31204b9/maintainability)](https://codeclimate.com/github/enter-at/lambda-handlers/maintainability)
[![](https://api.codeclimate.com/v1/badges/a39e55b85bfcc31204b9/test_coverage)](https://codeclimate.com/github/enter-at/lambda-handlers/test_coverage)
[![](https://requires.io/github/enter-at/lambda-handlers/requirements.svg?branch=master)](https://requires.io/github/enter-at/lambda-handlers/requirements/?branch=master)
[![](https://readthedocs.org/projects/lambda-handlers/badge/?version=latest)](https://lambda-handlers.readthedocs.io/en/latest/)
[![](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)


An opinionated Python package that facilitates specifying AWS Lambda handlers.

It includes input validation, error handling and response formatting.


## Getting started

To use `lambda-handlers` you must first install it:

```bash
pip install lambda-handlers
```

If you are going to use validation, you should choose between
[Marshmallow](https://pypi.org/project/marshmallow/) or
[jsonschema](https://pypi.org/project/jsonschema/).

To install with one of these:

```bash
pip install 'lambda-handlers[marshmallow]'
```

or

```bash
pip install 'lambda-handlers[jsonschema]'
```

### Quickstart

By default the `http_handler` decorator makes sure of parsing the request body
as JSON, and also formats the response as JSON with:
   - an adequate statusCode,
   - CORS headers, and
   - the handler return value in the body.

```python
from lambda_handler import http_handler

@http_handler()
def handler(event, context):
    return event['body']
```


### Examples

Skipping the CORS headers default and configuring it.

```python
from lambda_handler import http_handler
from lambda_handlers.response import cors

@http_handler(
    cors=cors(origin='localhost', credentials=False),
)
def handler(event, context):
    return event['body']
```


Using jsonschema to validate a the input of a User model.

```python
from typing import Dict, Any

from lambda_handler import validators, http_handler

user_schema: Dict[str, Any] = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'number'},
    },
}


@http_handler(
    validation=validators.jsonschema(body=user_schema),
)
def handler(event, context):
    user = event['body']
    return user
```


Using Marshmallow to validate a User model in the input and in
the response body.

```python
from lambda_handler import validators, http_handler
from marshmallow import Schema, fields


class UserSchema(Schema):
    user_id = fields.Integer(required=True)


class ResponseSchema(Schema):
    body = fields.Nested(UserSchema, required=True)
    headers = fields.Dict(required=True)
    statusCode = fields.Integer(required=True)


@http_handler(
    validation=validators.marshmallow(
        body=UserSchema(),
        response=ResponseSchema(),
    ),
)
def handler(event, context):
    user = event['body']
    return user
```


## Development

This project uses [pipenv](https://pipenv.readthedocs.io) to manage its dependencies
and Python environment. You can install it by:

```bash
pip install --user pipenv
```

We recommend using a Python virtual environment for each separate project you do.
For that, we suggest using [pyenv](https://github.com/pyenv/pyenv-installer).

### Installation

For production, after you clone this repository,
you can install this project plus dependencies with:

```bash
cd <clone_dest>
make install
```

### Development

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

