import logging
from typing import Any, Dict

from lambda_handlers import formatters
from lambda_handlers.types import Headers, APIGatewayProxyResult
from lambda_handlers.errors import (
    NotFoundError,
    BadRequestError,
    ValidationError,
    ResponseValidationError,
)
from lambda_handlers.response import CorsHeaders
from lambda_handlers.handlers.lambda_handler import LambdaHandler
from lambda_handlers.response.response_builder import (
    ok,
    not_found,
    bad_request,
    bad_implementation,
    internal_server_error,
)

logger = logging.getLogger(__name__)


class HTTPHandler(LambdaHandler):
    """
    Decorator class to facilitate the definition of AWS HTTP Lambda handlers with:
       - input validation,
       - output formatting,
       - CORS headers, and
       - error handling.

    Parameters
    ----------
    cors: lambda_decorator.response.CorsHeaders
        Definition of the CORS headers.

    body_format: Callable
        Formatter callable to parse the input body.

    output_format: Callable
        Formatter callable to format the output body from the return value of the handler function.

    validation: TBD
        A callable or schema definition to validate: body, pathParameters, queryParameters, and response.
    """

    def __init__(self, cors=None, body_format=None, output_format=None, validation=None):
        self._format_body = body_format or formatters.input_format.json
        self._validator = validation
        self._format_output = output_format or formatters.output_format.json
        self._cors = cors or CorsHeaders(origin='*', credentials=True)

    def before(self, event, context):
        self._validate_request(event, context)
        self._parse_body(event)
        return event, context

    def after(self, result):
        if not isinstance(result, APIGatewayProxyResult) and 'statusCode' not in result:
            result = ok(result)
        response = self._create_response(result)
        self._validate_response(response)
        return response

    def on_exception(self, exception):
        return self._create_response(self._handle_error(exception))

    def _validate_request(self, event, context):
        if self._validator:
            transformed_event = transformed_context = self._validator.validate_request(event, context)
            event.update(transformed_event)
            context.update(transformed_context)

    def _validate_response(self, response):
        if self._validator:
            self._validator.validate_response(response)

    def _parse_body(self, event):
        if 'body' in event:
            event['body'] = self._format_body(event['body'])

    def _create_response(self, result: APIGatewayProxyResult) -> Dict[str, Any]:
        result.headers = self._create_headers(result.headers)
        result.body = self._format_output(result.body)
        return result.asdict()

    def _create_headers(self, headers: Headers) -> Headers:
        if not headers:
            headers = {}

        if self._cors:
            headers.update(self._cors.create_headers())

        return headers or None

    def _handle_error(self, error) -> APIGatewayProxyResult:
        if isinstance(error, NotFoundError):
            return not_found(str(error))
        if isinstance(error, ResponseValidationError):
            return bad_implementation(str(error))
        if isinstance(error, (BadRequestError, ValidationError)):
            return bad_request(str(error))

        logger.error(error)
        return internal_server_error()
