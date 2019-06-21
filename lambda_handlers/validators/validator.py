from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

from lambda_handlers.errors import ValidationError


class Validator(ABC):

    def __init__(self, path=None, query=None, body=None):
        self._path_parameters_schema = path
        self._query_string_parameters_schema = query
        self._body_schema = body

    def __call__(self, event, context):
        cumulative_errors = []

        def _validate(key, schema):
            data, errors = self.on_validate(event.get(key, {}), schema)
            if errors:
                cumulative_errors.append(errors)
            elif key in event:
                event[key].update(data)

        if self._path_parameters_schema:
            _validate('pathParameters', self._path_parameters_schema())

        if self._query_string_parameters_schema:
            _validate('queryStringParameters', self._query_string_parameters_schema())

        if self._body_schema:
            _validate('body', self._body_schema())

        if cumulative_errors:
            description = self.format_errors(cumulative_errors)
            raise ValidationError(description)

    @abstractmethod
    def validate(self, instance: Any, schema: Any) -> Tuple[Any, List[Any]]:
        pass

    @abstractmethod
    def format_errors(self, errors: List[Any]) -> List[Dict[str, Any]]:
        pass
