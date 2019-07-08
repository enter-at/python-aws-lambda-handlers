from lambda_handlers import formatters
from lambda_handlers.validators import Validator
from lambda_handlers.handlers.lambda_handler import LambdaHandler
from lambda_handlers.handlers.mixins.formatting_mixin import FormattingMixin
from lambda_handlers.handlers.mixins.validation_mixin import ValidationMixin


class EventHandler(LambdaHandler, ValidationMixin, FormattingMixin):
    """
    Decorator class to facilitate the definition of AWS Lambda handlers with:
        - input validation,
        - output formatting.

    Parameters
    ----------
    input_format: Callable
        Formatter callable to parse the input event.

    output_format: Callable
        Formatter callable to format the output body from the return value of the handler function.

    validator:
        A callable or schema definition to validate: event, and resulr.
    """

    def __init__(self, input_format=None, output_format=None, validator=None):
        self._validator: Validator = validator
        self._input_format = input_format or formatters.input_format.json
        self._output_format = output_format or formatters.output_format.json

    @property
    def validator(self):
        return self._validator

    def before(self, event, context):
        return self.validate_event(self.format_input(event), context)

    def after(self, result):
        return self.validate_result(self.format_output(result))
