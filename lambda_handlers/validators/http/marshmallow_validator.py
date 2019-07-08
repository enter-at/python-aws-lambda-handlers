from lambda_handlers.validators.http.http_validator import HttpValidator
from lambda_handlers.validators.marshmallow_validator import (
    MarshmallowValidator,
)


class HttpMarshmallowValidator(MarshmallowValidator, HttpValidator):
    pass
