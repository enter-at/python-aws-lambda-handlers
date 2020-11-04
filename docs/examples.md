# Examples

## HTTP handlers

Skipping the CORS headers default and configuring it.

```python
from lambda_handlers.handlers import http_handler
from lambda_handlers.response import cors

@http_handler(cors=cors(origin='localhost', credentials=False))
def handler(event, context):
    return {
        'message': 'Hello World!'
    }
```

```bash
aws lambda invoke --function-name example response.json
cat response.json
```

```json
{
    "headers":{
        "Access-Control-Allow-Origin": "localhost",
        "Content-Type": "application/json"
    },
    "statusCode": 200,
    "body": "{\"message\": \"Hello World!\"}"
}
```

## Validation

Using jsonschema to validate a User model as input.

```python
from typing import Any, Dict, List, Tuple, Union

import jsonschema

from lambda_handlers.handlers import http_handler
from lambda_handlers.errors import EventValidationError

class SchemaValidator:
    """A payload validator that uses jsonschema schemas."""

    @classmethod
    def validate(cls, instance, schema: Dict[str, Any]):
        """
        Raise EventValidationError (if any error) from validating 
        `instance` against `schema`.
        """
        validator = jsonschema.Draft7Validator(schema)
        errors = list(validator.iter_errors(instance))
        if errors:
            field_errors = sorted(validator.iter_errors(instance), key=lambda error: error.path)
            raise EventValidationError(field_errors)

    @staticmethod
    def format_errors(errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Re-format the errors from JSONSchema."""
        path_errors: Dict[str, List[str]] = defaultdict(list)
        for error in errors:
            path_errors[error.path.pop()].append(error.message)
        return [{path: messages} for path, messages in path_errors.items()]

user_schema: Dict[str, Any] = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'number'},
    },
}

@http_handler()
def handler(event, context):
    user = event['body']
    SchemaValidator.validate(user, user_schema)
    return user
```

```bash
aws lambda invoke --function-name example --payload '{"body": {"user_id": 42}}' response.json
cat response.json
```

```json
{
    "headers":{
        "Access-Control-Allow-Credentials": true,
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    },
    "statusCode": 200,
    "body": "{\"user_id\": 42}"
}
```

Using Marshmallow to validate a User model as input body and response body.

```python
from typing import Any, Dict, List, Tuple, Union

from marshmallow import Schema, fields, ValidationError

from lambda_handlers.handlers import http_handler
from lambda_handlers.errors import EventValidationError

class SchemaValidator:
    """A data validator that uses Marshmallow schemas."""

    @classmethod
    def validate(cls, instance: Any, schema: Schema) -> Any:
        """Return the data or raise EventValidationError if any error from validating `instance` against `schema`."""
        try:
            return schema.load(instance)
        except ValidationError as error:
            raise EventValidationError(error.messages)

class UserSchema(Schema):
    user_id = fields.Integer(required=True)

@http_handler()
def handler(event, context):
    user = event['body']
    SchemaValidator.validate(user, UserSchema())
    return user
```

```bash
aws lambda invoke --function-name example --payload '{"body": {"user_id": 42}}' response.json
cat response.json
```

```json
{
    "headers":{
        "Access-Control-Allow-Credentials": true,
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    },
    "statusCode": 200,
    "body": "{\"user_id\": 42}"
}
```

```bash
aws lambda invoke --function-name example --payload '{"body": {"user_id": "peter"}}' response.json
cat response.json
```

```json
{
    "headers":{
        "Access-Control-Allow-Credentials": true,
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    },
    "statusCode": 400,
    "body": "{\"errors\": {\"user_id\": [\"Not a valid integer.\"]}"
}
```
