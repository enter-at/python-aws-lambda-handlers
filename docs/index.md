# lambda-handlers
An opinionated Python package that facilitates specifying AWS Lambda handlers.

It includes input validation, error handling and response formatting.

## Contents

* [Validators](validators.md)
* [API Reference](source/modules)

## Getting started

Install `lambda-handlers` with:

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
    validator=validators.jsonschema(body=user_schema),
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
    validator=validators.marshmallow(
        body=UserSchema(),
        response=ResponseSchema(),
    ),
)
def handler(event, context):
    user = event['body']
    return user
```