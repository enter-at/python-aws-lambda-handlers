class FormattingMixin:

    def format_input(self, event):
        return self._input_format(event)

    def format_output(self, result):
        return self._output_format(result)
