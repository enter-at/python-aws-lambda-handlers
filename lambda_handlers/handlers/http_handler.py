from typing import Optional, Dict, Any
import logging

from lambda_handlers import formatters
from lambda_handlers.response import Cors
from lambda_handlers.handlers import LambdaHandler
from lambda_handlers.types import APIGatewayProxyResult
from lambda_handlers.errors import BadRequestError, NotFoundError, ValidationError
from lambda_handlers.response.builder import not_found, bad_request, internal_server_error, ok


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
    cors: lambda_decorator.response.Cors
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
        self._cors = cors or Cors(origin='*', credentials=True)

    def before(self, event, context):
        self._validate(event, context)
        self._parse_body(event)
        return event, context

    def after(self, result):
        if not isinstance(result, APIGatewayProxyResult) and 'statusCode' not in result:
            result = ok(result)
        return self._create_response(result)

    def on_exception(self, exception):
        return self._create_response(self._handle_error(exception))

    def _validate(self, event, context):
        if self._validator:
            self._validator(event, context)

    def _parse_body(self, event):
        if 'body' in event:
            event['body'] = self._format_body(event['body'])

    def _create_response(self, result: APIGatewayProxyResult) -> Dict[str, any]:
        result.headers = self._create_headers(result.headers)
        result.body = self._format_output(result.body)
        return result.asdict()

    def _create_headers(self, headers: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not headers:
            headers = {}

        if self._cors:
            headers.update(self._cors.create_headers())
        return headers or None

    def _handle_error(self, error) -> APIGatewayProxyResult:
        if isinstance(error, NotFoundError):
            return not_found(str(error))
        if isinstance(error, ValidationError):
            return bad_request(str(error))
        if isinstance(error, BadRequestError):
            return bad_request(str(error))

        logger.error(error)
        return internal_server_error()
