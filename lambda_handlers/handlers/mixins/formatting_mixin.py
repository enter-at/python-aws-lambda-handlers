"""Formatting mixin."""


class FormattingMixin:
    """A mixin to use Formatters."""

    def format_input(self, event):
        """Parse `event` and return the result."""
        return self._input_format.format(event)

    def format_output(self, result):
        """Return a formatted str from the `result`."""
        return self._output_format.format(result)
