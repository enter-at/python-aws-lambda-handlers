import pytest

from lambda_handlers.validators.http.http_validator import HttpValidator
from lambda_handlers.validators.jsonschema_validator import JSONSchemaValidator
from lambda_handlers.validators.http.http_jsonschema_validator import HttpJSONSchemaValidator


@pytest.fixture(scope='session')
def validator() -> HttpJSONSchemaValidator:
    return HttpJSONSchemaValidator()


class TestHttpJSONSchemaValidator:

    def test_create(self, validator):
        assert isinstance(validator, JSONSchemaValidator)
        assert isinstance(validator, HttpValidator)
