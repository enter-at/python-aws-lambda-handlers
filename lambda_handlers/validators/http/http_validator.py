from typing import Any, Dict

from lambda_handlers.validators.validator import Validator


class HttpValidator(Validator):

    def __init__(self, path=None, query=None, body=None, request=None, response=None):
        super().__init__(input_schema=request, output_schema=response)
        self._schemas = {
            'pathParameters': path,
            'queryStringParameters': query,
            'body': body,
        }

    @property
    def schemas(self) -> Dict[str, Any]:
        return self._schemas
