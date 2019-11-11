import json

from ..event_handler_marshmallow import handler


class TestEventHandlerValidation:

    def test_event_handler(self):
        event = {
            'price': 99,
            'timestamp': '2019-01-10',
        }
        event_payload = json.dumps(event)
        response = handler(event_payload, None)
        assert isinstance(response, str)

        result = json.loads(response)
        assert result['message'] == "The price on 2019-01-10 is 99."
