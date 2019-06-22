from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Callable

from lambda_handlers.errors import (
    RequestValidationError,
    ResponseValidationError
)


class Validator(ABC):

    def __init__(self, path=None, query=None, body=None, request=None, response=None):
        self._path_parameters_schema = path
        self._query_string_parameters_schema = query
        self._body_schema = body
        self._request_schema = request
        self._response_schema = response

    def validate_request(self, event, context) -> Tuple[Any, Any]:
        if self._request_schema:
            data, errors = self.validate(event, self._request_schema())
        else:
            data, errors = self._validate_request_contexts(event, context)

        if errors:
            description = self.format_errors(errors)
            raise RequestValidationError(description)

        return data, context

    def validate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        if not self._response_schema:
            return response

        data, errors = self.validate(response, self._response_schema())

        if errors:
            description = self.format_errors(errors)
            raise ResponseValidationError(description)

        return data

    def _validate_request_contexts(self, event, context) -> Tuple[Dict[str, Any], List[Any]]:
        contexts = {
            'pathParameters': self._path_parameters_schema,
            'queryStringParameters': self._query_string_parameters_schema,
            'body': self._body_schema
        }
        return self._validate_many(event, {key: schema() for key, schema in contexts.items() if schema})

    def _validate_many(self, target: Dict[str, Any], definitions: Dict[str, Callable]) -> Tuple[Dict[str, Any], List[Any]]:
        cumulative_errors = []
        transformed_data = {}

        for key, schema in definitions.items():
            data, errors = self.validate(target.get(key, {}), schema)
            if errors:
                cumulative_errors.append(errors)
            elif key in target:
                transformed_data[key] = data

        return transformed_data, cumulative_errors

    @abstractmethod
    def validate(self, instance: Any, schema: Any) -> Tuple[Any, List[Any]]:
        pass

    @abstractmethod
    def format_errors(self, errors: List[Any]) -> List[Dict[str, Any]]:
        pass
