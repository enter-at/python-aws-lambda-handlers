from typing import Any, Dict, Tuple, cast

import pytest

from lambda_handlers.handlers.lambda_handler import Context, LambdaHandler

Event = Dict[str, Any]


class EventAwareException(Exception):
    def __init__(self, message: str, event: Event):
        self.event = event
        return super().__init__(message)


class CallOrderAwareHandler(LambdaHandler):
    def before(self, event: Event, context: Context) -> Tuple[Event, Context]:
        event['route'].append('before')
        return super().before(event, context)

    def after(self, result: Any) -> Any:
        result['route'].append('after')
        return super().after(result)

    def on_exception(self, exception: Exception) -> Any:
        cast(EventAwareException, exception).event['route'].append('on_exception')
        return super().on_exception(exception)


lambda_handler = CallOrderAwareHandler()


@pytest.fixture
def handler():
    @lambda_handler
    def handler(event, context):
        if context is None:
            raise EventAwareException(message='no such context', event=event)
        return event

    return handler


class TestLambdaHandler:

    @pytest.fixture
    def event(self):
        return {'route': []}

    def test_call_order(self, handler, event):
        result = handler(event, {})

        assert result == event
        assert event['route'] == ['before', 'after']

    def test_call_exception(self, handler, event):
        with pytest.raises(EventAwareException, match='no such context'):
            handler(event, None)

        assert event['route'] == ['before', 'on_exception']
