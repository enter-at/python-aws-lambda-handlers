"""CORS Headers for responses."""

from lambda_handlers.types import Headers


class CORSHeaders:
    """Return the data and the errors from validating `instance` against `schema`."""

    def __init__(self, origin: str = None, credentials: bool = False):
        self.origin = origin or '*'
        self.credentials = credentials

    def create_headers(self) -> Headers:
        """Return the CORS-related parts of the response header."""
        headers: Headers = {
            'Access-Control-Allow-Origin': self.origin,
        }
        if self.credentials:
            headers['Access-Control-Allow-Credentials'] = True

        return headers
