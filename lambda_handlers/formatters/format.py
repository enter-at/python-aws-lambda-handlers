"""Base formatter classes."""

from typing import Callable
from dataclasses import dataclass


@dataclass
class Format:
    """Format class to hold output and input formats."""

    content_type: str
    format: Callable


class format:
    """Decorator class to specify formatters."""

    def __init__(self, content_type: str):
        self.content_type = content_type

    def __call__(self, fn):
        """Decorate functions."""
        return Format(
            content_type=self.content_type,
            format=fn,
        )
