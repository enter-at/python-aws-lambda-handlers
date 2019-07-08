from typing import Any, Dict

import pytest

from lambda_handlers.errors import EventValidationError, ResultValidationError
from lambda_handlers.validators.validator import Validator


class RecordValidator(Validator):
    def __init__(self, records=None, input_schema=None, output_schema=None):
        super().__init__(input_schema=input_schema, output_schema=output_schema)
        self._schemas = {'records': records}

    @property
    def schemas(self) -> Dict[str, Any]:
        return self._schemas


@pytest.fixture
def simple_schema_validator(simple_schema_validator_builder):
    return simple_schema_validator_builder(RecordValidator)


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


class TestValidatorWithInputSchema:

    @pytest.fixture
    def subject(self, simple_schema_validator):
        schema = {
            'price': int,
            'accountable': bool,
            'comment': str,
        }
        return simple_schema_validator(input_schema=schema)

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


class TestValidatorWithResultSchema:

    @pytest.fixture
    def subject(self, simple_schema_validator):
        schema = {
            'user': dict,
            'accountable': bool,
        }
        return simple_schema_validator(output_schema=schema)

    def test_validate_result(self, subject):
        result = {
            'user': {'name': 'Peter Baker'},
            'accountable': False,
        }
        assert subject.validate_result(result) == result

    def test_validate_invalid_result(self, subject):
        result = {
            'user': 12,
        }

        with pytest.raises(ResultValidationError) as error:
            subject.validate_result(result)

        assert isinstance(error.value.description, list)
        assert len(error.value.description) == 2
        assert {'user': ['12 is not of type <class \'dict\'>']} in error.value.description
        assert {'accountable': ['missing']} in error.value.description


class TestValidatorWithRecordsSchema:

    @pytest.fixture
    def subject(self, simple_schema_validator):
        records_schema = {
            'user_name': str,
            'accountable': bool,
        }
        return simple_schema_validator(records=records_schema)

    def test_validate_valid(self, subject):
        event = {
            'records': {
                'user_name': 'Peter Baker',
                'accountable': True,
            },
        }
        context = {}
        assert subject.validate_event(event, context)

    def test_validate_invalid_request(self, subject):
        event = {
            'records': {
                'user_name': True,
            },
        }
        context = {}

        with pytest.raises(EventValidationError) as error:
            subject.validate_event(event, context)

        nested_errors = error.value.description
        assert isinstance(nested_errors, list)
        assert len(nested_errors) == 1

        records_errors = next(errors['records'] for errors in nested_errors if 'records' in errors)
        assert isinstance(records_errors, list)
        assert {'user_name': ['True is not of type <class \'str\'>']} in records_errors
        assert {'accountable': ['missing']} in records_errors


class TestValidatorWithInputSchemaAndRecordsSchema:

    @pytest.fixture
    def subject(self, simple_schema_validator):
        input_schema = {
            'price': int,
            'accountable': bool,
        }
        records_schema = {
            'user_name': str,
        }
        return simple_schema_validator(input_schema=input_schema, records=records_schema)

    def test_validate_input_schema_takes_precedence(self, subject):
        event = {
            'price': 12,
            'accountable': True,
        }
        context = {}
        assert subject.validate_event(event, context)

    def test_validate_invalid_input(self, subject):
        event = {
            'price': '12',
        }
        context = {}

        with pytest.raises(EventValidationError) as error:
            subject.validate_event(event, context)

        assert isinstance(error.value.description, list)
        assert len(error.value.description) == 2
        assert {'price': ['12 is not of type <class \'int\'>']} in error.value.description
        assert {'accountable': ['missing']} in error.value.description
