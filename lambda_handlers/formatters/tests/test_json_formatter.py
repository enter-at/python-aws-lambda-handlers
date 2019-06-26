import pytest

from lambda_handlers.formatters import (
    FormattingError,
    input_format,
    output_format,
)


class TestInputFormatJSON:

    def test_valid_string_dict(self):
        assert {'name': 'Peter'} == input_format.json('{"name": "Peter"}')

    def test_valid_int_dict(self):
        assert {'score': 100} == input_format.json('{"score": 100}')

    def test_valid_bool_dict(self):
        assert {'is_valid': True} == input_format.json('{"is_valid": true}')

    def test_valid_nested_dict(self):
        assert {'person': {'name': 'Peter'}} == input_format.json('{"person": {"name": "Peter"}}')

    def test_empty_content(self):
        assert {} == input_format.json('{}')

    def test_random_string(self):
        with pytest.raises(FormattingError, match='Invalid JSON input.'):
            input_format.json('sadfawfopq2yr923')

    def test_empty_string(self):
        with pytest.raises(FormattingError, match='Invalid JSON input.'):
            input_format.json('')

    def test_none(self):
        with pytest.raises(FormattingError, match='Unexpected type for JSON input.'):
            input_format.json(None)


class TestOutputFormatJSON:

    def test_valid_string_dict(self):
        assert '{"name": "Peter"}' == output_format.json({'name': 'Peter'})

    def test_valid_int_dict(self):
        assert '{"score": 100}' == output_format.json({'score': 100})

    def test_valid_bool_dict(self):
        assert '{"is_valid": true}' == output_format.json({'is_valid': True})

    def test_valid_nested_dict(self):
        assert '{"person": {"name": "Peter"}}' == output_format.json({'person': {'name': 'Peter'}})

    def test_empty_content(self):
        assert '{}' == output_format.json({})

    def test_random_string(self):
        assert '"sadfawfopq2yr923"' == output_format.json('sadfawfopq2yr923')

    def test_empty_string(self):
        assert '""' == output_format.json('')

    def test_none(self):
        assert 'null' == output_format.json(None)

    def test_bool(self):
        assert 'true' == output_format.json(True)

    def test_int(self):
        assert '42' == output_format.json(42)
