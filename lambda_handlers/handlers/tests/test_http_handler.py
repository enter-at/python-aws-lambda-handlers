import pytest
from marshmallow import Schema, fields

from lambda_handlers import validators
from lambda_handlers.handlers import http_handler
from lambda_handlers.response import cors
from lambda_handlers.formatters.format import format
from lambda_handlers.response.response_builder import no_content


class TestHTTPHandlerDefaults:

    @pytest.fixture
    def handler(self):
        @http_handler()
        def handler(event, context):
            return {'user_id': 12}

        return handler

    def test_empty_body_validation(self, handler):
        response = handler({}, None)
        assert isinstance(response, dict)
        assert response['statusCode'] == 200

    def test_invalid_body_validation(self, handler):
        response = handler({'body': '{.x'}, None)
        assert isinstance(response, dict)
        assert response['statusCode'] == 400
        assert response['body'] == '{"errors": [{"body": ["Invalid JSON input."]}]}'

    def test_handler_response(self, handler):
        response = handler({}, None)
        assert isinstance(response, dict)
        assert response['statusCode'] == 200
        assert response['body'] == '{"user_id": 12}'
        assert response['headers'] == {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Credentials': True,
            'Access-Control-Allow-Origin': '*',
        }


@format('application/text+piped')
def pipe_input(content):
    items = content.split('|')
    return dict(zip(items[::2], items[1::2]))


@format('application/text+piped')
def pipe_output(content):
    content_items = [
        item for pairs in list(content.items())
        for item in pairs
    ]
    return '|'.join(content_items)


class TestHTTPHandlerCustomBodyFormat:

    @pytest.fixture
    def handler(self):
        @http_handler(
            input_format=pipe_input,
        )
        def handler(event, context):
            return event['body']

        return handler

    def test_custom_body_formatting(self, handler):
        event = {'body': 'user_id|peter'}
        response = handler(event, None)
        assert isinstance(response, dict)
        assert response['statusCode'] == 200
        assert response['body'] == '{"user_id": "peter"}'


class TestHTTPHandlerCORS:

    @pytest.fixture
    def handler(self):
        @http_handler(
            cors=cors(origin='localhost', credentials=False),
        )
        def handler(event, context):
            return event

        return handler

    def test_custom_cors_headers(self, handler):
        response = handler({}, None)
        assert isinstance(response, dict)
        assert response['statusCode'] == 200
        assert response['headers'] == {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'localhost',
        }


class TestHTTPHandlerCustomOutputFormat:

    @pytest.fixture
    def handler(self):
        @http_handler(
            output_format=pipe_output,
        )
        def handler(event, context):
            return {'user_id': 'peter'}

        return handler

    def test_custom_output_format(self, handler):
        response = handler({}, None)
        assert isinstance(response, dict)
        assert response['statusCode'] == 200
        assert response['body'] == 'user_id|peter'

        assert 'Content-Type' in response['headers']
        assert response['headers']['Content-Type'] == 'application/text+piped'


class TestHTTPHandlerOutputFormatNoBodyDefault:

    @pytest.fixture
    def handler(self):
        @http_handler()
        def handler(event, context):
            return None

        return handler

    def test_format_no_body(self, handler):
        response = handler({}, None)
        assert isinstance(response, dict)
        assert response['statusCode'] == 204
        assert 'body' not in response


class TestHTTPHandlerOutputFormatNoBody:

    @pytest.fixture
    def handler(self):
        @http_handler()
        def handler(event, context):
            return no_content()

        return handler

    def test_format_no_body(self, handler):
        response = handler({}, None)
        assert isinstance(response, dict)
        assert response['statusCode'] == 204
        assert 'body' not in response


class TestHTTPHandlerCustomMarshmallowValidator:

    @pytest.fixture
    def handler(self):
        class UserSchema(Schema):
            user_id = fields.Integer(required=True)

        class ResponseSchema(Schema):
            body = fields.Nested(UserSchema, required=True)
            headers = fields.Dict(required=True)
            statusCode = fields.Integer(required=True)

        @http_handler(
            validator=validators.http.marshmallow(body=UserSchema(), response=ResponseSchema()),
        )
        def handler(event, context):
            return event['body']

        return handler

    @pytest.mark.parametrize(
        'body,expected',
        [
            ('{"user_id": 1}', '{"user_id": 1}'),
            ('{"user_id": "1"}', '{"user_id": 1}'),
        ],
    )
    def test_custom_body_validator(self, handler, body, expected):
        event = {'body': body}
        response = handler(event, None)
        assert isinstance(response, dict)
        assert response['statusCode'] == 200
        assert response['body'] == expected
