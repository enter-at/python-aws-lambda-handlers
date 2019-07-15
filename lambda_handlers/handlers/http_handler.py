"""A handler for HTTP request events."""

import logging
from typing import Any, Dict

from lambda_handlers.types import Headers, APIGatewayProxyResult
from lambda_handlers.errors import (
    FormatError,
    NotFoundError,
    BadRequestError,
    ValidationError,
    ResultValidationError,
)
from lambda_handlers.response import CORSHeaders
from lambda_handlers.handlers.event_handler import EventHandler
from lambda_handlers.response.response_builder import (
    ok,
    not_found,
    bad_request,
    bad_implementation,
    internal_server_error,
)

logger = logging.getLogger(__name__)


class HTTPHandler(EventHandler):
    """
    Decorator class to facilitate the definition of AWS HTTP Lambda handlers.

    Features:
        - input validation,
        - output formatting,
        - CORS headers, and
        - error handling.

    Parameters
    ----------
    cors: lambda_decorator.response.CORSHeaders
        Definition of the CORS headers.
        Default: CORSHeaders(origin='*', credentials=True).

    input_format: Format, optional
        Formatter to parse the input event.
        Default:  formatters.input_format.json.

    output_format: Format, optional
        Formatter to format the output body from the return value of the handler function.
        Default:  formatters.output_format.json.

    validator: Callable, optional
        A callable or schema definition to validate: event, and result.
    """

    def __init__(self, cors=None, input_format=None, output_format=None, validator=None):
        super().__init__(input_format=input_format, output_format=output_format, validator=validator)
        self._cors = cors or CORSHeaders(origin='*', credentials=True)

    def after(self, result):
        """Event method to be called just after the handler is executed."""
        if not isinstance(result, APIGatewayProxyResult) and 'statusCode' not in result:
            result = ok(result)
        return self._create_response(result)

    def on_exception(self, exception):
        """Event method to be called in case an exception is raises."""
        return self._create_response(self._handle_error(exception))

    def format_input(self, event):
        """Return `event` with a formatted `event['body']`."""
        if 'body' in event:
            try:
                event['body'] = self._input_format.format(event['body'])
            except FormatError as error:
                raise FormatError([{'body': [error.description]}])
        return event

    def format_output(self, response):
        """Return `response` with a formatted `response['body']`."""
        response['body'] = self._output_format.format(response['body'])
        return response

    def _create_response(self, result: APIGatewayProxyResult) -> Dict[str, Any]:
        result.headers = self._create_headers(result.headers)
        return self.format_output(self.validate_result(result.asdict()))

    def _create_headers(self, headers: Headers) -> Headers:
        if not headers:
            headers = {}

        if self._output_format:
            headers['Content-Type'] = self._output_format.content_type

        if self._cors:
            headers.update(self._cors.create_headers())

        return headers or None

    def _handle_error(self, error) -> APIGatewayProxyResult:
        if isinstance(error, NotFoundError):
            return not_found(error.description)
        if isinstance(error, ResultValidationError):
            return bad_implementation(error.description)
        if isinstance(error, (BadRequestError, FormatError, ValidationError)):
            return bad_request(error.description)

        logger.error(error)
        return internal_server_error()
