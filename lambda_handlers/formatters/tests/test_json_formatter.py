import json
from typing import Dict, Union

import pytest

from lambda_handlers.formatters import input_format, output_format


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
        with pytest.raises(json.decoder.JSONDecodeError, match=r'Expecting value: line 1 column 1 \(char 0\)'):
            input_format.json('sadfawfopq2yr923')

    def test_empty_string(self):
        with pytest.raises(json.decoder.JSONDecodeError, match=r'Expecting value: line 1 column 1 \(char 0\)'):
            input_format.json('')

    def test_none(self):
        with pytest.raises(TypeError, match='the JSON object must be str, bytes or bytearray, not NoneType'):
            input_format.json(None)


class TestOutputFormatJSON:

    def test_valid(self, data_sample):
        assert json.dumps(data_sample) == output_format.json(data_sample)

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
