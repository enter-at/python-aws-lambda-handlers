"""A base class for AWS Lambda handlers."""

from abc import ABC
from typing import Any, Dict, Tuple, NewType, Callable, Optional
from functools import wraps

Event = Dict[str, Any]
LambdaContext = NewType('LambdaContext', object)


class LambdaHandler(ABC):
    """A base class for AWS Lambda handlers.

    Contain hooks to be called before, after, and when an exception is raised.
    """

    def __init__(self, handler: Optional[Callable] = None):
        self._handler = handler

    def __call__(self, handler: Callable):  # noqa: D102
        @wraps(handler)
        def wrapper(*args):
            try:
                handler_self = args[0] if len(args) > 2 else None
                return self.after(self._call_handler(handler_self, handler, *self.before(*args[-2:])))
            except Exception as exception:
                return self.on_exception(exception)

        return wrapper

    def _call_handler(self, handler_self, handler, event, context):
        if handler_self:
            return handler(handler_self, event, context)

        return handler(event, context)

    def before(self, event: Event, context: LambdaContext) -> Tuple[Event, LambdaContext]:
        """Event method to be called just before the handler is executed."""
        return event, context

    def after(self, result: Any) -> Any:
        """Event method to be called just after the handler is executed."""
        return result

    def on_exception(self, exception: Exception) -> Any:
        """Event method to be called when an exception is raised."""
        raise exception
