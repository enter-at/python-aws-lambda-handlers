"""A handler for AWS events with validation and formatting."""

from lambda_handlers import formatters
from lambda_handlers.formatters import Format
from lambda_handlers.handlers.lambda_handler import LambdaHandler
from lambda_handlers.handlers.mixins.formatting_mixin import FormattingMixin


class EventHandler(LambdaHandler, FormattingMixin):
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
    """

    def __init__(self, input_format=None, output_format=None):
        self._input_format: Format = input_format or formatters.input_format.json
        self._output_format: Format = output_format or formatters.output_format.json

    def before(self, event, context):
        """Event hook called before the handler. It formats and validates `event`."""
        return self.format_input(event), context

    def after(self, result):
        """Event method called after the handler. It formats and validates `result`."""
        return self.format_output(result)
