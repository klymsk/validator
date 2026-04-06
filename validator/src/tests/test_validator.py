import pytest
from exceptions.custom_exceptions import (
    ConstraintError,
    MissingFieldError,
    TypeMismatchError,
    ValidationError
)
from validator.validator import Validator


# Базові тести
class TestValidatorBasic:
    @pytest.fixture
    def simple_schema(self):
        return {
            "name": {"type": str},
            "age": {"type": int}
        }

    # Перевірка коректних даних
    def test_valid_data(self, simple_schema):
        validator = Validator(simple_schema)
        data = {"name": "John", "age": 25}

        assert validator.validate(data) is True

    # Наявність поля
    def test_missing_field(self, simple_schema):
        validator = Validator(simple_schema)
        data = {"name": "John"}  # age

        with pytest.raises(MissingFieldError) as exc_info:
            validator.validate(data)

        assert "age" in str(exc_info.value)

    # Перевірка типу
    def test_wrong_type_string(self, simple_schema):
        validator = Validator(simple_schema)
        data = {"name": "John", "age": "25"} 

        with pytest.raises(TypeMismatchError):
            validator.validate(data)

    def test_wrong_type_number(self, simple_schema):
        validator = Validator(simple_schema)
        data = {"name": 123, "age": 25}  # name має бути str, не int

        with pytest.raises(TypeMismatchError):
            validator.validate(data)


