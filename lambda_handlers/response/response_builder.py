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


def ok(result: str) -> APIGatewayProxyResult:
    return _build_request(result, HTTPStatus.OK)


def created(result: str) -> APIGatewayProxyResult:
    return _build_request(result, HTTPStatus.CREATED)


def no_content() -> APIGatewayProxyResult:
    return _build_request(None, HTTPStatus.NO_CONTENT)


def not_found(description: str) -> APIGatewayProxyResult:
    error = NotFoundError(description)
    return _build_request(error, HTTPStatus.NOT_FOUND)


def bad_request(description: str) -> APIGatewayProxyResult:
    error = BadRequestError(description)
    return _build_request(error, HTTPStatus.BAD_REQUEST)


def forbidden(description: str) -> APIGatewayProxyResult:
    error = ForbiddenError(description)
    return _build_request(error, HTTPStatus.FORBIDDEN)


def bad_implementation(description: str = None) -> APIGatewayProxyResult:
    return internal_server_error(description or 'BadImplementation')


def internal_server_error(description: str = None) -> APIGatewayProxyResult:
    error = InternalServerError(description or 'InternalServerError')
    return _build_request(error, HTTPStatus.INTERNAL_SERVER_ERROR)


def _build_request(result: Union[LambdaError, Any], status_code: HTTPStatus) -> APIGatewayProxyResult:
    if isinstance(result, LambdaError):
        body = {'errors': result.description}
    else:
        body = result

    return APIGatewayProxyResult(body=body, statusCode=status_code.value)
