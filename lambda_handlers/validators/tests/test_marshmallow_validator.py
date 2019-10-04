from typing import Any, Dict

import pytest
from marshmallow import Schema, fields
from marshmallow.validate import Range

from lambda_handlers.validators.validator import Validator
from lambda_handlers.validators.marshmallow_validator import MarshmallowValidator


class EventSchema(Schema):
    price = fields.Integer(required=True, validate=Range(min=1, max=100))
    total = fields.Integer(validate=Range(min=1, max=99))


@pytest.fixture(scope='session')
def schema() -> Dict[str, Any]:
    return EventSchema()


@pytest.fixture(scope='session')
def validator(schema) -> MarshmallowValidator:
    return MarshmallowValidator()


class TestMarshmallowSchemaValidator:

    def test_create(self, validator):
        assert isinstance(validator, Validator)

    def test_validate_valid_data(self, validator, schema):
        event = {'price': 100}
        data, errors = validator.validate(event, schema)
        assert data
        assert not errors
        assert 'price' in data
        assert data['price'] == 100

    def test_validate_invalid_data(self, validator, schema):
        event = {'price': 'xx100'}
        data, errors = validator.validate(event, schema)
        assert not data
        assert errors
        assert len(errors) == 1
        assert errors['price'] == ['Not a valid integer.']

    def test_validate_none_data(self, validator, schema):
        event = None
        data, errors = validator.validate(event, schema)
        assert not data
        assert errors == {'_schema': ['Invalid input type.']}


class TestMarshmallowSchemaValidatorFormatErrors:

    def test_format_errors(self, validator, schema):
        event = {'price': 'xx100', 'total': 100}
        instance, errors = validator.validate(event, schema)
        formatted_errors = validator.format_errors(errors)
        assert len(formatted_errors) == 2
        assert {'price': ['Not a valid integer.']} in formatted_errors
        assert {'total': ['Must be greater than or equal to 1 and less than or equal to 99.']} in formatted_errors

    def test_format_empty_list_of_errors(self, validator, schema):
        assert validator.format_errors([]) == []
