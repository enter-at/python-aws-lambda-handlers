from lambda_handlers.formatters import output_format


class TestOutputFormatJSON:

    def test_valid_string_dict(self):
        assert '{"name": "Peter"}' == output_format.json.format({'name': 'Peter'})

    def test_valid_int_dict(self):
        assert '{"score": 100}' == output_format.json.format({'score': 100})

    def test_valid_bool_dict(self):
        assert '{"is_valid": true}' == output_format.json.format({'is_valid': True})

    def test_valid_nested_dict(self):
        assert '{"person": {"name": "Peter"}}' == output_format.json.format({'person': {'name': 'Peter'}})

    def test_empty_content(self):
        assert '{}' == output_format.json.format({})

    def test_random_string(self):
        assert '"sadfawfopq2yr923"' == output_format.json.format('sadfawfopq2yr923')

    def test_empty_string(self):
        assert '""' == output_format.json.format('')

    def test_none(self):
        assert 'null' == output_format.json.format(None)

    def test_bool(self):
        assert 'true' == output_format.json.format(True)

    def test_int(self):
        assert '42' == output_format.json.format(42)
