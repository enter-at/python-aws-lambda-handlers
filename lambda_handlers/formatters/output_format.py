"""Output formatter objects."""

import json as jsonlib

from .format import format


@format('application/json')
def json(content) -> str:
    """JSON ouput formatter."""
    return jsonlib.dumps(content)
