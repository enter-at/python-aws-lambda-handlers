import json
from typing import Callable

import pytest

from marshmallow import Schema, fields
from marshmallow.validate import Range

from lambda_handlers import validators
from lambda_handlers.handlers import event_handler
from lambda_handlers.errors import FormatError


class TestEventHandlerDefaults:

    @pytest.fixture
    def handler(self) -> Callable:
        @event_handler()
        def handler(event, context):
            return event
        return handler

    def test_empty_body_validation(self, handler):
        response = handler('{"a": 1}', None)
        assert response == '{"a": 1}'

    def test_invalid_body_validation(self, handler):
        with pytest.raises(FormatError, match='Unexpected type for JSON input'):
            handler({}, None)


class TestEventHandlerValidation:

    @pytest.fixture
    def handler(self):
        class EventSchema(Schema):
            price = fields.Integer(required=True, validate=Range(min=1, max=100))
            timestamp = fields.Date(required=True)

        class ResponseSchema(Schema):
            message = fields.String(required=True)

        @event_handler(
            validator=validators.marshmallow(
                input_schema=EventSchema(),
                output_schema=ResponseSchema(),
            ),
        )
        def handler(event, context) -> Callable:
            price = event['price']
            timestamp = event['timestamp']
            response = {
                'message': f'The price on {timestamp} is {price}.'
            }
            return response
        return handler

    def test_validation(self, handler):
        event = {
            'price': 99,
            'timestamp': '2019-01-10',
        }
        event_payload = json.dumps(event)
        response = handler(event_payload, None)
        assert response == '{"message": "The price on 2019-01-10 is 99."}'

    def test_invalid_body_validation(self, handler):
        with pytest.raises(FormatError, match='Unexpected type for JSON input'):
            handler({}, None)
