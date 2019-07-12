"""Functions to help building HTTP responses."""

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
    """Return a response with OK status code."""
    return _build_response(result, HTTPStatus.OK)


def created(result: Any) -> APIGatewayProxyResult:
    """Return a response with CREATED status code."""
    return _build_response(result, HTTPStatus.CREATED)


def no_content() -> APIGatewayProxyResult:
    """Return a response with NO CONTENT status code."""
    return _build_response(None, HTTPStatus.NO_CONTENT)


def not_found(description: Any) -> APIGatewayProxyResult:
    """Return a response with NOT FOUND status code."""
    error = NotFoundError(description)
    return _build_response(error, HTTPStatus.NOT_FOUND)


def bad_request(description: Any) -> APIGatewayProxyResult:
    """Return a response with BAD REQUEST status code."""
    error = BadRequestError(description)
    return _build_response(error, HTTPStatus.BAD_REQUEST)


def forbidden(description: Any) -> APIGatewayProxyResult:
    """Return a response with FORBIDDEN status code."""
    error = ForbiddenError(description)
    return _build_response(error, HTTPStatus.FORBIDDEN)


def bad_implementation(description: Any = None) -> APIGatewayProxyResult:
    """Return a Internal Server Error response."""
    return internal_server_error(description)


def internal_server_error(description: Any = None) -> APIGatewayProxyResult:
    """Return a Internal Server Error response."""
    error = InternalServerError(description or 'An internal server error occurred')
    return _build_response(error, HTTPStatus.INTERNAL_SERVER_ERROR)


def _build_response(result: Union[LambdaError, Any], status_code: HTTPStatus) -> APIGatewayProxyResult:
    if isinstance(result, LambdaError):
        body = {'errors': result.description}
    else:
        body = result

    return APIGatewayProxyResult(body=body, statusCode=status_code.value)
