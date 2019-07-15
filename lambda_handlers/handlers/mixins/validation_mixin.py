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

    def validate_event(self, event, context):
        """Validate the event with `self.validator`, return event and context."""
        if self.validator:
            transformed_event, transformed_context = self.validator.validate_event(event, context)
            event.update(transformed_event)
            if context is not None:
                context.update(transformed_context)
        return event, context

    def validate_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and return the result with `self.validator`."""
        if self.validator:
            return self.validator.validate_result(result)
        return result
