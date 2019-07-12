"""CORS Headers for responses."""

from typing import Dict, Union


class CORSHeaders:
    """Return the data and the errors from validating `instance` against `schema`."""

    def __init__(self, origin: str = None, credentials: bool = False):
        self.origin = origin or '*'
        self.credentials = credentials

    def create_headers(self) -> Dict[str, Union[str, bool]]:
        """Return the CORS-related parts of the response header."""
        headers: Dict[str, Union[str, bool]] = {
            'Access-Control-Allow-Origin': self.origin,
        }
        if self.credentials:
            headers['Access-Control-Allow-Credentials'] = True

        return headers
