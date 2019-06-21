from typing import Any, Dict, List, Tuple

from marshmallow import ValidationError
from lambda_handlers.validators import Validator

NO_FIELD_NAME = 'errors'


class MarshmallowValidator(Validator):

    def validate(self, instance, schema) -> Tuple[Any, List[Any]]:
        result = schema.load(instance)
        return result.data, result.errors

    def format_error(self, errors) -> List[Dict[str, Any]]:
        exception = ValidationError(errors)
        return exception.normalized_messages(no_field_name=NO_FIELD_NAME).get(NO_FIELD_NAME, None)
