import pytest

from lambda_handlers.errors import FormatError
from lambda_handlers.handlers import event_handler


class TestEventHandlerDefaults:

    @pytest.fixture
    def handler(self):
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
