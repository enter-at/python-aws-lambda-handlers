class LambdaError(Exception):
    def __init__(self, description):
        self.description = description


class BadRequestError(LambdaError):
    pass


class ForbiddenError(LambdaError):
    pass


class InternalServerError(LambdaError):
    pass


class NotFoundError(LambdaError):
    pass


class ValidationError(LambdaError):
    pass


class FormattingError(LambdaError):
    pass


class RequestValidationError(ValidationError):
    pass


class ResponseValidationError(ValidationError):
    pass
