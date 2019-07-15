"""Base class for Validators."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Union
from collections import defaultdict

from lambda_handlers.errors import EventValidationError, ResultValidationError


class Validator(ABC):
    """Base class for Validators.

    Parameters
    ----------
    input_schema:
        The schema to validate the input data: event and context.

    output_schema:
        The schema to validate the output data: handler's return value.
    """

    def __init__(
        self,
        input_schema=None,
        output_schema=None,
    ):
        self._input_schema = input_schema
        self._output_schema = output_schema

    @property
    def schemas(self) -> Dict[str, Any]:
        """The schemas for each section of context."""
        return {}

    def validate_event(self, event: Any, context: Any) -> Tuple[Any, Any]:
        """Validate `event` against the input_schema.

        Parameters
        ----------
        event:
            The event data object.

        context:
            The context data object.

        Returns
        -------
        data: Any
            The same as `event` after passing through validation.

        context: Any
            The validated context in case there is no input_schema, but
            the schemas function is used.

        Raises
        ------
        ResultValidationError:
            In case of validation errors.
        """
        if self._input_schema:
            data, errors = self.validate(event, self._input_schema)

            if errors:
                description = self.format_errors(errors)
                raise EventValidationError(description)

            return data, context

        return self._validate_event_contexts(event, context)

    def validate_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate `result` against the output_schema.

        Parameters
        ----------
        result: Dict[str, Any]
            The data object.

        Returns
        -------
        data: Dict[str, Any]
            The same as `result`.

        Raises
        ------
        ResultValidationError:
            In case of validation errors.
        """
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
        definitions: Dict[str, Any],
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
        """Validate `instance` against `schema`.

        Abstract method to be replaced when the specific validation method is chosen.

        Parameters
        ----------
        instance:
            The data object to be validated.

        schema:
            The data schema definition.

        Returns
        -------
        transformed_data: Any
            The result validated data.

        errors: Union[Dict[str, Any], List[Any]]
            The validation errors.
        """
        pass

    @abstractmethod
    def format_errors(self, errors: Union[Dict[str, Any], List[Any]]) -> List[Dict[str, Any]]:
        """Re-structure `errors` for output."""
        pass
