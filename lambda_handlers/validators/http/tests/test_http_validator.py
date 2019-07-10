import pytest

from lambda_handlers.errors import EventValidationError, ResultValidationError
from lambda_handlers.validators.http.http_validator import HttpValidator


@pytest.fixture
def simple_schema_validator(simple_schema_validator_builder):
    return simple_schema_validator_builder(HttpValidator)


class TestValidatorWithoutSchema:

    @pytest.fixture
    def subject(self, simple_schema_validator):
        return simple_schema_validator()

    def test_validate_event(self, subject, mocker):
        event = {}
        context = {}
        validate_spy = mocker.spy(subject, 'validate')
        assert (event, context) == subject.validate_event(event, context)
        assert validate_spy.call_count == 0

    def test_validate_result(self, subject, mocker):
        response = {}
        validate_spy = mocker.spy(subject, 'validate')
        assert response == subject.validate_result(response)
        assert validate_spy.call_count == 0


class TestValidatorWithRequestSchema:

    @pytest.fixture
    def subject(self, simple_schema_validator):
        schema = {
            'price': int,
            'accountable': bool,
            'comment': str,
        }
        return simple_schema_validator(request=schema)

    def test_validate_valid_request(self, subject):
        event = {
            'price': 12,
            'accountable': True,
            'comment': 'some comment',
        }
        context = {}
        assert subject.validate_event(event, context)

    def test_validate_invalid_request(self, subject):
        event = {
            'price': '12',
        }
        context = {}

        with pytest.raises(EventValidationError) as error:
            subject.validate_event(event, context)

        assert isinstance(error.value.description, list)
        assert len(error.value.description) == 3
        assert {'price': ['12 is not of type <class \'int\'>']} in error.value.description
        assert {'accountable': ['missing']} in error.value.description
        assert {'comment': ['missing']} in error.value.description


class TestValidatorWithResponseSchema:

    @pytest.fixture
    def subject(self, simple_schema_validator):
        schema = {
            'user': dict,
            'accountable': bool,
        }
        return simple_schema_validator(response=schema)

    def test_validate_response(self, subject):
        response = {
            'user': {'name': 'Peter Baker'},
            'accountable': False,
        }
        assert subject.validate_result(response) == response

    def test_validate_invalid_response(self, subject):
        response = {
            'user': 12,
        }

        with pytest.raises(ResultValidationError) as error:
            subject.validate_result(response)

        assert isinstance(error.value.description, list)
        assert len(error.value.description) == 2
        assert {'user': ['12 is not of type <class \'dict\'>']} in error.value.description
        assert {'accountable': ['missing']} in error.value.description


class TestValidatorWithPathParametersSchema:

    @pytest.fixture
    def subject(self, simple_schema_validator):
        path_parameters_schema = {
            'user_name': str,
            'accountable': bool,
        }
        return simple_schema_validator(path=path_parameters_schema)

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
        assert {'user_name': ['True is not of type <class \'str\'>']} in path_parameters_errors
        assert {'accountable': ['missing']} in path_parameters_errors


class TestValidatorWithPathParametersSchemaAndQueryStringParametersSchema:

    @pytest.fixture
    def subject(self, simple_schema_validator):
        path_parameters_schema = {
            'user_name': str,
            'accountable': bool,
        }
        query_string_parameters_schema = {
            'filter': str,
        }
        return simple_schema_validator(path=path_parameters_schema, query=query_string_parameters_schema)

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
        assert subject.validate_event(event, context)

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

        with pytest.raises(EventValidationError) as error:
            subject.validate_event(event, context)

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
    def subject(self, simple_schema_validator):
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
        return simple_schema_validator(
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
        assert subject.validate_event(event, context)

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

        with pytest.raises(EventValidationError) as error:
            subject.validate_event(event, context)

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
