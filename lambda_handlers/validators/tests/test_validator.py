from typing import Any, Dict, List
from contextlib import contextmanager
from collections import defaultdict

import pytest

from lambda_handlers.errors import (
    RequestValidationError,
    ResponseValidationError,
)
from lambda_handlers.validators import Validator


@contextmanager
def not_raises(expected_exception):
    try:
        yield

    except expected_exception:
        raise AssertionError(
            f'Did raise exception {expected_exception} when it should not!',
        )

    except Exception as err:
        raise AssertionError(
            f'An unexpected exception {err} raised.',
        )


class SimpleSchemaValidator(Validator):

    def validate(self, instance: Any, schema: dict):
        cumulative_errors = []

        for key, type_def in schema.items():
            if key not in instance:
                cumulative_errors.append({key: 'missing'})
            elif isinstance(type_def, dict):
                _, errors = self.validate(instance[key], type_def)
                if errors:
                    cumulative_errors.extend(errors)
            elif type(instance[key]) != type_def:
                cumulative_errors.append({key: f'{instance[key]} is not of type {type_def}'})

        return instance, cumulative_errors

    def format_errors(self, errors) -> List[Dict[str, Any]]:
        path_errors: Dict[str, List[str]] = defaultdict(list)
        for error in errors:
            for key, value in error.items():
                path_errors[key].append(value)
        return [{path: messages} for path, messages in path_errors.items()]


class TestValidatorWithoutSchema:

    @pytest.fixture
    def subject(self):
        return SimpleSchemaValidator()

    def test_validate_request(self, subject, mocker):
        event = {}
        context = {}
        validate_spy = mocker.spy(subject, 'validate')
        assert (event, context) == subject.validate_request(event, context)
        assert validate_spy.call_count == 0

    def test_validate_response(self, subject, mocker):
        response = {}
        validate_spy = mocker.spy(subject, 'validate')
        assert response == subject.validate_response(response)
        assert validate_spy.call_count == 0


class TestValidatorWithRequestSchema:

    @pytest.fixture
    def subject(self):
        schema = {
            'price': int,
            'accountable': bool,
            'comment': str,
        }
        return SimpleSchemaValidator(request=schema)

    def test_validate_valid_request(self, subject):
        event = {
            'price': 12,
            'accountable': True,
            'comment': 'some comment',
        }
        context = {}
        with not_raises(RequestValidationError):
            subject.validate_request(event, context)

    def test_validate_invalid_request(self, subject):
        event = {
            'price': '12',
        }
        context = {}

        with pytest.raises(RequestValidationError) as error:
            subject.validate_request(event, context)

        assert isinstance(error.value.description, list)
        assert len(error.value.description) == 3
        assert {'price': ['12 is not of type <class \'int\'>']} in error.value.description
        assert {'accountable': ['missing']} in error.value.description
        assert {'comment': ['missing']} in error.value.description


class TestValidatorWithResponseSchema:

    @pytest.fixture
    def subject(self):
        schema = {
            'user': dict,
            'accountable': bool,
        }
        return SimpleSchemaValidator(response=schema)

    def test_validate_response(self, subject):
        response = {
            'user': {'name': 'Peter Baker'},
            'accountable': False,
        }
        with not_raises(ResponseValidationError):
            assert subject.validate_response(response) == response

    def test_validate_invalid_response(self, subject):
        response = {
            'user': 12,
        }

        with pytest.raises(ResponseValidationError) as error:
            subject.validate_response(response)

        assert isinstance(error.value.description, list)
        assert len(error.value.description) == 2
        assert {'user': ['12 is not of type <class \'dict\'>']} in error.value.description
        assert {'accountable': ['missing']} in error.value.description


class TestValidatorWithPathParametersSchema:

    @pytest.fixture
    def subject(self):
        path_parameters_schema = {
            'user_name': str,
            'accountable': bool,
        }
        return SimpleSchemaValidator(path=path_parameters_schema)

    def test_validate_valid(self, subject):
        event = {
            'pathParameters': {
                'user_name': 'Peter Baker',
                'accountable': True,
            },
        }
        context = {}
        with not_raises(RequestValidationError):
            subject.validate_request(event, context)

    def test_validate_invalid_request(self, subject):
        event = {
            'pathParameters': {
                'user_name': True,
            },
        }
        context = {}

        with pytest.raises(RequestValidationError) as error:
            subject.validate_request(event, context)

        nested_errors = error.value.description
        assert isinstance(nested_errors, list)
        assert len(nested_errors) == 1

        path_parameters_errors = next(
            errors['pathParameters'] for errors in nested_errors if 'pathParameters' in errors
        )
        assert isinstance(path_parameters_errors, list)
        assert {'user_name': ['True is not of type <class \'str\'>']} in path_parameters_errors
        assert {'accountable': ['missing']} in path_parameters_errors


class TestValidatorWithPathParametersSchemaAndQueryStringParametersSchema:

    @pytest.fixture
    def subject(self):
        path_parameters_schema = {
            'user_name': str,
            'accountable': bool,
        }
        query_string_parameters_schema = {
            'filter': str,
        }
        return SimpleSchemaValidator(path=path_parameters_schema, query=query_string_parameters_schema)

    def test_validate_valid_request(self, subject):
        event = {
            'pathParameters': {
                'user_name': 'Peter Baker',
                'accountable': True,
            },
            'queryStringParameters': {
                'filter': 'a,b,c',
            },
        }
        context = {}
        with not_raises(RequestValidationError):
            subject.validate_request(event, context)

    def test_validate_invalid_request(self, subject):
        event = {
            'pathParameters': {
                'user_name': True,
            },
            'queryStringParameters': {
                'filter': 100,
            },
        }
        context = {}

        with pytest.raises(RequestValidationError) as error:
            subject.validate_request(event, context)

        nested_errors = error.value.description
        assert isinstance(nested_errors, list)
        assert len(nested_errors) == 2

        path_parameters_errors = next(
            errors['pathParameters'] for errors in nested_errors if 'pathParameters' in errors
        )
        assert isinstance(path_parameters_errors, list)
        assert {'user_name': ['True is not of type <class \'str\'>']} in path_parameters_errors
        assert {'accountable': ['missing']} in path_parameters_errors

        query_string_parameters_errors = next(
            errors['queryStringParameters'] for errors in nested_errors if 'queryStringParameters' in errors
        )
        assert isinstance(query_string_parameters_errors, list)
        assert {'filter': ['100 is not of type <class \'str\'>']} in query_string_parameters_errors


class TestValidatorWithPathParametersSchemaAndQueryStringParametersSchemaAndBodySchema:

    @pytest.fixture
    def subject(self):
        path_parameters_schema = {
            'user_name': str,
            'accountable': bool,
        }
        query_string_parameters_schema = {
            'filter': str,
        }
        body_schema = {
            'content': str,
        }
        return SimpleSchemaValidator(
            path=path_parameters_schema,
            query=query_string_parameters_schema,
            body=body_schema,
        )

    def test_validate_valid_request(self, subject):
        event = {
            'pathParameters': {
                'user_name': 'Peter Baker',
                'accountable': True,
            },
            'queryStringParameters': {
                'filter': 'a,b,c',
            },
            'body': {
                'content': 'some long text',
            },
        }
        context = {}
        with not_raises(RequestValidationError):
            subject.validate_request(event, context)

    def test_validate_invalid_request(self, subject):
        event = {
            'pathParameters': {
                'user_name': True,
            },
            'queryStringParameters': {
                'filter': 100,
            },
        }
        context = {}

        with pytest.raises(RequestValidationError) as error:
            subject.validate_request(event, context)

        nested_errors = error.value.description
        assert isinstance(nested_errors, list)
        assert len(nested_errors) == 3

        path_parameters_errors = next(
            errors['pathParameters'] for errors in nested_errors if 'pathParameters' in errors
        )
        assert isinstance(path_parameters_errors, list)
        assert {'user_name': ['True is not of type <class \'str\'>']} in path_parameters_errors
        assert {'accountable': ['missing']} in path_parameters_errors

        query_string_parameters_errors = next(
            errors['queryStringParameters'] for errors in nested_errors if 'queryStringParameters' in errors
        )
        assert isinstance(query_string_parameters_errors, list)
        assert {'filter': ['100 is not of type <class \'str\'>']} in query_string_parameters_errors

        body_parameters_errors = next(
            errors['body'] for errors in nested_errors if 'body' in errors
        )
        assert isinstance(body_parameters_errors, list)
        assert {'content': ['missing']} in body_parameters_errors


class TestValidatorWithRequestSchemaAndPathParametersSchema:

    @pytest.fixture
    def subject(self):
        request_schema = {
            'price': int,
            'accountable': bool,
        }
        path_parameters_schema = {
            'user_name': str,
        }
        return SimpleSchemaValidator(request=request_schema, path=path_parameters_schema)

    def test_validate_valid_request_takes_precedence(self, subject):
        event = {
            'price': 12,
            'accountable': True,
        }
        context = {}
        with not_raises(RequestValidationError):
            subject.validate_request(event, context)

    def test_validate_invalid_request(self, subject):
        event = {
            'price': '12',
        }
        context = {}

        with pytest.raises(RequestValidationError) as error:
            subject.validate_request(event, context)

        assert isinstance(error.value.description, list)
        assert len(error.value.description) == 2
        assert {'price': ['12 is not of type <class \'int\'>']} in error.value.description
        assert {'accountable': ['missing']} in error.value.description
