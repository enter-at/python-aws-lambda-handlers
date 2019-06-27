from abc import ABC
from typing import Any, Dict, Tuple, Callable
from functools import wraps

Event = Dict[str, Any]
Context = Dict[str, Any]


class LambdaHandler(ABC):
    def __call__(self, handler: Callable):
        @wraps(handler)
        def wrapper(event, context):
            return self._call_handler(handler, event, context)

        return wrapper

    def _call_handler(
        self,
        handler: Callable,
        event: Event,
        context: Context,
    ) -> Any:
        try:
            return self.after(handler(*self.before(event, context)))
        except Exception as exception:
            return self.on_exception(exception)

    def before(self, event: Event, context: Context) -> Tuple[Event, Context]:
        return event, context

    def after(self, result: Any) -> Any:
        return result

    def on_exception(self, exception: Exception) -> Any:
        raise exception
