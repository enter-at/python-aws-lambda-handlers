from typing import Any, Dict, List, Tuple

import pytest

from lambda_handlers.validators import Validator


class InMemoryValidator(Validator):

    def validate(self, instance: Any, schema: Any) -> Tuple[Any, List[Any]]:
        pass

    def format_errors(self, errors: List[Any]) -> List[Dict[str, Any]]:
        pass


class TestValidatorWithoutSchema:

    @pytest.fixture
    def subject(self):
        return InMemoryValidator()

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
    pass
