import json
from typing import Dict, Union

import pytest

from lambda_handlers.formatters import InputFormat, OutputFormat


@pytest.fixture
def data_sample() -> Dict[str, Union[str, int, bool]]:
    return {
        'name': 'Peter',
        'score': 100,
        'valid': True,
    }


class TestInputFormatJSON:

    def test_valid(self, data_sample):
        assert data_sample == InputFormat.json(json.dumps(data_sample))

    def test_empty_content(self):
        assert {} == InputFormat.json('{}')

    def test_random_string(self):
        with pytest.raises(json.decoder.JSONDecodeError, match='Expecting value:'):
            InputFormat.json('sadfawfopq2yr923')

    def test_empty_string(self):
        with pytest.raises(json.decoder.JSONDecodeError, match='Expecting value:'):
            InputFormat.json('')

    def test_none(self):
        with pytest.raises(TypeError, match='the JSON object must be'):
            InputFormat.json(None)


class TestOutputFormatJSON:

    def test_valid(self, data_sample):
        assert json.dumps(data_sample) == OutputFormat.json(data_sample)

    def test_empty_content(self):
        assert '{}' == OutputFormat.json({})

    def test_random_string(self):
        assert '"sadfawfopq2yr923"' == OutputFormat.json('sadfawfopq2yr923')

    def test_empty_string(self):
        assert '""' == OutputFormat.json('')

    def test_none(self):
        assert 'null' == OutputFormat.json(None)

    def test_bool(self):
        assert 'true' == OutputFormat.json(True)

    def test_int(self):
        assert '42' == OutputFormat.json(42)
