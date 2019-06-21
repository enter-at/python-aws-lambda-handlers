from typing import Any, Dict, List, Tuple

from lambda_handlers.errors import LambdaError
from lambda_handlers.validators import Validator

try:
    import marshmallow
except ImportError:
    marshmallow = None

NO_FIELD_NAME = 'errors'


class MarshmallowValidator(Validator):

    def validate(self, instance, schema) -> Tuple[Any, List[Any]]:
        if not marshmallow:
            raise LambdaError('Required marshmallow dependency not found.')

        result = schema.load(instance)
        return result.data, result.errors

    def format_error(self, errors) -> List[Dict[str, Any]]:
        exception = marshmallow.ValidationError(errors)
        return exception.normalized_messages(no_field_name=NO_FIELD_NAME).get(NO_FIELD_NAME, None)
