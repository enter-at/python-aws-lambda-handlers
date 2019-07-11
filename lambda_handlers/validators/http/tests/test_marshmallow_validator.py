import pytest
from marshmallow import Schema, fields

from lambda_handlers.errors import EventValidationError
from lambda_handlers.validators.http.http_validator import HttpValidator
from lambda_handlers.validators.marshmallow_validator import (
    MarshmallowValidator,
)
from lambda_handlers.validators.http.marshmallow_validator import (
    HttpMarshmallowValidator,
)


class TestHttpMarshmallowSchemaValidator:

    @pytest.fixture
    def subject(self) -> HttpMarshmallowValidator:
        return HttpMarshmallowValidator()

    def test_create(self, subject):
        assert isinstance(subject, MarshmallowValidator)
        assert isinstance(subject, HttpValidator)


class TestValidatorWithPathParametersSchema:

    @pytest.fixture
    def subject(self) -> HttpMarshmallowValidator:
        class PathSchema(Schema):
            user_name = fields.String(required=True)
            accountable = fields.Boolean(required=True)

        return HttpMarshmallowValidator(path=PathSchema())

    def test_validate_valid_request(self, subject):
        event = {
            'pathParameters': {
                'user_name': 'Peter Baker',
                'accountable': True,
            },
        }
        context = {}
        assert subject.validate_event(event, context)

    def test_validate_invalid_request(self, subject):
        event = {
            'pathParameters': {
                'user_name': True,
            },
        }
        context = {}

        with pytest.raises(EventValidationError) as error:
            subject.validate_event(event, context)

        nested_errors = error.value.description
        assert isinstance(nested_errors, list)
        assert len(nested_errors) == 1

        path_parameters_errors = next(
            errors['pathParameters'] for errors in nested_errors if 'pathParameters' in errors
        )
        assert isinstance(path_parameters_errors, list)
