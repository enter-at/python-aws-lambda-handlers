import pytest

from lambda_handlers.response.cors_headers import CorsHeaders


class TestCorsHeaders:

    @pytest.mark.parametrize(
        'origin, credentials, expected',
        [
            (
                None,
                None,
                {'Access-Control-Allow-Origin': '*'},
            ),
            (
                None,
                False,
                {'Access-Control-Allow-Origin': '*'},
            ),
            (
                None,
                True,
                {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
            ),
            (
                'https://developer.mozilla.org',
                None,
                {'Access-Control-Allow-Origin': 'https://developer.mozilla.org'},
            ),
            (
                'https://developer.mozilla.org',
                True,
                {
                    'Access-Control-Allow-Origin': 'https://developer.mozilla.org',
                    'Access-Control-Allow-Credentials': True,
                },
            ),
        ],
    )
    def test_create_headers(self, origin, credentials, expected):
        subject = CorsHeaders(origin=origin, credentials=credentials)
        assert subject.create_headers() == expected
