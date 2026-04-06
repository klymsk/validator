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

# Діапазони
class TestNumberConstraints:
    @pytest.fixture
    def number_schema(self):
        return {
            "id": {"type": int, "min": 1, "max": 9999}
        }

    def test_valid_number(self, number_schema):
        validator = Validator(number_schema)
        assert validator.validate({"id": 100}) is True
        assert validator.validate({"id": 1}) is True
        assert validator.validate({"id": 9999}) is True

    def test_number_below_min(self, number_schema):
        validator = Validator(number_schema)

        with pytest.raises(ConstraintError) as exc_info:
            validator.validate({"id": 0})

        assert "менше" in str(exc_info.value).lower()

    def test_number_above_max(self, number_schema):
        validator = Validator(number_schema)

        with pytest.raises(ConstraintError) as exc_info:
            validator.validate({"id": 10000})

        assert "більше" in str(exc_info.value).lower()