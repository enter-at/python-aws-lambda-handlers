import pytest

from lambda_handlers import APIGatewayProxyResult
from lambda_handlers.response.response_builder import (
    ok,
    created,
    forbidden,
    not_found,
    no_content,
    bad_request,
    bad_implementation,
    internal_server_error,
)


class TestResponseBuilder:

    @pytest.mark.parametrize(
        'description, builder, status_code, body',
        [
            ('invalid payload', bad_request, 400, {'errors': 'invalid payload'}),
            ('missing credentials', forbidden, 403, {'errors': 'missing credentials'}),
            ('invalid response format', bad_implementation, 500, {'errors': 'invalid response format'}),
            ('unknown error', internal_server_error, 500, {'errors': 'unknown error'}),
            ('user not found', not_found, 404, {'errors': 'user not found'}),
            ({'user': 'Peter Fox'}, ok, 200, {'user': 'Peter Fox'}),
            ({'user_id': 1245}, created, 201, {'user_id': 1245}),
        ],
    )
    def test_builder_with_description(self, description, builder, status_code, body):
        response = builder(description)
        assert isinstance(response, APIGatewayProxyResult)
        assert response.body == body
        assert response.statusCode == status_code
        assert response.headers is None
        assert response.multiValueHeaders is None
        assert response.isBase64Encoded is None

    @pytest.mark.parametrize(
        'builder, status_code, body',
        [
            (no_content, 204, None),
            (bad_implementation, 500, {'errors': 'An internal server error occurred'}),
            (internal_server_error, 500, {'errors': 'An internal server error occurred'}),
        ],
    )
    def test_builder_without_description(self, builder, status_code, body):
        response = builder()
        assert isinstance(response, APIGatewayProxyResult)
        assert response.body == body
        assert response.statusCode == status_code
        assert response.headers is None
        assert response.multiValueHeaders is None
        assert response.isBase64Encoded is None
