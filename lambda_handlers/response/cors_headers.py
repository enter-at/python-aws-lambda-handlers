from typing import Dict, Union


class CorsHeaders:
    def __init__(self, origin=None, credentials=None):
        self.origin = origin or '*'
        self.credentials = credentials

    def create_headers(self) -> Dict[str, Union[str, bool]]:
        headers = {
            'Access-Control-Allow-Origin': self.origin
        }
        if self.credentials:
            headers['Access-Control-Allow-Credentials'] = True

        return headers
