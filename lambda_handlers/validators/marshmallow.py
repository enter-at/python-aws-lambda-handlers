import marshmallow

from lambda_handlers.errors import ValidationError


class Validator:

    def __init__(self, path=None, query=None, body=None):
        self._path_parameters_schema = path
        self._query_string_parameters_schema = query
        self._body_schema = body

    def __call__(self, event, context):
        errors = []

        def _validate(key, schema):
            result = schema.load(event.get(key, {}))
            if result.errors:
                errors.append(result.errors)
            elif key in event:
                event[key].update(result.data)

        if self._path_parameters_schema:
            _validate('pathParameters', self._path_parameters_schema())

        if self._query_string_parameters_schema:
            _validate('queryStringParameters', self._query_string_parameters_schema())

        if self._body_schema:
            _validate('body', self._body_schema())

        if errors:
            exception = marshmallow.ValidationError(errors)
            description = exception.normalized_messages(no_field_name='errors')['errors']
            raise ValidationError(description)
