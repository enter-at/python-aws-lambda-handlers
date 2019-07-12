import pytest

from lambda_handlers.errors import FormatError
from lambda_handlers.formatters import input_format


class TestInputFormatJSON:

    def test_valid_string_dict(self):
        assert {'name': 'Peter'} == input_format.json.format('{"name": "Peter"}')

    def test_valid_int_dict(self):
        assert {'score': 100} == input_format.json.format('{"score": 100}')

    def test_valid_bool_dict(self):
        assert {'is_valid': True} == input_format.json.format('{"is_valid": true}')

    def test_valid_nested_dict(self):
        assert {'person': {'name': 'Peter'}} == input_format.json.format('{"person": {"name": "Peter"}}')

    def test_empty_content(self):
        assert {} == input_format.json.format('{}')

    def test_random_string(self):
        with pytest.raises(FormatError, match='Invalid JSON input.'):
            input_format.json.format('sadfawfopq2yr923')

    def test_empty_string(self):
        with pytest.raises(FormatError, match='Invalid JSON input.'):
            input_format.json.format('')

    def test_none(self):
        with pytest.raises(FormatError, match='Unexpected type for JSON input.'):
            input_format.json.format(None)
