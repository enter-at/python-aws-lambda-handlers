import pytest

from lambda_handlers.handlers import http_handler


class TestHTTPHandlerWithoutConfiguration:

    @pytest.fixture
    def handler(self):
        @http_handler()
        def handler(event, context):
            return {'user_id': 12}
        return handler

    def test_empty_body_validation(self, handler, mocker):
        response = handler({}, None)
        assert isinstance(response, dict)
        assert response['statusCode'] == 200

    def test_invalid_body_validation(self, handler, mocker):
        response = handler({'body': '{.x'}, None)
        assert isinstance(response, dict)
        assert response['statusCode'] == 400
        assert response['body'] == '{"errors": [{"body": ["Invalid JSON input."]}]}'
