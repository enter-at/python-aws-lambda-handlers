"""Handler decorator classes."""

from lambda_handlers.handlers.http_handler import HTTPHandler  # noqa
from lambda_handlers.handlers.event_handler import EventHandler  # noqa
from lambda_handlers.handlers.lambda_handler import LambdaHandler  # noqa

http_handler = HTTPHandler
event_handler = EventHandler
