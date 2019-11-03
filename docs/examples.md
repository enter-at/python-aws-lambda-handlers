# Examples

## HTTP handlers

Skipping the CORS headers default and configuring it.

```python
from lambda_handlers import http_handler
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

from lambda_handlers import validators, http_handler

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
from lambda_handlers import validators
from lambda_handlers.handlers import http_handler
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

## Event handlers

Using event_handler to validate input with Marshmallow.

```python
from lambda_handlers import validators
from lambda_handlers.handlers import event_handler
from marshmallow import Schema, fields


class UserSchema(Schema):
    user_id = fields.Integer(required=True)


@event_handler(
    validator=validators.marshmallow(
        body=UserSchema(),
        response=ResponseSchema(),
    ),
)
def handler(event, context):
    user = event['body']
    return user
```