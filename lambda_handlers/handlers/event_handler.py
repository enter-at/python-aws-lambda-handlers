"""A handler for AWS events with validation and formatting."""

from lambda_handlers import formatters
from lambda_handlers.formatters import Format
from lambda_handlers.validators.validator import Validator
from lambda_handlers.handlers.lambda_handler import LambdaHandler
from lambda_handlers.handlers.mixins.formatting_mixin import FormattingMixin
from lambda_handlers.handlers.mixins.validation_mixin import ValidationMixin


class EventHandler(LambdaHandler, ValidationMixin, FormattingMixin):
    """
    Decorator class to facilitate the definition of AWS Lambda event handlers.

    Features:
        - input validation,
        - output formatting.

    Parameters
    ----------
    input_format: Format, optional
        Format to parse the input event.
        Default:  formatters.input_format.json.

    output_format: Format, optional
        Format to format the output body from the return value of the handler function.
        Default:  formatters.output_format.json.

    validator: Callable, optional
        A callable or schema definition to validate: event, and result.
    """

    def __init__(self, input_format=None, output_format=None, validator=None):
        self._validator: Validator = validator
        self._input_format: Format = input_format or formatters.input_format.json
        self._output_format: Format = output_format or formatters.output_format.json

    @property
    def validator(self) -> Validator:
        """The event and result validator."""
        return self._validator

    def before(self, event, context):
        """Event hook called before the handler. It formats and validates `event`."""
        return self.validate_event(self.format_input(event), context)

    def after(self, result):
        """Event method called after the handler. It formats and validates `result`."""
        return self.validate_result(self.format_output(result))
