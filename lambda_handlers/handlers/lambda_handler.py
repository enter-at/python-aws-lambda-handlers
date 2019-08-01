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
        def wrapper(event, context):
            return self._call_handler(handler, event, context)

        return wrapper

    def _call_handler(self, handler: Callable, event: Event, context: LambdaContext) -> Any:
        try:
            return self.after(handler(*self.before(event, context)))
        except Exception as exception:
            return self.on_exception(exception)

    def before(self, event: Event, context: LambdaContext) -> Tuple[Event, LambdaContext]:
        """Event method to be called just before the handler is executed."""
        return event, context

    def after(self, result: Any) -> Any:
        """Event method to be called just after the handler is executed."""
        return result

    def on_exception(self, exception: Exception) -> Any:
        """Event method to be called when an exception is raised."""
        raise exception
