"""A AWS HTTP event validator that uses Marshmallow."""

from lambda_handlers.validators.http.http_validator import HttpValidator
from lambda_handlers.validators.marshmallow_validator import (
    MarshmallowValidator,
)


class HttpMarshmallowValidator(MarshmallowValidator, HttpValidator):
    """A AWS HTTP event validator that uses Marshmallow."""

    pass
