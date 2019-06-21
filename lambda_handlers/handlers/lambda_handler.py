import logging
from abc import ABC
from functools import wraps

logger = logging.getLogger(__name__)


class LambdaHandler(ABC):
    def __call__(self, handler):
        @wraps(handler)
        def wrapper(event, context):
            return self._call_handler(handler, event, context)
        return wrapper

    def _call_handler(self, handler, event, context):
        try:
            return self.after(handler(*self.before(event, context)))
        except Exception as exception:
            return self.on_exception(exception)

    def before(self, event, context):
        return event, context

    def after(self, result):
        return result

    def on_exception(self, exception):
        logger.error(exception)
        return exception
