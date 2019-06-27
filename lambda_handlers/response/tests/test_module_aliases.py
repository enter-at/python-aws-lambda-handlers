from typing import Any, Type

import pytest

import lambda_handlers.response as subject
from lambda_handlers.response.cors_headers import CorsHeaders


class TestModuleAliases:

    @pytest.mark.parametrize(
        'alias, target',
        [
            ('cors', CorsHeaders),
        ],
    )
    def test_alias(self, alias: str, target: Type[Any]):
        assert hasattr(subject, alias)
        assert getattr(subject, alias) == target
