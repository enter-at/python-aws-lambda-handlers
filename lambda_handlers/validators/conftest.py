"""Test utilities and fixtures."""

from typing import Any, Dict, List
from collections import defaultdict

import pytest


def builder(base_class):
    """Return a simple Validator for testing."""
    class SimpleSchemaValidator(base_class):

        def validate(self, instance: Any, schema: dict):
            cumulative_errors = []

            for key, type_def in schema.items():
                if key not in instance:
                    cumulative_errors.append({key: 'missing'})
                elif isinstance(type_def, dict):
                    _, errors = self.validate(instance[key], type_def)
                    if errors:
                        cumulative_errors.extend(errors)
                elif type(instance[key]) != type_def:
                    cumulative_errors.append({key: f'{instance[key]} is not of type {type_def}'})

            return instance, cumulative_errors

        def format_errors(self, errors) -> List[Dict[str, Any]]:
            path_errors: Dict[str, List[str]] = defaultdict(list)
            for error in errors:
                for key, value in error.items():
                    path_errors[key].append(value)
            return [{path: messages} for path, messages in path_errors.items()]

    return SimpleSchemaValidator


@pytest.fixture
def simple_schema_validator_builder():
    """Return the simple Validator for testing builder function."""
    return builder
