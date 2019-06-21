from typing import Dict, Union


class Cors:
    def __init__(self, origin=None, credentials=None):
        self.origin = origin
        self.credentials = credentials

    def create_headers(self) -> Dict[str, Union[str, bool]]:
        headers = {}
        headers['Access-Control-Allow-Origin'] = self.origin or '*'
        if self.credentials:
            headers['Access-Control-Allow-Credentials'] = True
        return headers
