"""Handler decorator classes."""

from .http_handler import HTTPHandler  # noqa
from .event_handler import EventHandler  # noqa
from .lambda_handler import LambdaHandler  # noqa

http_handler = HTTPHandler
event_handler = EventHandler
