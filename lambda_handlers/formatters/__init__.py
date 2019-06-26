from . import json_formatter
from ..errors import FormattingError  # noqa


class InputFormat:
    json = json_formatter.from_json


class OutputFormat:
    json = json_formatter.to_json


input_format = InputFormat
output_format = OutputFormat
