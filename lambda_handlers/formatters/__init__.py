from lambda_handlers.errors import FormattingError  # noqa
from lambda_handlers.formatters import json_formatter


class InputFormat:
    json = json_formatter.from_json


class OutputFormat:
    json = json_formatter.to_json


input_format = InputFormat
output_format = OutputFormat
