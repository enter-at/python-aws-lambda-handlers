from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Union, Callable
from collections import defaultdict

from lambda_handlers.errors import EventValidationError, ResultValidationError


class Validator(ABC):

    def __init__(
        self,
        input_schema=None,
        output_schema=None,
    ):
        self._input_schema = input_schema
        self._output_schema = output_schema

    @property
    def schemas(self) -> Dict[str, Any]:
        return {}

    def validate_event(self, event, context) -> Tuple[Any, Any]:
        if self._input_schema:
            data, errors = self.validate(event, self._input_schema)

            if errors:
                description = self.format_errors(errors)
                raise EventValidationError(description)

            return data, context

        return self._validate_event_contexts(event, context)

    def validate_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        if not self._output_schema:
            return result

        data, errors = self.validate(result, self._output_schema)

        if errors:
            description = self.format_errors(errors)
            raise ResultValidationError(description)

        return data

    def _validate_event_contexts(self, event, context) -> Tuple[Dict[str, Any], List[Any]]:

        transformed_data, errors = self._validate_many(
            event,
            {key: schema for key, schema in self.schemas.items() if schema},
        )

        if errors:
            raise EventValidationError(
                [{key: self.format_errors(error)} for key, error in errors.items()],
            )

        return transformed_data, context

    def _validate_many(
        self,
        target: Dict[str, Any],
        definitions: Dict[str, Callable],
    ) -> Tuple[Dict[str, Any], Dict[str, List[Any]]]:

        cumulative_errors: Dict[str, List[Any]] = defaultdict(list)
        transformed_data = {}

        for key, schema in definitions.items():
            data, errors = self.validate(target.get(key, {}), schema)
            if errors:
                entry = cumulative_errors[key]
                if not isinstance(errors, list):
                    errors = [errors]
                entry.extend(errors)

            elif key in target:
                transformed_data[key] = data

        return transformed_data, cumulative_errors

    @abstractmethod
    def validate(self, instance: Any, schema: Any) -> Tuple[Any, Union[Dict[str, Any], List[Any]]]:
        pass

    @abstractmethod
    def format_errors(self, errors: Union[Dict[str, Any], List[Any]]) -> List[Dict[str, Any]]:
        pass
