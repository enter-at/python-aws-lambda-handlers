from typing import Any, Dict, List, Tuple

from lambda_handlers.errors import LambdaError
from lambda_handlers.validators import Validator

try:
    import marshmallow
except ImportError:
    marshmallow = None

NO_FIELD_NAME = '__no_field_name__'


class MarshmallowValidator(Validator):

    def validate(self, instance, schema: marshmallow.Schema) -> Tuple[Any, List[Any]]:
        if not marshmallow:
            raise LambdaError('Required marshmallow dependency not found.')

        result = schema.load(instance)
        return result.data, result.errors

    def format_errors(self, errors) -> List[Dict[str, Any]]:
        exception = marshmallow.ValidationError(errors)
        field_errors = exception.normalized_messages(no_field_name=NO_FIELD_NAME)
        if not field_errors.get(NO_FIELD_NAME) and len(field_errors) == 1:
            return []
        return [{field: errors} for field, errors in field_errors.items()]
