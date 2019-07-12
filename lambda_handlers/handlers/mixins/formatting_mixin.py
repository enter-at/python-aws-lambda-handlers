
class FormattingMixin:
    """A mixin for formatting."""
    def format_input(self, event):
        return self._input_format.format(event)

    def format_output(self, result):
        return self._output_format.format(result)
