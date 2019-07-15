"""A validator for Marshmallow Schemas."""

from typing import Any, Dict, List, Tuple, Union

from lambda_handlers.errors import LambdaError
from lambda_handlers.validators.validator import Validator

try:
    import marshmallow
except ImportError:
    marshmallow = None

NO_FIELD_NAME = '__no_field_name__'


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

        result = schema.load(instance)
        return result.data, result.errors

    def format_errors(
        self,
        errors: Union[Dict[str, Any], List[Any]],
    ) -> List[Dict[str, Any]]:
        """Re-format the errors from Marshmallow."""
        exception = marshmallow.ValidationError(errors)
        field_errors = exception.normalized_messages(no_field_name=NO_FIELD_NAME)

        if NO_FIELD_NAME in field_errors and len(field_errors) == 1:
            entry = field_errors[NO_FIELD_NAME]
            return entry or []

        return [{field: errors} for field, errors in field_errors.items()]
