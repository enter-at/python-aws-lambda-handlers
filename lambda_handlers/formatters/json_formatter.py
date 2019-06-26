import json

from ..errors import FormattingError


def from_json(content):
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError as error:
        raise FormattingError('Invalid JSON input.') from error
    except TypeError as error:
        raise FormattingError('Unexpected type for JSON input.') from error


def to_json(content):
    return json.dumps(content)
