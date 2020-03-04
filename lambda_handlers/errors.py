"""Module Exception classes declarations."""


class LambdaError(Exception):
    """Base exception class."""

    def __init__(self, description):
        self.description = description


class BadRequestError(LambdaError):
    """Bad request error."""

    pass


class ForbiddenError(LambdaError):
    """Forbidden error."""

    pass


class InternalServerError(LambdaError):
    """Internal server error."""

    pass


class NotFoundError(LambdaError):
    """Not found error."""

    pass


class EventValidationError(LambdaError):
    """Event validation error."""

    pass


class FormatError(LambdaError):
    """Formatting error."""

    pass
