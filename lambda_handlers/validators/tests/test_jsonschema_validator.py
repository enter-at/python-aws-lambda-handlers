from typing import Any, Dict

import pytest

from lambda_handlers.validators import Validator
from lambda_handlers.validators.jsonschema_validator import JSONSchemaValidator


@pytest.fixture(scope='session')
def schema() -> Dict[str, Any]:
    return {
        'type': 'object',
        'properties': {
            'price': {'type': 'number'},
        },
    }


@pytest.fixture(scope='session')
def validator(schema) -> JSONSchemaValidator:
    return JSONSchemaValidator()


class TestJSONSchemaValidator:

    def test_create(self, validator):
        assert isinstance(validator, Validator)

    def test_validate_valid_data(self, validator, schema):
        event = {'price': 100}
        data, errors = validator.validate(event, schema)
        assert data == event
        assert not errors
        assert 'price' in data
        assert data['price'] == 100

    def test_validate_invalid_data(self, validator, schema):
        event = {'price': '100'}
        data, errors = validator.validate(event, schema)
        assert data == event
        assert errors
        assert len(errors) == 1
        assert errors[0].message == "'100' is not of type 'number'"

    def test_validate_none_data(self, validator, schema):
        event = None
        data, errors = validator.validate(event, schema)
        assert data == event
        assert errors
        assert len(errors) == 1
        assert errors[0].message == "None is not of type 'object'"


class TestJSONSchemaValidatorFormatErrors:

    def test_format_errors(self, validator, schema):
        event = {'price': '100'}
        data, errors = validator.validate(event, schema)
        assert validator.format_errors(errors) == [{'price': ["'100' is not of type 'number'"]}]

    def test_format_empty_list_of_errors(self, validator, schema):
        assert validator.format_errors([]) == []
