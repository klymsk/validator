import pytest
from parser.data_parser import DataParser
from parser.schema_parser import SchemaParser
from exceptions.custom_exceptions import ParserError, SchemaError


# Дата парсер
class TestDataParser:
    def test_valid_json_simple(self):
        parser = DataParser()
        data = '{"name": "John", "age": 25}'
        result = parser.parse(data)

        assert result["name"] == "John"
        assert result["age"] == 25

    # Коректність лапок
    def test_invalid_json_missing_quote(self):
        parser = DataParser()
        data = '{name: "John"}'

        with pytest.raises(ParserError) as exc_info:
            parser.parse(data)

        assert "JSON" in str(exc_info.value)

    # Коректність дужок
    def test_invalid_json_missing_brace(self):
        parser = DataParser()
        data = '{"name": "John"'

        with pytest.raises(ParserError):
            parser.parse(data)


    def test_json_with_null(self):
        parser = DataParser()
        data = '{"field": null}'
        result = parser.parse(data)

        assert result["field"] is None

    # Числові типи
    def test_json_with_numbers(self):
        parser = DataParser()
        data = '{"integer": 42, "float": 3.14, "negative": -10}'
        result = parser.parse(data)

        assert result["integer"] == 42
        assert result["float"] == 3.14
        assert result["negative"] == -10