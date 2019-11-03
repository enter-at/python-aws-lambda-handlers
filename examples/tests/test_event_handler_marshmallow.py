import pytest

from ..event_handler_marshmallow import handler


class TestEventHandlerValidation:

    def test_event_handler(self):
        event = {
            'price': 99,
            'timestamp': '01-10-2019',
        }
        response = handler(event, None)
        assert isinstance(response, dict)
        assert response['message'] == 200
