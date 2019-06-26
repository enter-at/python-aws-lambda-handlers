import json
from typing import Dict, Union

import pytest

from lambda_handlers.formatters import (
    FormattingError,
    input_format,
    output_format,
)


@pytest.fixture
def data_sample() -> Dict[str, Union[str, int, bool]]:
    return {
        'name': 'Peter',
        'score': 100,
        'valid': True,
    }


class TestInputFormatJSON:

    def test_valid(self, data_sample):
        assert data_sample == input_format.json(json.dumps(data_sample))

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

    def test_valid(self, data_sample):
        assert json.dumps(data_sample) == output_format.json(data_sample)

    def test_data_sample(self, data_sample):
        content = json.dumps(data_sample)
        assert json.dumps(content) == output_format.json(content)

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
