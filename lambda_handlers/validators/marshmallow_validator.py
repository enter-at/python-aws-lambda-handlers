"""A validator for Marshmallow Schemas."""

from typing import Any, Dict, List, Tuple, Union

from lambda_handlers.errors import LambdaError
from lambda_handlers.validators.validator import Validator

try:
    import marshmallow
except ImportError:
    pass

NO_FIELD_NAME = '_schema'


class MarshmallowValidator(Validator):
    """A Validator that uses Marshmallow schemas."""

    def validate(
        self,
        instance: Any,
        schema: 'marshmallow.Schema',
    ) -> Tuple[Any, Union[Dict[str, Any], List[Any]]]:
        """Return the data and errors (if any) from validating `instance` against `schema`."""
        if not marshmallow:
            raise LambdaError('Required marshmallow dependency not found.')

        try:
            return schema.load(instance), []
        except marshmallow.ValidationError as error:
            return None, error.messages

    def format_errors(
        self,
        errors: Union[Dict[str, Any], List[Any]],
    ) -> List[Dict[str, Any]]:
        """Re-format the errors from Marshmallow."""
        exception = marshmallow.ValidationError(errors)
        field_errors = exception.normalized_messages()

        if NO_FIELD_NAME in field_errors and len(field_errors) == 1:
            entry = field_errors[NO_FIELD_NAME]
            return entry or []

        return [{field: errors} for field, errors in field_errors.items()]
