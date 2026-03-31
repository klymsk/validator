import pytest
from parser.data_parser import DataParser
from exceptions.custom_exceptions import ParserError
from unittest.mock import mock_open, patch


def test_valid_json():
    mock_data = '{"name": "Alex"}'

    with patch("builtins.open", mock_open(read_data=mock_data)):
        parser = DataParser("fake.json")
        result = parser.parse()

        assert result["name"] == "Alex"


def test_invalid_json():
    mock_data = '{name: Alex}'  

    with patch("builtins.open", mock_open(read_data=mock_data)):
        parser = DataParser("fake.json")

        with pytest.raises(ParserError):
            parser.parse()