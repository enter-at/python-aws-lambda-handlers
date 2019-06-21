# -*- coding: utf-8 -*-
import logging
from functools import wraps
from typing import List, Dict, Union
from collections import defaultdict
from lambda_handlers.response.builder import bad_request, internal_server_error

try:
    import jsonschema  # noqa
except ImportError:
    jsonschema = None


logger = logging.getLogger(__name__)


def json_schema_validator(request_schema=None, response_schema=None):
    """
    Validate your request & response payloads against a JSONSchema.

    *NOTE: depends on the* `jsonschema <https://github.com/Julian/jsonschema>` package.
    *If you're using* `serverless-python-requirements <https://github.com/UnitedIncome/serverless-python-requirements>`_
    *you're all set. If you cURLed* ``lambda_handlers.py`` *you'll have to
    install it manually in your service's root directory.*

    Usage::

      >>> from jsonschema import ValidationError
      >>> from lambda_handlers import json_schema_validator
      >>> @json_schema_validator(request_schema={
      ... 'type': 'object', 'properties': {'price': {'type': 'number'}}})
      ... def handler(event, context):
      ...     return event['price']
      >>> handler({'price': 'bar'}, object())
      {'statusCode': 400, 'body': "{'price': ['bar' is not of type 'number']}"}
      >>> @json_schema_validator(response_schema={
      ... 'type': 'object', 'properties': {'price': {'type': 'number'}}})
      ... def handler(event, context):
      ...     return {'price': 'bar'}
      >>> handler({}, object())
      {'statusCode': 500, 'body': "{'price': ['bar' is not of type 'number']}"}
    """
    def wrapper_wrapper(handler):
        @wraps(handler)
        def wrapper(event, context):
            if jsonschema is None:
                logger.error('jsonschema is not installed, skipping response validation')
                return

            if request_schema is not None:
                errors = _validate(event, request_schema)
                if errors:
                    raise lambda_handlers.errors.ValidationError(errors)
                    # return bad_request(errors).asdict()

            response = handler(event, context)

            if response_schema is not None:
                errors = _validate(response, response_schema)
                if errors:
                    raise lambda_handlers.errors.ValidationError(errors)
                    # return internal_server_error(errors).asdict()

            return response

        return wrapper

    return wrapper_wrapper


def _validate(instance, schema: dict) -> Union[List[Dict[str, List[str]]], None]:
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    if errors:
        return _normalized_messages(errors)


def _normalized_messages(errors: List[jsonschema.ValidationError]) -> List[Dict[str, List[str]]]:
    path_errors = defaultdict(list)
    for error in errors:
        path_errors[error.path.pop()].append(error.message)

    return [{path: messages} for path, messages in path_errors.items()]
