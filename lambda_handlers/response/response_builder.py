from http import HTTPStatus
from typing import Any, Union

from lambda_handlers.types import APIGatewayProxyResult
from lambda_handlers.errors import (
    LambdaError,
    NotFoundError,
    ForbiddenError,
    BadRequestError,
    InternalServerError,
)


def ok(result: Any) -> APIGatewayProxyResult:
    return _build_response(result, HTTPStatus.OK)


def created(result: Any) -> APIGatewayProxyResult:
    return _build_response(result, HTTPStatus.CREATED)


def no_content() -> APIGatewayProxyResult:
    return _build_response(None, HTTPStatus.NO_CONTENT)


def not_found(description: Any) -> APIGatewayProxyResult:
    error = NotFoundError(description)
    return _build_response(error, HTTPStatus.NOT_FOUND)


def bad_request(description: Any) -> APIGatewayProxyResult:
    error = BadRequestError(description)
    return _build_response(error, HTTPStatus.BAD_REQUEST)


def forbidden(description: Any) -> APIGatewayProxyResult:
    error = ForbiddenError(description)
    return _build_response(error, HTTPStatus.FORBIDDEN)


def bad_implementation(description: Any = None) -> APIGatewayProxyResult:
    return internal_server_error(description)


def internal_server_error(description: Any = None) -> APIGatewayProxyResult:
    error = InternalServerError(description or 'An internal server error occurred')
    return _build_response(error, HTTPStatus.INTERNAL_SERVER_ERROR)


def _build_response(result: Union[LambdaError, Any], status_code: HTTPStatus) -> APIGatewayProxyResult:
    if isinstance(result, LambdaError):
        body = {'errors': result.description}
    else:
        body = result

    return APIGatewayProxyResult(body=body, statusCode=status_code.value)
