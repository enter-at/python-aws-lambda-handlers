"""A mixin for event and result data validation."""

from abc import abstractmethod
from typing import Any, Dict


class ValidationMixin:
    """A mixin for event and result data validation."""

    @property
    @abstractmethod
    def validator(self):
        """Return the validator for events and results."""
        pass

    def validate_event(self, event):
        """Validate the event with `self.validator`, return event and context."""
        if self.validator:
            transformed_event = self.validator.validate_event(event)
            event.update(transformed_event)
        return event

    def validate_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and return the result with `self.validator`."""
        if self.validator:
            return self.validator.validate_result(result)
        return result
