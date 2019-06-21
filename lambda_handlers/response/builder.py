import json
from http import HTTPStatus
from typing import Union, Any
from lambda_handlers.types import APIGatewayProxyResult
from lambda_handlers.errors import (
    BadRequestError,
    LambdaError,
    ForbiddenError,
    InternalServerError,
    NotFoundError
)


def bad_request(description: str) -> APIGatewayProxyResult:
    error = BadRequestError(description)
    return _build_request(error, HTTPStatus.BAD_REQUEST)


def forbidden(description: str) -> APIGatewayProxyResult:
    error = ForbiddenError(description)
    return _build_request(error, HTTPStatus.FORBIDDEN)


def internal_server_error(description: str = None) -> APIGatewayProxyResult:
    error = InternalServerError(description or 'InternalServerError')
    return _build_request(error, HTTPStatus.INTERNAL_SERVER_ERROR)


def not_found(description: str) -> APIGatewayProxyResult:
    error = NotFoundError(description)
    return _build_request(error, HTTPStatus.NOT_FOUND)


def ok(result: str) -> APIGatewayProxyResult:
    return _build_request(result, HTTPStatus.OK)


def created(result: str) -> APIGatewayProxyResult:
    return _build_request(result, HTTPStatus.CREATED)


def _build_request(
    result: Union[LambdaError, Any],
    status_code: HTTPStatus
) -> APIGatewayProxyResult:
    if isinstance(result, LambdaError):
        body = {'errors': result.description}
    else:
        body = result

    return APIGatewayProxyResult(body=json.dumps(body), statusCode=status_code.value)
