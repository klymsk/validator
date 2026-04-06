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

# Схема парсер
class TestSchemaParser:
    def test_simple_schema(self):
        parser = SchemaParser()
        schema_text = """
        type User {
            name: string
            age: integer
        }
        """
        result = parser.parse(schema_text)

        assert "User" in result
        assert "name" in result["User"]
        assert "age" in result["User"]
        assert result["User"]["name"]["type"] == str
        assert result["User"]["age"]["type"] == int

    def test_schema_with_constraints(self):
        parser = SchemaParser()
        schema_text = """
        type User {
            id: integer range(1, 9999)
            username: string length(3, 20)
        }
        """
        result = parser.parse(schema_text)

        user_schema = result["User"]
        # Перевіряємо числові обмеження
        assert user_schema["id"]["min"] == 1
        assert user_schema["id"]["max"] == 9999
        # Перевіряємо обмеження на довжину
        assert user_schema["username"]["min_length"] == 3
        assert user_schema["username"]["max_length"] == 20

    # Регулярний вираз
    def test_schema_with_regex(self):
        parser = SchemaParser()
        schema_text = """
        type User {
            email: string regex(".*@.*")
        }
        """
        result = parser.parse(schema_text)

        assert result["User"]["email"]["regex"] == ".*@.*"

    # Коректність схеми
    def test_invalid_schema_missing_colon(self):
        parser = SchemaParser()
        schema_text = """
        type User {
            name string
        }
        """

        with pytest.raises(SchemaError):
            parser.parse(schema_text)


    def test_empty_schema(self):
        parser = SchemaParser()
        schema_text = ""
        result = parser.parse(schema_text)

        assert result == {}

    def test_schema_with_whitespace(self):
        parser = SchemaParser()
        schema_text = """


        type User {
            name: string
        }


        """
        result = parser.parse(schema_text)

        assert "User" in result
        assert result["User"]["name"]["type"] == str