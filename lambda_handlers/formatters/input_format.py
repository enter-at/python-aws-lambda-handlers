"""Input formatter objects."""

import json as jsonlib
from typing import Any

from lambda_handlers.errors import FormatError

from .format import format


@format('application/json')
def json(content) -> Any:
    """JSON input formatter."""
    try:
        return jsonlib.loads(content)
    except jsonlib.decoder.JSONDecodeError as error:
        raise FormatError('Invalid JSON input.') from error
    except TypeError as error:
        raise FormatError('Unexpected type for JSON input.') from error
