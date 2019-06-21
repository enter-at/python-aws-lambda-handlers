from typing import Any, Dict, List, Tuple
from collections import defaultdict

from jsonschema import Draft7Validator
from lambda_handlers.validators import Validator


class JSONSchemaValidator(Validator):

    def validate(self, instance, schema) -> Tuple[Any, List[Any]]:
        validator = Draft7Validator(schema)
        errors = sorted(validator.iter_errors(instance), key=lambda error: error.path)
        return instance, errors

    def format_error(self, errors) -> List[Dict[str, Any]]:
        path_errors: Dict[str, List[str]] = defaultdict(list)
        for error in errors:
            path_errors[error.path.pop()].append(error.message)

        return [{path: messages} for path, messages in path_errors.items()]
