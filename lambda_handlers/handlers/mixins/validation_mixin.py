from abc import abstractmethod
from typing import Any, Dict


class ValidationMixin:

    @property
    @abstractmethod
    def validator(self):
        pass

    def validate_event(self, event, context):
        if self.validator:
            transformed_event, transformed_context = self.validator.validate_event(event, context)
            event.update(transformed_event)
            if context is not None:
                context.update(transformed_context)
        return event, context

    def validate_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        if self.validator:
            return self.validator.validate_result(result)
        return result
